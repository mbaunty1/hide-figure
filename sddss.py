import pygame
import sys
import random


class HideAndSeekGame:
    def __init__(self):
        pygame.init()
        # Налаштування екрану
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Хованки: 20 рівнів")
        # Ініціалізація шрифта
        self.font = pygame.font.Font(None, 36)
        # Доступні фігури
        self.shapes = ["square", "circle", "triangle", "star", "diamond"]
        self.colors = [(196, 98, 193), (199, 26, 78), (115, 217, 184), (183, 217, 115)]
        self.target_shape = None  # Фігура, яку вибрав гравець
        self.objects = []
        self.running = True
        self.clock = pygame.time.Clock()
        self.current_level = 1  # Поточний рівень
        self.max_levels = 20  # Максимальна кількість рівнів

    def choose_shape(self):
        """Екран вибору фігури"""
        waiting_for_choice = True
        while waiting_for_choice:
            self.screen.fill((255, 255, 255))
            # Показати текст
            text = self.font.render("Оберіть фігуру:", True, (0, 0, 0))
            self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, 50))
            # Розташувати фігури в один рядок
            start_x = 50
            spacing = (self.screen_width - 100) // len(self.shapes)
            for i, shape in enumerate(self.shapes):
                x = start_x + i * spacing
                y = 200
                self.draw_shape(shape, x, y, random.choice(self.colors))
                # Показати текст з назвою фігури
                label = self.font.render(shape, True, (0, 0, 0))
                self.screen.blit(label, (x + 10, y + 100))
            pygame.display.flip()
            # Обробка подій
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    for i, shape in enumerate(self.shapes):
                        x = start_x + i * spacing
                        y = 200
                        if self.is_shape_clicked(shape, pos, x, y):
                            self.target_shape = shape
                            waiting_for_choice = False

    def generate_objects(self):
        """Генерація об'єктів на екрані"""
        self.objects = []
        num_objects = 10 + self.current_level  # Зі зростанням рівня додається більше об'єктів
        for _ in range(num_objects):
            x = random.randint(0, self.screen_width - 50)
            y = random.randint(0, self.screen_height - 50)
            shape = random.choice(self.shapes)
            color = random.choice(self.colors)
            self.objects.append((shape, color, (x, y)))

    def run_game(self):
        """Основний цикл гри"""
        self.choose_shape()
        while self.running:
            self.generate_objects()
            level_running = True
            object_speed = max(30 - self.current_level, 5)  # Час оновлення положення об'єктів
            while level_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.check_click(event.pos)
                        level_running = False  # Вихід на наступний рівень після кліку
                self.move_objects()
                self.draw_objects()
                pygame.display.flip()
                self.clock.tick(object_speed)  # Складність залежить від швидкості руху

            # Перевірка завершення рівня
            if not self.running:
                break
            self.current_level += 1
            if self.current_level > self.max_levels:
                self.win()
        pygame.quit()
        sys.exit()

    def move_objects(self):
        """Рух об'єктів для ускладнення гри"""
        for i in range(len(self.objects)):
            shape, color, (x, y) = self.objects[i]
            dx = random.choice([-1, 1]) * random.randint(1, 5)  # Випадковий рух
            dy = random.choice([-1, 1]) * random.randint(1, 5)
            new_x = max(0, min(self.screen_width - 50, x + dx))
            new_y = max(0, min(self.screen_height - 50, y + dy))
            self.objects[i] = (shape, color, (new_x, new_y))

    def check_click(self, position):
        """Перевірка натискання на об'єкт"""
        for shape, color, pos in self.objects:
            x, y = pos
            if self.is_shape_clicked(shape, position, x, y):
                if shape == self.target_shape:
                    return  # Успішний вибір, продовжуємо до наступного рівня
                else:
                    self.game_over()
                    return

    def is_shape_clicked(self, shape, position, x, y):
        """Перевірка, чи була натиснута певна фігура"""
        if shape == "square":
            rect = pygame.Rect(x, y, 50, 50)
            return rect.collidepoint(position)
        elif shape == "circle":
            center = (x + 25, y + 25)
            return ((position[0] - center[0]) ** 2 + (position[1] - center[1]) ** 2) <= 25 ** 2
        elif shape == "triangle":
            points = [(x, y + 50), (x + 25, y), (x + 50, y + 50)]
            return self.point_in_polygon(position, points)
        elif shape == "star":
            return self.point_in_star(position, x, y)
        elif shape == "diamond":
            points = [(x, y + 25), (x + 25, y), (x + 50, y + 25), (x + 25, y + 50)]
            return self.point_in_polygon(position, points)
        return False

    def draw_objects(self):
        """Малювання об'єктів на екрані"""
        self.screen.fill((255, 255, 255))
        level_text = self.font.render(f"Рівень: {self.current_level}/{self.max_levels}", True, (0, 0, 0))
        self.screen.blit(level_text, (10, 10))
        for shape, color, pos in self.objects:
            x, y = pos
            self.draw_shape(shape, x, y, color)

    def draw_shape(self, shape, x, y, color):
        """Малювання однієї фігури"""
        if shape == "square":
            pygame.draw.rect(self.screen, color, (x, y, 50, 50))
        elif shape == "circle":
            pygame.draw.circle(self.screen, color, (x + 25, y + 25), 25)
        elif shape == "triangle":
            points = [(x, y + 50), (x + 25, y), (x + 50, y + 50)]
            pygame.draw.polygon(self.screen, color, points)
        elif shape == "star":
            self.draw_star(x, y, color)
        elif shape == "diamond":
            points = [(x, y + 25), (x + 25, y), (x + 50, y + 25), (x + 25, y + 50)]
            pygame.draw.polygon(self.screen, color, points)

    def game_over(self):
        """Кінець гри"""
        self.show_message("Game Over", (255, 0, 0))
        self.running = False

    def win(self):
        """Перемога"""
        self.show_message("Вітаємо! Ви пройшли всі 20 рівнів!", (0, 255, 0))

    def show_message(self, text, color):
        """Показати повідомлення"""
        self.screen.fill((255, 255, 255))
        message = self.font.render(text, True, color)
        self.screen.blit(message, (self.screen_width // 2 - message.get_width() // 2, self.screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    @staticmethod
    def point_in_polygon(point, polygon):
        """Перевірка, чи точка знаходиться всередині багатокутника"""
        x, y = point
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def draw_star(self, x, y, color):
        """Малювання зірки"""
        points = [
            (x + 25, y), (x + 31, y + 15), (x + 47, y + 15),
            (x + 34, y + 25), (x + 39, y + 40), (x + 25, y + 30),
            (x + 11, y + 40), (x + 16, y + 25), (x + 3, y + 15),
            (x + 19, y + 15)
        ]
        pygame.draw.polygon(self.screen, color, points)

    def point_in_star(self, point, x, y):
        """Перевірка, чи точка знаходиться всередині зірки"""
        points = [
            (x + 25, y), (x + 31, y + 15), (x + 47, y + 15),
            (x + 34, y + 25), (x + 39, y + 40), (x + 25, y + 30),
            (x + 11, y + 40), (x + 16, y + 25), (x + 3, y + 15),
            (x + 19, y + 15)
        ]
        return self.point_in_polygon(point, points)


if __name__ == "__main__":
    game = HideAndSeekGame()
    game.run_game()
