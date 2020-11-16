helper_string = """
ScreenManager:
    id: screen_manager
    MainScreen:
        id: main_screen_id
    ExportScreen:
        id: export_screen_id
        
<MainScreen>:
    name: 'main_screen'
    BoxLayout:
        orientation: "vertical"
        spacing: "5dp"
            
        MDToolbar:
            id: main_screen_top_toolbar
            title: "Anki Deck Export"
            elevation: 5
            pos_hint: {'top': 1}
                            
        ScrollView:              
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: dp(28)
                spacing: dp(15)
                                
                MDFlatButton:
                    text: 'Select File'
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    theme_text_color: "Custom"
                    text_color: rgba('ffffff')
                    md_bg_color: rgba('2196f3')
                    on_press: app.file_manager_open()
                    
                MDLabel:
                    text: ""
                    id: path_selected_label
                    halign: 'center'
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    height: self.texture_size[1]
                    
                MDLabel:
                    halign: 'center'
                    text: 'Fields separated by'
                    
                MDDropDownItem:
                    id: drop_item
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    text: 'Default TAB'
                    on_release: app.change_field_sep()
                    
                MDFlatButton:
                    text: 'Import'
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    theme_text_color: "Custom"
                    text_color: rgba('ffffff')
                    md_bg_color: rgba('2196f3') 
                    on_press: app.import_file()

<ExportScreen>:
    name: 'export_screen'
    BoxLayout:
        orientation: "vertical"
        spacing: "5dp"
            
        MDToolbar:
            title: "Anki Deck Export"
            elevation: 5
            pos_hint: {'top': 1}
                            
        ScrollView:              
            MDBoxLayout:
                id: export_screen_box_layout
                orientation: 'vertical'
                adaptive_height: True
                padding: dp(28)
                spacing: dp(15)
                                
                MDTextField:
                    id: tf_deck_title
                    hint_text: 'Deck Title'
                    helper_text: "Name appear at top in AnkiDroid app"
                    helper_text_mode: "on_focus"
                
                MDTextField:
                    id: tf_deck_model
                    hint_text: 'Deck Model'
                
                MDLabel:
                    halign: 'center'
                    text: 'Enter fields name'
                
                MDBoxLayout:
                    id: export_screen_box_layout_fields
                    orientation: 'vertical'
                    adaptive_height: True
                    padding: dp(28)
                    spacing: dp(15)
"""