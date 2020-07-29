import tkinter.messagebox
import platform
import random
import genanki
import csv
from tkinter import *
from tkinter.filedialog import askopenfilename

class ExportDeck:
    def __init__(self, master):
        self.root = root
        root.title("Export Deck")
        if 'aarch64' in platform.platform():
        	root.attributes('-fullscreen', True)
        else:
        	root.geometry("600x600")
 
        self.fileNameLabel = Message(root, text = "File Name", width=294)
        self.fileNameLabel.pack()
        self.filename = ""

        self.btnSelectFile = Button(root, text = "Select File", command=self.selectFile)
        self.btnSelectFile.pack()
         
        self.selectDelimLabel = Label(root, text = "Fields separated by:")
        self.selectDelimLabel.pack()
        self.delim = ''

        self.var = IntVar()
        R1 = Radiobutton(root, text='"," comma', variable=self.var, value=1, command=self.sel)
        R1.pack()

        R2 = Radiobutton(root, text='"\\t" tab      ', variable=self.var, value=2, command=self.sel)
        R2.pack()

        self.btnImportFile = Button(root, text = "Import", command=self.importFile)
        self.btnImportFile.pack()

    def selectFile(self):
        self.filename = askopenfilename(filetypes=[("Text, CSV, TSV Files", ".txt .csv .tsv")])
        print(self.filename)
        self.fileNameLabel.config(text=self.filename)

    def sel(self):
        selection = self.var.get()
        if selection == 1:
            self.delim = ','
            
        if selection == 2:
            self.delim = '\t'

    def importFile(self):
        self.window = Toplevel(self.root)
        if 'aarch64' in platform.platform():
        	 self.window.attributes('-fullscreen', True)
        else:
             self.window.geometry('500x600')

        deckNameLabel = Label(self.window, text="Name of Deck")
        deckNameLabel.grid(row=0, column=0)

        self.deckNameEntry = Entry(self.window)
        self.deckNameEntry.grid(row=0, column=1)
        
        deckTitleLabel = Label(self.window, text="Title of Deck")
        deckTitleLabel.grid(row=1, column=0)
        
        self.deckTitleEntry = Entry(self.window)
        self.deckTitleEntry.grid(row=1, column=1)

        
        deckModelLabel = Label(self.window, text="Model of Deck")
        deckModelLabel.grid(row=2, column=0)
        
        self.deckModelEntry = Entry(self.window)
        self.deckModelEntry.grid(row=2, column=1)

        mapFieldLabel = Label(self.window, text="Enter Fields Name")
        mapFieldLabel.grid(row=3, column=0, padx=20, pady=8)

        datafilename = self.filename

        d = self.delim
        f = open(datafilename, 'r', encoding='utf-8')

        reader = csv.reader(f, delimiter=d)
        ncol = len(next(reader))

        self.fields = []
        self.fieldNum = []
        for i in range(ncol):
            self.fieldNum.append("Field" + str(i))

        label = {}
        self.entry = {}
        i=4   # 3 entry box above
        for field in self.fieldNum:
            lb = Label(self.window, text=field)
            lb.grid(row=i, column=0)
            label[field] = lb

            en = Entry(self.window, textvariable=field)
            en.grid(row=i, column=1)
            self.entry[field] = en
            i += 1
        
        
        btnExportDeck = Button(self.window, text = "Export", command=self.exportDeck)
        btnExportDeck.grid(row=i, column=1)


    def exportDeck(self):
        try:
            flag = False
            for field in self.fieldNum:
                if len(self.entry[field].get()) > 0:
                    flag = True
                else:
                    flag = False
            
            if len(self.deckNameEntry.get()) > 0 and len(self.deckTitleEntry.get()) > 0 and len(self.deckModelEntry.get()) > 0 and flag:

                back = ""
                front = "<div>{{" + self.entry['Field0'].get() + "}}</div>"

                for field in self.fieldNum:
                    back += "<div>{{" + self.entry[field].get() + "}}</div>\n"
                    self.fields.append({"name" : self.entry[field].get() })

                #print(front)
                #print(back)
                
                data_filename = self.filename

                deck_filename = self.deckNameEntry.get() + ".apkg"
                
                anki_deck_title = self.deckTitleEntry.get()

                anki_model_name = self.deckModelEntry.get()

                model_id = random.randrange(1 << 30, 1 << 31)

                style = """
.card {
font-family: arial;
font-size: 24px;
text-align: center;
color: black;
background-color: white;
}
"""      
                #print(self.fields)
                anki_model = genanki.Model(
                    model_id,
                    anki_model_name,
                    fields = self.fields,
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
                    csv_reader = csv.reader(csv_file, delimiter = self.delim)
                    for row in csv_reader:
                        flds = []
                        for i in range(len(row)):
                            flds.append(row[i])

                        anki_note = genanki.Note(
                        model=anki_model,
                        fields=flds,
                        )
                        anki_notes.append(anki_note)

                random.shuffle(anki_notes)

                anki_deck = genanki.Deck(model_id, anki_deck_title)
                anki_package = genanki.Package(anki_deck)

                for anki_note in anki_notes:
                    anki_deck.add_note(anki_note)

                anki_package.write_to_file(deck_filename)

                print("Deck generated with {} flashcards".format(len(anki_deck.notes)))
                
                messagebox.showinfo("Success", "Deck generated!")

                self.window.destroy()

            else:
                print("Fields are empty!")
        except:
            print("Deck Creation Failed!")
            messagebox.showerror("Failed", "Deck not generated!")

root = Tk()
gui = ExportDeck(root)
root.mainloop()
