import random
import math
import pygame

class Snowflake:
    def __init__(self, window_size):
        """
        Ініціалізує об'єкт сніжинки з розміром вікна.

        :param window_size: Розмір вікна (ширина, висота)
        """
        self.window_size = window_size
        self.snowflakes = self.generate_snowflakes()

    def generate_snowflakes(self):
        """
        Генерує список сніжинок з випадковими параметрами.

        :return: Список сніжинок
        """
        snowflakes = []
        for _ in range(100):
            x = random.randint(0, self.window_size[0])
            y = random.randint(0, self.window_size[1])
            speed = random.uniform(0.5, 1.5)
            wobble = random.uniform(0.1, 0.3)
            size = random.randint(2, 5)
            snowflakes.append([x, y, speed, wobble, size])
        return snowflakes

    def update_and_draw(self, screen, time):
        """
        Оновлює положення сніжинок та малює їх на екрані.

        :param screen: Екран для малювання
        :param time: Поточний час для обчислення коливань
        """
        for i, (x, y, speed, wobble, size) in enumerate(self.snowflakes):
            y += speed
            x += math.sin(time * wobble) * 0.5
            if y > self.window_size[1]:
                y = random.randint(-50, 0)
                x = random.randint(0, self.window_size[0])
            color = (255, 255, 255, 200)
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (int(size / 2), int(size / 2)), int(size / 2))
            screen.blit(surf, (int(x), int(y)))
            self.snowflakes[i] = [x, y, speed, wobble, size]