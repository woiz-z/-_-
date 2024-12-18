import random
import re

from Configs import Configs as con


def generate_random_color():
    """
    Генерує випадковий колір.

    Повертає:
        tuple: Кортеж з трьох значень (R, G, B), кожне з яких є випадковим числом від 0 до 255.
    """
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def file_write():
    """
    Записує конфігураційні налаштування у файл.

    Файл:
        config_file: Файл, у який записуються налаштування.
    """
    with open('./Configs/config_file', 'w+') as file:
        file.write(f"volume = {con.volume}\n")
        file.write(f"resolution_index = {con.resolution_index}\n")
        file.write(f"fullscreen = {con.fullscreen}\n")

def file_read():
    """
    Зчитує конфігураційні налаштування з файлу та встановлює їх у конфігурації.
    """
    with open('./Configs/config_file', 'r') as file:
        lines = file.readlines()
        for line in lines:
            match = re.match(r"(\w+) = ([\w.]+)", line)
            if match:
                key, value = match.groups()
                if key == "volume":
                    setattr(con, key, float(value))
                else:
                    try:
                        setattr(con, key, int(value))
                    except ValueError:
                        setattr(con, key, value)