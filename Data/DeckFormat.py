
class DeckFormat:
    PROGRESSION_SERIES = "progression%20series"
    ANIME_DECKS = "anime%20decks"

    def create_url(self, format, offset=0):
        return f"https://ygoprodeck.com/category/format/{format}?&offset={offset}"

    def return_list(self):
        data = {}
        data[self.PROGRESSION_SERIES] = 540
        #data[self.ANIME_DECKS] = 2300
        return data

    def return_list_as_list(self):
        data = []
        data.append(self.PROGRESSION_SERIES)
        #data.append(self.ANIME_DECKS)
        return data

    def create_deck_data(self, ygopro_controller, webpage):
        deck_data = {"main_deck": {}, "extra_deck": {}, "side_deck": {}}
        for section in deck_data:
            div = webpage.find('div', {"id": section})
            if not div is None:
                for card in div.find_all("a", {"class": "ygodeckcard"}):
                    ygocard = ygopro_controller.FindCardIDNullCheck(card.find("img")['data-name'])
                    if not ygocard['name'] in deck_data[section]:
                        deck_data[section][ygocard['name']] = 0
                    deck_data[section][ygocard['name']] = deck_data[section][ygocard['name']] + 1
        return deck_data

    def return_deck_name(self, url):
        return url.replace("https://ygoprodeck.com/deck/", "Deck:")