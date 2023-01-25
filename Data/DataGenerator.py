from Controller.FileAndDirectoryController import FileDirectoryController, JSONController
from Controller.WebsiteController import WebsiteController
from Controller.ThreadController import ThreadController
from Controller.YgoproController import YgoproController
from Data.DeckFormat import DeckFormat

class DataGenerator:
    def __init__(self, download_ygo_images=False, generate_all_deck_urls=False, generate_deck_data_from_urls=False, max_threads_1=10, max_threads_2=10, max_thread_images=10):
        self.ygopro_controller = YgoproController(max_thread_images)

        self.my_data = {}
        for deck_format in DeckFormat().return_list():
            self.my_data[deck_format] = {}

        self.deck_lists = {}
        for deck_format in DeckFormat().return_list():
            self.deck_lists[deck_format] = []

        self.deck_data = {}
        for deck_format in DeckFormat().return_list():
            self.deck_data[deck_format] = {}

        self.max_threads_1 = max_threads_1
        self.max_threads_2 = max_threads_2

        if download_ygo_images:
            thread_controller = ThreadController(max_thread_images)
            thread_controller.start_load_wait(self.ygopro_controller.download_all_images_thread)

        for deck_format in DeckFormat().return_list():
            self.deck_format = deck_format
            self.data_file = FileDirectoryController().read_and_write_file("Data/1.MyData", f"{self.deck_format}.txt")
            self.load_my_data()
            self.generate_all_deck_urls(override=generate_all_deck_urls)
            self.generate_deck_data_from_urls(override=generate_deck_data_from_urls)

    def load_my_data(self):
        for line in self.data_file.read().splitlines():
            self.my_data[self.deck_format][line[2:]] = int(line[0])

    def generate_all_deck_urls(self, override=False):
        FileDirectoryController().create_directory(f"Data/2.DeckURLS")
        if override or not FileDirectoryController().does_path_exist(f"Data/2.DeckURLS/{self.deck_format}.txt"):
            thread_controller = ThreadController(self.max_threads_1)
            thread_controller.start_load_wait(self.generate_all_deck_urls_thread)
            FileDirectoryController().write_array_to_file("Data/2.DeckURLS", f"{self.deck_format}.txt", self.deck_lists[self.deck_format])
        else:
            self.deck_lists[self.deck_format] = FileDirectoryController().read_array_from_file("Data/2.DeckURLS", f"{self.deck_format}.txt")

    def generate_all_deck_urls_thread(self, thread_id):
        website_controller = WebsiteController()
        for i in range(thread_id * 20, DeckFormat().return_list()[self.deck_format], self.max_threads_1 * 20):
            webpage = website_controller.return_webpage(DeckFormat().create_url(self.deck_format, offset=i), sleep=5)
            for deck in webpage.find_all("div", {"class": "deck-layout-single-flex"}):
                deck_url = f"https://ygoprodeck.com{deck.find('a')['href']}"
                if not deck_url in self.deck_lists[self.deck_format]:
                    print(deck_url)
                    self.deck_lists[self.deck_format].append(deck_url)

    def generate_deck_data_from_urls(self, override=False):
        FileDirectoryController().create_directory(f"Data/3.DeckData")
        if override or not FileDirectoryController().does_path_exist(f"Data/3.DeckData/{self.deck_format}.json"):
            if override:
                FileDirectoryController().delete_file("Data/3.DeckData", f"{self.deck_format}.json")
            thread_controller = ThreadController(self.max_threads_2)
            thread_controller.start_load_wait(self.generate_deck_data_from_urls_thread)
            JSONController().dump_dict_to_json("Data/3.DeckData", f"{self.deck_format}.json", self.deck_data[self.deck_format])
        else:
            self.deck_data[self.deck_format] = JSONController().load_json("Data/3.DeckData", f"{self.deck_format}.json")

    def generate_deck_data_from_urls_thread(self, thread_id):
        website_controller = WebsiteController()
        for i in range(thread_id, len(self.deck_lists[self.deck_format]), self.max_threads_2):
            webpage = website_controller.return_webpage(self.deck_lists[self.deck_format][i], sleep=2)
            self.deck_data[self.deck_format][DeckFormat().return_deck_name(self.deck_lists[self.deck_format][i])] = DeckFormat().create_deck_data(self.ygopro_controller, webpage)
            print(f"Decks Generated: {len(self.deck_data[self.deck_format])} / {len(self.deck_lists[self.deck_format])}")