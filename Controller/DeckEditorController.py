from Data.DataGenerator import DataGenerator
from UI.DeckEditor import DeckEditor

class DeckEditorController:
    def __init__(self):
        self.deck_generator = DataGenerator(
            download_ygo_images=False,
            generate_all_deck_urls=False,
            generate_deck_data_from_urls=False,
            max_threads_1=2,
            max_threads_2=10,
            max_thread_images=50
        )

        self.deck_editor = DeckEditor(self.deck_generator, 900, 1600, "Command Window")
        self.deck_editor.update_gui()
        self.deck_editor.mainloop()