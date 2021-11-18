import requests
from bs4 import BeautifulSoup
from enum import Enum, auto


url = "https://www.crous-bordeaux.fr/restaurant/resto-u-n1/"
data = None
menu_today = None
loud_mode = False


html_id = "menu-repas"
html_attrs = "content clearfix"
delimiter_food = "Plat chaud :"
delimiter_close = "Fermée"


class Chain(Enum):
    CLASSIC = auto()
    FISH = auto()
    FRIES = auto()
    TOURIST = auto()


class Menu:
    day:str
    classic:str = ""
    fish:str = ""
    fries:str = ""
    tourist:str = ""


def generate_menu():
    return menu_today


def update_data():
    global data
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    raw_menu = soup.find(id=html_id)
    data = raw_menu.find_all("li")


def handle_title(element, first_day):
    text_date = element.find("h3").contents[0]
    day = text_date.split(" ")[2]
    
    if first_day is True:
        first_day = False

    if first_day is None:
        global menu_today
        menu_today.day = text_date
        if loud_mode:
            print(f">>>> {text_date}")
        first_day = True
        
    return day, first_day


def add_menu_fragment(chain, fragment):
    global menu_today

    if chain is Chain.CLASSIC:
        menu_today.classic = menu_today.classic + fragment + "\n"

    elif chain is Chain.FRIES:
        menu_today.fries = menu_today.fries + fragment + "\n"

    elif chain is Chain.FISH:
        menu_today.fish = menu_today.fish + fragment + "\n"

    elif chain is Chain.TOURIST:
        menu_today.tourist = menu_today.tourist + fragment + "\n"


def handle_content(element, day, id, chain):

    text = element.contents[0]
    if day == "samedi":
        pass
        """
        if id >= 7 and len(text) != 86 and len(text) != 72 and delimiter_close != text:
            if delimiter_food == text:
                print(" ")
            print(text)
        """
        
    else:
        if id >= 9 and len(text) != 86:

            if delimiter_food == text:
                chain = next_chain(chain)
                # print(" ")
            else:
                add_menu_fragment(chain, text)
                if loud_mode:
                    print(">>", chain, text)

    return chain


# TODO  do better, like iterator ?
def next_chain(chain):
    if chain is None:
        return Chain.CLASSIC

    elif chain is Chain.CLASSIC:
        return Chain.FRIES

    elif chain is Chain.FRIES:
        return Chain.FISH

    elif chain is Chain.FISH:
        return Chain.TOURIST

    elif chain is Chain.TOURIST:
        return None


def process_data():
    global menu_today
    menu_today = Menu()
        
    first_day = None
    id = -1
    day = None
    chain = None

    for element in data:
        id += 1

        if first_day is False:
            break

        if len(element) == 5:
            day, first_day = handle_title(element, first_day)
            # chain = next_chain(chain)
            id = 0
            
        elif len(element) != 0:
            chain = handle_content(element, day, id, chain)


def is_missing_data():
    print("is_missing_data()", data)
    return data is None


def update_menu():
    update_data()
    process_data()


def get_menu():
    update_menu()
    return generate_menu()


if __name__ == '__main__':
    # update_data()
    # process_data()
    # print(" ")
    # print(vars(menu_today))
    pass
