from Menus.First_Menu import First_Menu
from Other.Other_Functions import file_read

if __name__ == '__main__':
    file_read()
    menu = First_Menu()
    menu.run()