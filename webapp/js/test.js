/*

// step 1
const m = new Model({
  name: "Basic (and reversed card)",
  id: "1542906796044",
  flds: [
    { name: "Front" },
    { name: "Back" }
  ],
  req: [
    [0, "all", [0]],
    [1, "all", [1]]
  ],
  tmpls: [
    {
      name: "Card 1",
      qfmt: "{{Front}}",
      afmt: "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}",
    },
    {
      name: "Card 2",
      qfmt: "{{Back}}",
      afmt: "{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}",
    }
  ],
})

// step 2

const d = new Deck(1542998993960, "hi")
d.addNote(m.note(['this is front', 'this is back']))


// step 3

const p = new Package()
p.addDeck(d)
p.write()

// step 4
var zip = new JSZip();
const decoder = new TextDecoder('utf-8');

// step 5

var data = db.export()
zip.file("collection.anki2", decoder.decode(db.export()));

// step 6

zip.file("media", "{}")

// step 7

zip.generateAsync({ type: "blob" }).then(function (content) {
  // see FileSaver.js
  saveAs(content, "example.apkg");
});

*/