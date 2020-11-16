
var db;
window.onload = function () {
initSqlJs(config).then(function (SQL) {
    db = new SQL.Database();
    db.run(schema);
    db.run(col);
});
}

class Package {
    constructor() {
        this.decks = []
        this.media = []
    }

    addDeck(deck) {
        this.decks.push(deck)
    }

    addMedia(data, name) {
        this.media.push({ name, data })
    }

    addMediaFile(filename, name = null) {
        this.media.push({ name: name || filename, filename })
    }

    /*
    writeToFile(filename) {
      const {name, fd} = tmp.fileSync()
      const db = require('better-sqlite3')(name)
      this.write(db)
      db.close()
      const out = fs.createWriteStream(filename)
      const archive = archiver('zip')
      archive.pipe(out)
      archive.file(name, { name: 'collection.anki2' })
      const media_info = {}
      this.media.forEach((m, i) => {
        if (m.filename != null) archive.file(m.filename, { name: i.toString() })
        else archive.append(m.data, { name: i.toString() })
        media_info[i] = m.name
      })
      archive.append(JSON.stringify(media_info), { name: 'media' })
      return archive.finalize()
    }
    */

    writeToFile(filename) {

        var zip = new JSZip();

        //zip.file("Hello.txt", "Hello World\n");

        this.write(db)

        zip.file("collection.anki2", db);
        zip.file("media", "{}");

        zip.generateAsync({ type: "blob" }).then(function (content) {
            // see FileSaver.js
            saveAs(content, "export.apkg");

        });

    }

    write() {
        const now = new Date
        const models = {}
        const decks = {}
        this.decks.forEach(d => {
            d.notes.forEach(n => models[n.model.props.id] = n.model.props)
            decks[d.id] = {
                ...defaultDeck,
                id: d.id,
                name: d.name,
            }
        })


        const col = {
            id: null,
            crt: (+now/1000)|0,
            mod: +now,
            scm: +now,
            ver: 11,
            dty: 0,
            usn: 0,
            ls: 0,
            conf: JSON.stringify(defaultConf),
            models: JSON.stringify(models),
            decks: JSON.stringify(decks),
            dconf: JSON.stringify({1: {id: 1, ...defaultDeckConf}}),
            tags: JSON.stringify({}),
          }
      
        //   db.run(`INSERT INTO col
        //       (id, crt, mod, scm, ver, dty, usn, ls, conf, models, decks, dconf, tags)
        //       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        //     [null, (+now/1000)|0, +now, +now, 11, 0, 0, 0, JSON.stringify(defaultConf), JSON.stringify(models), JSON.stringify(decks), JSON.stringify({1: {id: 1, ...defaultDeckConf}}), JSON.stringify({}) ]
        //     )
      

        // const insert_notes = db.prepare(
        //     `INSERT INTO notes (id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data)
        //     VALUES (null, $guid, $mid, $mod, $usn, $tags, $flds, $sfld, 0, 0, '')`
        //   )
        //   const insert_cards = db.prepare(
        //     `INSERT INTO cards (id, nid, did, ord, mod, usn, type, queue, due, ivl, factor, reps, lapses, left, odue, odid, flags, data)
        //     VALUES (null, $nid, $did, $ord, $mod, $usn, $type, $queue, 0, 0, 0, 0, 0, 0, 0, 0, 0, '')`
        //   )

        for (const deck of this.decks) {
            for (const note of deck.notes) {
                var mod = (+now / 1000) | 0;

                console.log(note.guid, note.model.props.id, mod, -1, note.tags, note.fields.join('\x1f'), 0);

                db.run( `INSERT INTO notes (id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data)
                VALUES (null, ?, ?, ?, ?, ?, ?, ?, 0, 0, '')`, [note.guid, note.model.props.id, mod, -1, note.tags, note.fields.join('\x1f'), 0]);

                // insert_notes.run({
                //     id: note_id,
                //     guid: note.guid,
                //     mid: note.model.props.id,
                //     mod: (+now / 1000) | 0,
                //     usn: -1,
                //     tags: note.tags,
                //     flds: note.fields.join('\x1f'),
                //     sfld: 0,
                // })

                for (const card_ord of note.cards) {

                    var note_id = Math.floor(1000000000000 + Math.random() * 9000000000000);
                    var new_random = Math.floor(100 + Math.random() * 900)
                    var card_id = Date.now() + new_random;

                    // insert_cards.run({
                    //     id: card_id,
                    //     nid: note_id,
                    //     did: deck.id,
                    //     ord: card_ord,
                    //     mod: (+now / 1000) | 0,
                    //     usn: -1,
                    //     type: 0, // 0=new, 1=learning, 2=due 
                    //     queue: 0, // -1 for suspended
                    // })

                    var mod2 = (+now / 1000) | 0;

                    db.run(
                        `INSERT INTO cards (id, nid, did, ord, mod, usn, type, queue, due, ivl, factor, reps, lapses, left, odue, odid, flags, data)
                        VALUES (null, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, '')`, [note_id, deck.id, card_ord, mod2, -1, 0, 0 ]
                      )
                
                
                }

                
            }
        } // for loop


    }
}