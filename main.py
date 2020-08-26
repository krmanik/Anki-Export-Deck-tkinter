import tkinter.messagebox
import platform
import random
import genanki
import csv
from tkinter import *
from tkinter import font
from tkinter.filedialog import askopenfilename


class ExportDeck:
    def __init__(self, master):
        self.root = root
        root.title("Export Deck")
        root.config(bg="white")

        if 'aarch64' in platform.platform():
            root.attributes('-fullscreen', True)
            self.fontRoboto = font.Font(
                family='Roboto', size=12, weight='bold')
            self.fontRoboto1 = font.Font(
                family='Roboto', size=8, weight='bold')
            self.fontRoboto2 = font.Font(
                family='Roboto', size=10, weight='bold')
        else:
            root.geometry("360x640")
            self.fontRoboto = font.Font(
                family='Roboto', size=18, weight='bold')
            self.fontRoboto1 = font.Font(
                family='Roboto', size=12, weight='bold')
            self.fontRoboto2 = font.Font(
                family='Roboto', size=16, weight='bold')

        projectTitleLabel = Label(root, text="Anki Deck Export")
        projectTitleLabel.config(
            font=self.fontRoboto2, bg="white", fg="#5599ff")
        projectTitleLabel.pack()

        self.entryFrame = Frame(
            root, background="#00ccff", borderwidth=1, relief=FLAT)

        self.fileNameEntry = Entry(self.entryFrame)
        self.fileNameEntry.config(bd=0, fg="#535d6c")

        self.entryFrame.pack(fill=BOTH, padx=5, pady=8)
        self.fileNameEntry.pack(fill=BOTH)

        self.btnSelectFile = Button(
            root, text="Select File", command=self.selectFile)
        self.btnSelectFile.config(highlightthickness=0, bd=0, fg="white", bg="#00ccff",
                                  activebackground="#00ccff", activeforeground="white", font=self.fontRoboto)
        self.btnSelectFile.pack(pady=12)

        self.tkvar = StringVar(root)
        self.fieldSep = {'TAB', 'COMMA'}
        self.tkvar.set('TAB')

        self.entryOptionMenuFrame = Frame(
            root, background="white", relief=FLAT)
        self.entryOptionMenuFrame.pack(padx=20, fill=BOTH)

        self.entryDelimFrame = Frame(
            self.entryOptionMenuFrame, background="#00ccff", borderwidth=1, relief=FLAT)
        self.entryDelimFrame.pack(side=RIGHT)

        self.selectDelimLabel = Label(
            self.entryOptionMenuFrame, text="Fields separated by")
        self.selectDelimLabel.config(
            font=self.fontRoboto, bg="white", fg="#00ccff")
        self.selectDelimLabel.pack(pady=5, side=LEFT)

        optionMenu = OptionMenu(self.entryDelimFrame,
                                self.tkvar, *self.fieldSep)
        optionMenu.config(bd=0, fg="#00ccff", background="white",
                          activebackground="white", activeforeground="#00ccff", font=self.fontRoboto1)
        optionMenu["menu"].config(bd=0, fg="#00ccff", background="white",
                                  activebackground="#00ccff", activeforeground="white")
        optionMenu.pack()

        self.filename = ""
        self.delim = ''

        self.btnImportFile = Button(
            root, text="Import", command=self.importFile)

        self.btnImportFile.config(highlightthickness=0, bd=0, fg="white", bg="#5fd38d",
                                  activebackground="#5fd38d", activeforeground="white", font=self.fontRoboto)
        self.btnImportFile.pack(pady=20, padx=20, fill=BOTH)

    def selectFile(self):
        self.filename = askopenfilename(
            filetypes=[("Text, CSV, TSV Files", ".txt .csv .tsv")])
        print(self.filename)
        self.fileNameEntry.insert(END, self.filename)

    def importFile(self):
        if len(self.filename) > 0:

            # print(self.tkvar.get())
            selection = self.tkvar.get()

            if selection == "TAB":
                self.delim = '\t'

            if selection == "COMMA":
                self.delim = ','

            self.window = Toplevel(self.root)
            self.window.config(bg="white")
            if 'aarch64' in platform.platform():
                self.window.attributes('-fullscreen', True)
            else:
                self.window.geometry("430x640")

            projectTitleNameFrame = Frame(self.window, relief=FLAT)
            projectTitleNameFrame.grid(row=0, columnspan=2)
            projectTitleLabel = Label(
                projectTitleNameFrame, text="Anki Deck Export")
            projectTitleLabel.config(
                font=self.fontRoboto2, bg="white", fg="#5599ff")
            projectTitleLabel.grid(row=0)

            entryDeckNameFrame = Frame(
                self.window, background="#00ccff", borderwidth=1, relief=FLAT)
            entryDeckTitleFrame = Frame(
                self.window, background="#00ccff", borderwidth=1, relief=FLAT)
            entryDeckModelFrame = Frame(
                self.window, background="#00ccff", borderwidth=1, relief=FLAT)

            deckTitleLabel = Label(self.window, text="Title of Deck    ")
            deckTitleLabel.config(font=self.fontRoboto1,
                                  bg="white", fg="#00ccff")
            deckTitleLabel.grid(row=1, column=0)

            self.deckTitleEntry = Entry(entryDeckTitleFrame, bd=0)
            self.deckTitleEntry.grid(row=1, column=1)
            self.deckTitleEntry.config(font=self.fontRoboto1)
            entryDeckTitleFrame.grid(row=1, column=1, pady=2)

            deckNameLabel = Label(self.window, text="Name of Deck ")
            deckNameLabel.config(font=self.fontRoboto1,
                                 bg="white", fg="#00ccff")
            deckNameLabel.grid(row=2, column=0)

            self.deckNameEntry = Entry(entryDeckNameFrame, bd=0)
            self.deckNameEntry.grid(row=2, column=1)
            self.deckNameEntry.config(font=self.fontRoboto1)
            entryDeckNameFrame.grid(row=2, column=1, pady=2)

            deckModelLabel = Label(self.window, text="Model of Deck")
            deckModelLabel.config(font=self.fontRoboto1,
                                  bg="white", fg="#00ccff")
            deckModelLabel.grid(row=3, column=0)

            self.deckModelEntry = Entry(entryDeckModelFrame, bd=0)
            self.deckModelEntry.grid(row=3, column=1)
            self.deckModelEntry.config(font=self.fontRoboto1)
            entryDeckModelFrame.grid(row=3, column=1, pady=2)

            mapFieldLabel = Label(self.window, text="Enter Fields Name")
            mapFieldLabel.config(font=self.fontRoboto2,
                                 bg="white", fg="#5599ff")
            mapFieldLabel.grid(row=4, column=0, padx=20, pady=8)

            datafilename = self.filename

            d = self.delim
            f = open(datafilename, 'r', encoding='utf-8')

            reader = csv.reader(f, delimiter=d)
            ncol = len(next(reader))

            self.fields = []
            self.fieldNum = []
            for i in range(ncol):
                self.fieldNum.append("Field " + str(i))

            label = {}
            self.entry = {}

            enFrame = {}

            i = 5   # entry box and title above
            for field in self.fieldNum:
                lb = Label(self.window, text=field)
                lb.config(font=self.fontRoboto1, bg="white", fg="#00ccff")
                lb.grid(row=i, column=0, pady=2)
                label[field] = lb

                fr = Frame(self.window, background="#00ccff",
                           borderwidth=1, relief=FLAT)
                fr.grid(row=i, column=1, pady=2)

                en = Entry(fr, textvariable=field)
                en.config(bd=0, fg="#535d6c", font=self.fontRoboto1)
                en.grid(row=i, column=1)
                self.entry[field] = en
                i += 1

            btnExportDeck = Button(
                self.window, text="Export", command=self.exportDeck)
            btnExportDeck.config(highlightthickness=0, bd=0, fg="white", bg="#5fd38d",
                                 activebackground="#5fd38d", activeforeground="white", font=self.fontRoboto)
            btnExportDeck.grid(row=i, columnspan=2, pady=16, ipadx=40)

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
                front = "<div>{{" + self.entry['Field 0'].get() + "}}</div>"

                for field in self.fieldNum:
                    back += "<div>{{" + self.entry[field].get() + "}}</div>\n"
                    self.fields.append({"name": self.entry[field].get()})

                # print(front)
                # print(back)

                data_filename = self.filename

                deck_filename = self.deckNameEntry.get() + ".apkg"

                anki_deck_title = self.deckTitleEntry.get()

                anki_model_name = self.deckModelEntry.get()

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
                    fields=self.fields,
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
                    csv_reader = csv.reader(csv_file, delimiter=self.delim)
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

                print("Deck generated with {} flashcards".format(
                    len(anki_deck.notes)))

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
