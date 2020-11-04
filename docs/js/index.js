pythonCode = `
    """
    Author: Infinyte7 (Mani)
    """

    def exportDeck(*args):
        import os
        import csv
        import random
        import genanki
        import traceback
        
        data_filename = "/input.txt"
        anki_deck_title = "Anki Export"
        anki_model_name = "Basic (Anki-Export)"
        
        csv_fields = []

        for f in fields:
            csv_fields.append({"name": f})

        deck_filename = "output.apkg"
    
        try:
            back = ""
            front = "<div>{{" + str(fields[0]) + "}}</div>"
    
            for field in fields:
                back += "<div>{{" + str(field) + "}}</div>\\n"
    
            model_id = random.randrange(1 << 30, 1 << 31)
    
            style = """.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
    }
    """
            anki_model = genanki.Model(
                model_id,
                anki_model_name,
                fields=csv_fields,
                templates=[
                    {
                        "name": "Card 1",
                        "qfmt": front,
                        "afmt": back,
                    },
                ],
                css=style,
            )
    
            anki_notes = []
    
            with open(data_filename, "r", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=delimiter)
                for row in csv_reader:
                    flds = []
                    for i in range(len(row)):
                        flds.append(row[i])
    
                    anki_note = genanki.Note(
                        model=anki_model,
                        fields=flds,
                    )
                    anki_notes.append(anki_note)
    
            #random.shuffle(anki_notes)
    
            anki_deck = genanki.Deck(model_id, anki_deck_title)
            anki_package = genanki.Package(anki_deck)
    
            for anki_note in anki_notes:
                anki_deck.add_note(anki_note)
    
            anki_package.write_to_file(deck_filename)
    
            deck_export_msg = "Deck generated with {} flashcards".format(len(anki_deck.notes))
            js.document.getElementById("deck-generated-msg").innerHTML = "<h5>" + deck_export_msg + "</h5>"
            js.showSnackbar(deck_export_msg)
            js.document.getElementById('downloadCard').style.display = "block"
            
        except:
            traceback.print_exc()
            deck_export_msg = "Deck Creation Failed! Try again"
            js.showSnackbar(deck_export_msg)
            js.document.getElementById('downloadCard').style.display = "none"
    
    import micropip

    # localhost
    # micropip.install("http://localhost:8000/py-whl/frozendict-1.2-py3-none-any.whl")
    # micropip.install("http://localhost:8000/py-whl/pystache-0.5.4-py3-none-any.whl")
    # micropip.install("http://localhost:8000/py-whl/PyYAML-5.3.1-cp38-cp38-win_amd64.whl")
    # micropip.install('http://localhost:8000/py-whl/cached_property-1.5.2-py2.py3-none-any.whl')
    # micropip.install("http://localhost:8000/py-whl/genanki-0.8.0-py3-none-any.whl")

    # from GitHub using CDN
    micropip.install("https://cdn.jsdelivr.net/gh/infinyte7/Anki-Export-Deck-tkinter/docs/py-whl/frozendict-1.2-py3-none-any.whl")
    micropip.install("https://cdn.jsdelivr.net/gh/infinyte7/Anki-Export-Deck-tkinter/docs/py-whl/pystache-0.5.4-py3-none-any.whl")
    micropip.install("https://cdn.jsdelivr.net/gh/infinyte7/Anki-Export-Deck-tkinter/docs/py-whl/PyYAML-5.3.1-cp38-cp38-win_amd64.whl")
    micropip.install("https://cdn.jsdelivr.net/gh/infinyte7/Anki-Export-Deck-tkinter/docs/py-whl/cached_property-1.5.2-py2.py3-none-any.whl")
    micropip.install("https://cdn.jsdelivr.net/gh/infinyte7/Anki-Export-Deck-tkinter/docs/py-whl/genanki-0.8.0-py3-none-any.whl")
        `

languagePluginLoader.then(() => {
    return pyodide.loadPackage(['micropip'])
}).then(() => {
    pyodide.runPython(pythonCode);

    document.getElementById("loading-msg").style.display = "none";
    document.getElementById("loading-spinner").style.display = "none";

    showSnackbar("Ready to import file");
})

languagePluginLoader.then(function () {
    console.log('Ready');
});

function exportDeck() {
    // type conversion from javascript to python
    var field;
    var empty = false;
    for (i=0; i<fieldsCount; i++) {
        field = "field" + i
        if (document.getElementById(field).value == "") {
            empty = true;
            break;
        }
    }

    if (!empty) {
        pyodide.runPython(`
        import js
        fields = []
        for i in range(0, fieldsCount):
            field = "field" + str(i)
    
            field_value = js.document.getElementById(field).value
            print(field_value)
    
            fields.append(field_value)
        exportDeck()
        `);
    } else {
        showSnackbar("Empty fields");
    }
}

var content = null;
var firstLine = null;
var fieldsCount = null;
var file = null;
var reader = null;
var delimiter = null;

function inputFile() {
    file = document.getElementById("file").files[0];
    reader = new FileReader();
}

function importFile() {
    try {

        delimiter = document.getElementById('fieldSeparatedBy').value;

        if (delimiter == "tab") {
            delimiter = "\t";
        } else if (delimiter == "comma") {
            delimiter = ",";
        }

        reader.readAsText(file);
        reader.onload = evt => {
            content = evt.target.result;
            //console.log(content);

            firstLine = content.split('\n').shift();
            console.log(firstLine);

            fieldsCount = firstLine.split(delimiter).length;
            console.log(fieldsCount);

            var fields = "";
            var j = 0;

            for (i = 0; i < fieldsCount; i++) {
                j = i+1;
                fields += "<div class='input-field col s12'><input id='field" + i 
                + "' type='text'></input><label for='field"+ i +"'>Field " + j 
                + "</label></div>";
            }

            document.getElementById('fields').innerHTML = fields;

            pyodide.runPython("from js import content, fieldsCount, delimiter");
            //pyodide.runPython("print(content)");
            pyodide.runPython("print(fieldsCount)");
            pyodide.runPython(`
            with open('input.txt', 'w', encoding='utf-8') as f:
                f.write(content);
            `)

            document.getElementById("fields-card").style.display = "block";
            document.getElementById("fields-msg").innerHTML = "<h5>Enter fields name</h5>";
        }

    } catch (error) {
        console.log(error);
        document.getElementById("fields-card").style.display = "none";
        showSnackbar("Failed to import file. Check file or try again");
    }

}

function downloadDeck() {
    let txt = pyodide.runPython(`                  
    with open('/output.apkg', 'rb') as fh:
        out = fh.read()
    out
    `);

    const blob = new Blob([txt], { type: 'application/zip' });
    let url = window.URL.createObjectURL(blob);

    var downloadLink = document.createElement("a");
    downloadLink.href = url;
    downloadLink.download = "Export-Deck.apkg";
    document.body.appendChild(downloadLink);
    downloadLink.click();
}

function showSnackbar(msg) {
    var x = document.getElementById("snackbar");

    x.innerHTML = msg;
    x.className = "show";

    setTimeout(function () { x.className = x.className.replace("show", ""); }, 3000);
}
