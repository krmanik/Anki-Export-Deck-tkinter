"""
Author: Infinyte7 (Mani)
"""

import random
import genanki
import csv
import traceback
import os.path
from os import path

def exportDeck():

    data_filename = str(input("Enter input file name with extension: "))

    if not path.exists(data_filename):
        print("File not exists")
        quit()

    anki_deck_title = str(input("Enter title of deck: "))

    if len(anki_deck_title) == 0:
        print("Empty title")
        quit()

    # model name
    r1 = str(random.randrange(1 << 10, 1 << 11))
    anki_model_name = str(input("Enter model of deck: "))
    anki_model_name = anki_model_name + "-Basic-" + r1

    delim = "\t"

    d = str(input("Fields are separated by (tab, comma): "))
    if d == "TAB" or d == "tab":    
        delim = "\t"
    elif d == "COMMA" or d == "comma":    
        delim = ","
    else:
        print("Not supported...")

    csv_fields = []
    fields = []

    f = open(data_filename, 'r', encoding='utf-8')

    reader = csv.reader(f, delimiter=delim)
    ncol = len(next(reader))

    for i in range(ncol):
        msg = "Enter field " + str(i) + " name: "
        field = str(input(msg))
        csv_fields.append({"name": field})
        fields.append(field)

    # exported deck name
    r2 = str(random.randrange(1 << 15, 1 << 16))

    deck_filename = "export_" + r2 + ".apkg"

    try:
        back = ""
        front = "<div>{{" + str(fields[0]) + "}}</div>"

        for field in fields:
            back += "<div>{{" + str(field) + "}}</div>\n"

        model_id = random.randrange(1 << 30, 1 << 31)

        style = """
.card {
font-family: arial;
font-size: 20px;
text-align: center;
color: black;
background-color: white;
}
"""
        # print(self.fields)
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
            csv_reader = csv.reader(csv_file, delimiter=delim)
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

        print("Deck generated with {} flashcards".format(
            len(anki_deck.notes)))
        
    except:
        traceback.print_exc()
        print("Deck Creation Failed!")

exportDeck()
