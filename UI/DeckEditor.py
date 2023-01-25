from tkinter import Tk, PhotoImage, Label
from Controller.TkinterController import TkinterController
from Controller.FileAndDirectoryController import FileDirectoryController
from Controller.YgoproController import YgoproController
from Data.DeckFormat import DeckFormat
import math
import random
from Controller.VariableController import VariableController

class DeckEditor(Tk):
    def __init__(self, data_generator, height, width, title, background_color='#211717'):
        super().__init__()
        self.TkinterController = TkinterController()
        self.data_generator = data_generator
        self.number_per_page = 20
        self.card_search_numx = 4
        self.card_window_numx = 15
        self.current_page = 0
        self.current_user_data = {"main_deck": {}, "extra_deck": {}, "side_deck": {}}
        self.format_selection = None
        self.search_cards = self.data_generator.ygopro_controller.ygopro_data
        self.set_values(height, width, title, background_color)

    def set_values(self, height, width, title, background_color='#211717'):
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(width=False, height=False)
        self.TkinterController.place_image(self, "Background.png", 0, 0, size=(width, height))
        self.configure(bg=background_color)
        self.search_input = self.search_input = self.TkinterController.return_entry_field("Placeholder", (1200, 20), 20, 58, self.search_input_callback)
        self.TkinterController.add_dropdown(self, DeckFormat().return_list_as_list(), 1, 51, 1200, 760, self.deck_format_list_callback)
        self.format_selection = DeckFormat().return_list_as_list()[0]
        self.TkinterController.add_button(self, "Open Data File!", self.open_format_file, 1, 24, 1200, 803)
        self.TkinterController.add_button(self, "Complete From Files!", self.generate_deck_from_format, 1, 24, 1200, 832)
        self.TkinterController.add_button(self, "Clear Editor!", self.clear_editor, 1, 24, 1200, 860)
        self.update_gui()

    def update_gui(self):
        for widget in self.winfo_children():
            if not f"{widget}" == ".!label" and not f"{widget}" == ".!entry" and not f"{widget}" == ".!button" and not f"{widget}" == ".!button2" and not f"{widget}" == ".!button3":
                widget.destroy()

        if not (search_input := self.search_input.get()) == "":
            new_data = []
            for card in self.data_generator.ygopro_controller.ygopro_data:
                if search_input.lower() in card['name'].lower():
                    new_data.append(card)
            self.search_cards = new_data
        else:
            self.search_cards = self.data_generator.ygopro_controller.ygopro_data

        self.display_cards_in_search_area()

    def display_cards_in_search_area(self):
        count = 0

        for card_index in range(self.number_per_page * self.current_page, self.number_per_page * (self.current_page + 1)):
            if len(self.search_cards) > card_index:
                card = self.search_cards[card_index]
                mathx = int(count % self.card_search_numx)
                mathy = int(count / self.card_search_numx)
                posx = 1200 + (mathx * 88)
                posy = 60 + (mathy * 129) + (int(count / self.card_search_numx) * 12)
                self.TkinterController.place_image(self, f"Data/Ygodata/Images/{card['id']}.jpg", posx, posy, size=(88, 129))

                if card['type'] == "Fusion Monster" or card['type'] == "XYZ Monster" or card['type'] == "Synchro Monster" or card['type'] == "Link Monster":
                    self.TkinterController.add_card_button(self, "Extra Deck", self.add_card_to_deck, 1, 11, posx + 3, posy + 75, card, "extra_deck", 15)
                else:
                    self.TkinterController.add_card_button(self, "Main Deck", self.add_card_to_deck, 1, 11, posx + 3, posy + 75, card, "main_deck", 60)
                self.TkinterController.add_card_button(self, "Side Deck", self.add_card_to_deck, 1, 11, posx + 3, posy + 102, card, "side_deck", 15)

                count += 1

        count = 0
        x_count = 0
        scale = 0.775
        height = int(129 * scale)
        width = int(88 * scale)
        gap = 12 * scale

        for card_name in self.current_user_data['main_deck']:
            for i in range(0, self.current_user_data['main_deck'][card_name], 1):
                mathx = int(count % self.card_window_numx)
                mathy = int(count / self.card_window_numx)
                posx = 20 + (mathx * width) + (x_count * gap)
                posy = 20 + (mathy * height) + (int(count / self.card_window_numx) * gap)
                card = YgoproController(0).FindCardByName(card_name)
                self.TkinterController.place_image(self, f"Data/Ygodata/Images/{card['id']}.jpg", posx, posy, size=(width, height))
                count += 1
                x_count += 1
                if x_count >= self.card_window_numx:
                    x_count = 0

        count = 0
        x_count = 0

        for card_name in self.current_user_data['extra_deck']:
            for i in range(0, self.current_user_data['extra_deck'][card_name], 1):
                mathx = int(count % self.card_window_numx)
                mathy = int(count / self.card_window_numx)
                posx = 20 + (mathx * width) + (x_count * gap)
                posy = 525 + (mathy * height) + (int(count / self.card_window_numx) * gap)
                card = YgoproController(0).FindCardByName(card_name)
                self.TkinterController.place_image(self, f"Data/Ygodata/Images/{card['id']}.jpg", posx, posy, size=(width, height))
                count += 1
                x_count += 1
                if x_count >= self.card_window_numx:
                    x_count = 0

        count = 0
        x_count = 0

        for card_name in self.current_user_data['side_deck']:
            for i in range(0, self.current_user_data['side_deck'][card_name], 1):
                mathx = int(count % self.card_window_numx)
                mathy = int(count / self.card_window_numx)
                posx = 20 + (mathx * width) + (x_count * gap)
                posy = 675 + (mathy * height) + (int(count / self.card_window_numx) * gap)
                card = YgoproController(0).FindCardByName(card_name)
                self.TkinterController.place_image(self, f"Data/Ygodata/Images/{card['id']}.jpg", posx, posy, size=(width, height))
                count += 1
                x_count += 1
                if x_count >= self.card_window_numx:
                    x_count = 0

    def search_input_callback(self, var):
        self.update_gui()

    def deck_format_list_callback(self, var):
        self.format_selection = str(var.get())

    def add_card_to_deck(self, card, section, max_in_section):
        if len(self.current_user_data[section]) < max_in_section and self.count_copies(card, section) < 3:
            if not card['name'] in self.current_user_data[section]:
                self.current_user_data[section][card['name']] = 0
            self.current_user_data[section][card['name']] = self.current_user_data[section][card['name']] + 1
            print(self.current_user_data)
            self.update_gui()

    def count_copies(self, card, section):
        if not card['name'] in self.current_user_data[section]:
            return 0
        return self.current_user_data[section][card['name']]

    def open_format_file(self):
        FileDirectoryController().open_file("Data/1.MyData", f"{self.format_selection}.txt")

    def clear_editor(self):
        self.current_user_data = {"main_deck": {}, "extra_deck": {}, "side_deck": {}}
        self.update_gui()

    def generate_deck_from_format(self):
        my_data = self.data_generator.my_data[self.format_selection]
        for card in my_data:
            if my_data[card] > 3:
                my_data[card] = 3

        deck_data = self.data_generator.deck_data[self.format_selection]
        deck_scores = {}
        for deck_name in deck_data:
            total_score = 0

            all_cards_in_main_deck = True
            all_cards_in_extra_deck = True
            all_cards_in_side_deck = True

            for card_name in self.current_user_data['main_deck']:
                all_cards_in_main_deck = card_name in deck_data[deck_name]['main_deck']
                if not all_cards_in_main_deck:
                    break

            for card_name in self.current_user_data['side_deck']:
                all_cards_in_side_deck = card_name in deck_data[deck_name]['side_deck']
                if not all_cards_in_side_deck:
                    break

            for card_name in self.current_user_data['extra_deck']:
                all_cards_in_extra_deck = card_name in deck_data[deck_name]['extra_deck']
                if not all_cards_in_extra_deck:
                    break

            if not all_cards_in_main_deck or not all_cards_in_extra_deck or not all_cards_in_side_deck:
                continue

            for card in deck_data[deck_name]['main_deck']:
                target_amount = deck_data[deck_name]['main_deck'][card]
                our_amount = -100
                if card in my_data:
                    our_amount = my_data[card]
                total_score += target_amount - our_amount

            for card in deck_data[deck_name]['extra_deck']:
                target_amount = deck_data[deck_name]['extra_deck'][card]
                our_amount = -100
                if card in my_data:
                    our_amount = my_data[card]
                total_score += target_amount - our_amount

            for card in deck_data[deck_name]['side_deck']:
                target_amount = deck_data[deck_name]['side_deck'][card]
                our_amount = -100
                if card in my_data:
                    our_amount = my_data[card]
                total_score += target_amount - our_amount

            deck_scores[deck_name] = total_score

        if len(deck_scores) == 0:
            return

        lowest_score = VariableController().return_lowest_value_in_dict(deck_scores)
        lowest_keys = VariableController().return_all_keys_of_value(deck_scores, lowest_score)
        self.current_user_data = deck_data[random.choice(lowest_keys)]
        self.update_gui()
