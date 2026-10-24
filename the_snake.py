"""Игра «Змейка» на pygame.

Модуль содержит классы игровых объектов и основной игровой цикл.
"""
from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центр экрана — глобальная константа, чтобы не дублировать:
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self, body_color=(255, 255, 255)):
        """Инициализирует объект в центре поля.

        :param body_color: цвет объекта в формате RGB.
        """
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw_cell(self, position, color):
        """Рисует одну клетку поля по координатам.

        :param position: координаты левого верхнего угла клетки.
        :param color: цвет заливки клетки.
        """
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовывает объект. Переопределяется в наследниках."""


class Apple(GameObject):
    """Яблоко — игровой объект, который съедает змейка."""

    def __init__(self, occupied_positions=None):
        """Создаёт яблоко в случайной свободной клетке поля.

        :param occupied_positions: занятые клетки,
        куда яблоко не должно попасть.
        """
        super().__init__(APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=None):
        """Перемещает яблоко в случайную клетку, свободную от змейки.

        :param occupied_positions: занятые клетки,
        куда яблоко не должно попасть.
        """
        occupied = set(occupied_positions or ())
        free_cells = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x * GRID_SIZE, y * GRID_SIZE) not in occupied
        ]
        # Если свободных клеток нет — оставляем яблоко на месте:
        if free_cells:
            self.position = choice(free_cells)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Змейка — основной управляемый объект игры."""

    def __init__(self):
        """Создаёт змейку и приводит её в начальное состояние."""
        super().__init__(SNAKE_COLOR)
        self.reset()

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Применяет новое направление, выбранное игроком."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку на одну клетку в текущем направлении."""
        self.update_direction()

        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        step_x = dx * GRID_SIZE
        step_y = dy * GRID_SIZE

        new_x = (head_x + step_x) % SCREEN_WIDTH
        new_y = (head_y + step_y) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)
        self.position = new_head

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.position = SCREEN_CENTER
        self.positions = [SCREEN_CENTER]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def draw(self):
        """Отрисовывает змейку и затирает старый хвост."""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        for position in self.positions:
            self.draw_cell(position, self.body_color)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш и закрытие окна.

    :param game_object: змейка, которой управляет игрок.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запускает основной игровой цикл."""
    pygame.init()

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        head = snake.get_head_position()

        if head == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif head in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
