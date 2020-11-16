from kivy.lang import Builder
from kivy.properties import DictProperty
from kivy.utils import rgba
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.utils import platform
import random
import genanki
import csv
import os
import traceback

from kivy.core.window import Window
Window.softinput_mode = 'below_target'

from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path

from kivymd.uix.textfield import MDTextField

from main_str import helper_string


class MainScreen(Screen):
    pass

class ExportScreen(Screen):
    pass


class AnkiExport(MDApp):
    dynamic_ids = DictProperty({})

    def build(self):
        if platform == 'android':
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
            ])
        self.field_sep_tab = True

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path
        )
        self.file_manager.ext = ['.txt', '.tsv', '.csv']

        self.sm = Builder.load_string(helper_string)

        self.back_btn_press_count = 0
        Window.bind(on_keyboard=self.on_back_press)

        return self.sm

    def on_back_press(self, window, key, *args):
        if key == 27:  # the esc key
            if self.sm.current == "main_screen":
                self.back_btn_press_count += 1

                if self.back_btn_press_count > 1:
                    MDApp.get_running_app().stop()
                else:
                    toast('Press again to exit')

            elif self.sm.current == "export_screen":
                self.sm.current = "main_screen"
                self.back_btn_press_count = 0
                self.sm.ids.export_screen_id.ids.export_screen_box_layout_fields.clear_widgets()

            else:
                self.sm.current = "main_screen"
                self.back_btn_press_count = 0

    def exit_manager(self):
        self.file_manager.close()

    def select_path(self, path):
        self.exit_manager()
        self.file_selected(path)

    def file_manager_open(self):
        if platform == 'android':
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            SD_CARD = primary_external_storage_path()
            self.file_manager.show(SD_CARD)
        else:
            self.file_manager.show("/")

    def file_selected(self, path):
        self.sm.ids.main_screen_id.ids.path_selected_label.text = path

    def import_file(self):
        if self.sm.ids.main_screen_id.ids.path_selected_label.text != "":
            self.sm.current = "export_screen"
            datafilename = self.sm.ids.main_screen_id.ids.path_selected_label.text

            if self.field_sep_tab:
                self.delim = '\t'
            else:
                self.delim = ','

            f = open(datafilename, 'r', encoding='utf-8')

            reader = csv.reader(f, delimiter=self.delim)
            self.ncol = len(next(reader))

            for i in range(self.ncol):
                id = "Field" + str(i)
                tf_name = MDTextField(id=id)
                tf_name.hint_text = "Field " + str(i)

                self.sm.ids.export_screen_id.ids.export_screen_box_layout_fields.add_widget(tf_name)

                self.dynamic_ids[id] = tf_name

            flat_btn = MDFlatButton(text="Export Deck", pos_hint={'center_x': .5, 'center_y': .5}, on_press=self.exportDeck)

            flat_btn.text_color = rgba('ffffff')
            flat_btn.md_bg_color = rgba('2196f3')

            self.sm.ids.export_screen_id.ids.export_screen_box_layout_fields.add_widget(flat_btn)

        else:
            toast('Select file first')

    def change_field_sep(self):
        if self.field_sep_tab:
            self.sm.ids.main_screen_id.ids.drop_item.text = 'COMMA'
            self.field_sep_tab = False
        else:
            self.sm.ids.main_screen_id.ids.drop_item.text = 'TAB'
            self.field_sep_tab = True


    def exportDeck(self, btn):
        if platform == 'android':
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            SD_CARD = primary_external_storage_path()
            folder = os.path.join(SD_CARD, 'Anki Deck Export')
        else:
            folder = 'Anki Deck Export'

        if not os.path.exists(folder):
            os.makedirs(folder)

        # imported file name
        data_filename = self.sm.ids.main_screen_id.ids.path_selected_label.text

        # title
        anki_deck_title = self.sm.ids.export_screen_id.ids.tf_deck_title.text

        # model
        anki_model_name = self.sm.ids.export_screen_id.ids.tf_deck_model.text

        deck_name = anki_deck_title + "_Export_" + ".apkg"

        if platform == 'android':
            # deck file
            deck_filename = os.path.join(SD_CARD, 'Anki Deck Export', deck_name)
        else:
            deck_filename = os.path.join('Anki Deck Export', deck_name)

        model_id = random.randrange(1 << 30, 1 << 31)

        flag = False

        front = "<div>{{" + self.dynamic_ids["Field0"].text + "}}</div>"
        back = ""

        self.fields = []
        for field in self.dynamic_ids:
            self.fields.append({"name": self.dynamic_ids[field].text})
            back += "<div>{{" + self.dynamic_ids[field].text + "}}</div>\n"

        for field in self.dynamic_ids:
            if len(self.dynamic_ids[field].text) > 0:
                flag = True
            else:
                flag = False

        style = """
.card {
font-family: arial;
font-size: 20px;
text-align: center;
color: black;
background-color: white;
}
        """

        try:
            if flag:
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

                #random.shuffle(anki_notes)

                anki_deck = genanki.Deck(model_id, anki_deck_title)
                anki_package = genanki.Package(anki_deck)

                for anki_note in anki_notes:
                    anki_deck.add_note(anki_note)

                anki_package.write_to_file(deck_filename)

                toast("Deck generated with {} flashcards".format(
                    len(anki_deck.notes)))

            else:
                toast("Fields are empty!")
        except:
            toast("Deck Creation Failed!")
            print(traceback.print_exc())

AnkiExport().run()