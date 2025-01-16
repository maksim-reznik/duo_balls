# n, q = map(int, input().split())
# vt = [list(map(int, input().split())) for _ in range(n)]
# pq = [list(map(int, input().split())) for _ in range(q)]
# for i in range(q):
#     v = 0
#     t = 0
#     for j in vt:
#         x = 0
#         print(j, x, pq[i][0], x + j[1])
#
#         if x < pq[i][0] <= x + j[1] or x < pq[i][1] <= x + j[1]:
#
#             v += vt[i][0]
#             t += vt[i][1]
#         x += j[1]
#     print(v, t)
import random

from pygame import *
from random import *
from math import *
import numpy as np
from pygame import gfxdraw
from scipy.stats import alpha

score = 0
global lost
lost = 0

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def draw_transparent_circle(win, x, y, radius, color, alpha_level):
    gfxdraw.filled_circle(win, x, y, radius, (color[0], color[1], color[2], alpha_level))

def rotate_point(point, angle):
    #Поворачивает точку вокруг начала координат на заданный угол.
    x, y = point
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    return (x * cos_angle - y * sin_angle, x * sin_angle + y * cos_angle)

def get_rotated_corners(rect):
    # Возвращает координаты углов вращающегося прямоугольника.
    angle = rect.angle  # Угол поворота в радианах
    width, height = rect.width, rect.height
    center = (rect.x + width / 2, rect.y + height / 2)

    corners = [
        (-width / 2, -height / 2),
        (width / 2, -height / 2),
        (width / 2, height / 2),
        (-width / 2, height / 2)
    ]

    rotated_corners = [rotate_point(corner, angle) for corner in corners]
    return [(corner[0] + center[0], corner[1] + center[1]) for corner in rotated_corners]

def is_colliding(rect1, rect2):
    # Проверяет, пересекаются ли два вращающихся прямоугольника.
    corners1 = get_rotated_corners(rect1)
    corners2 = get_rotated_corners(rect2)

    # Проверяем оси для первого прямоугольника
    for i in range(4):
        # Вектор стороны
        edge = np.array(corners1[(i + 1) % 4]) - np.array(corners1[i])
        # Нормаль к стороне
        normal = np.array([-edge[1], edge[0]])

        # Проекция углов первого прямоугольника
        projections1 = [np.dot(normal, np.array(corner)) for corner in corners1]
        min1, max1 = min(projections1), max(projections1)

        # Проекция углов второго прямоугольника
        projections2 = [np.dot(normal, np.array(corner)) for corner in corners2]
        min2, max2 = min(projections2), max(projections2)

        # Проверка на пересечение
        if max1 < min2 or max2 < min1:
            return False  # Нет пересечения

    # Проверяем оси для второго прямоугольника
    for i in range(4):
        edge = np.array(corners2[(i + 1) % 4]) - np.array(corners2[i])
        normal = np.array([-edge[1], edge[0]])

        projections1 = [np.dot(normal, np.array(corner)) for corner in corners1]
        min1, max1 = min(projections1), max(projections1)

        projections2 = [np.dot(normal, np.array(corner)) for corner in corners2]
        min2, max2 = min(projections2), max(projections2)

        if max1 < min2 or max2 < min1:
            return False  # Нет пересечения

    return True  # Прямоугольники пересекаются


# Класс GameSprite
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y
        self.player_image = player_image
        self.image = transform.scale(image.load(player_image), (self.size_x, self.size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


    def rotate(self, angle):
        self.image = transform.rotate(image.load(self.player_image), angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def killl(self):
        global score
        score += 1
        self.kill()


class Particle(sprite.Sprite):
    def __init__(self, color, size, cord):
        super().__init__()
        self.color = color
        self.size = size
        self.cord = cord

    def update(self):
        draw.circle(window, self.color, self.cord, self.size)
        self.cord[1] += play_speed
        self.size -= play_speed /4


        if self.size <= 0:
            self.kill()


# Класс Player, унаследованный от GameSprite
class Player(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle_increment = 0.9 * play_speed
        self.angle = 0
        self.radius = 100
        self.sprites = [
            GameSprite("asteroid2.png", 0, 0, 20, 20, 0),
            GameSprite("asteroid2.png", 0, 0, 20, 20, 0)
        ]

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.angle -= self.angle_increment
        if keys[K_RIGHT]:
            self.angle += self.angle_increment

        [i.update() for i in particles]

    def draw(self):
        # Вычисление координат шаров
        x1 = 270 + self.radius * cos(radians(self.angle))
        y1 = 870 + self.radius * sin(radians(self.angle))
        x2 = 270 + self.radius * cos(radians(self.angle + 180))
        y2 = 870 + self.radius * sin(radians(self.angle + 180))

        self.sprites[0].rect.x = int(x1)
        self.sprites[0].rect.y = int(y1)
        self.sprites[1].rect.y = int(y2)
        self.sprites[1].rect.x = int(x2)

        # Рисование шаров
        draw.circle(window, RED, (int(x1), int(y1)), 20)
        draw.circle(window, BLUE, (int(x2), int(y2)), 20)

        blue_particle = Particle(BLUE, 20, [int(x2), int(y2)])
        red_particle = Particle(RED, 20, [int(x1), int(y1)])

        particles.append(blue_particle)
        particles.append(red_particle)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

class Enemy_Center(GameSprite):
    def __init__(self, player_x, player_y, size_x, size_y, player_speed):
        super().__init__("asteroid2.png", player_x, player_y, size_x, size_y, player_speed)
        self.angle = 0  # Начальный угол в радианах
        self.radius = 50  # Радиус вращения

    def update(self):
        # Обновление угла
        draw.rect(window, (255, 0, 0, 50), (self.rect.x, -10, 70, 1080))
        self.angle += np.radians(self.speed)  # Увеличиваем угол на скорость (в радианах)
        self.rect.y = int(self.rect.y + self.radius * np.sin(self.angle)) + play_speed/4  # Новая позиция по Y


    def draw(self):
        # Вычисление координатов углов вращающегося прямоугольника
        corners = self.get_rotated_corners()
        draw.polygon(window, RED, corners)  # Отрисовка прямоугольника

    def get_rotated_corners(self):
        # Возвращает координаты углов вращающегося прямоугольника
        angle_rad = radians(self.angle)
        half_width = self.size_x / 2
        half_height = self.size_y / 2
        center = (self.rect.x + half_width, self.rect.y + half_height)

        corners = [
            (-half_width, -half_height),
            (half_width, -half_height),
            (half_width, half_height),
            (-half_width, half_height)
        ]

        rotated_corners = [rotate_point(corner, angle_rad) for corner in corners]
        return [(corner[0] + center[0], corner[1] + center[1]) for corner in rotated_corners]

def show_game_over_screen(score):
    # Затемнение экрана
    overlay = Surface((win_width, win_height))
    overlay.fill((0, 0, 0))  # Черный цвет
    overlay.set_alpha(128)  # Уровень прозрачности (0-255)

    window.blit(overlay, (0, 0))  # Накладываем затемнение

    # Отображение счета
    lose_text = f'Счет: {score}'
    lose_surface = f1.render(lose_text, True, (255, 255, 255))
    window.blit(lose_surface, (win_width // 2 - lose_surface.get_width() // 2, win_height // 2 - 50))

    # Кнопка перезапуска
    restart_text = 'Нажмите ПРОБЕЛ для перезапуска'
    restart_surface = f1.render(restart_text, True, (255, 255, 255))
    window.blit(restart_surface, (win_width // 2 - restart_surface.get_width() // 2, win_height // 2 + 10))

    display.update()  # Обновление экрана


# Настройки музыки
mixer.init()
mixer.music.load('space.mp3')
# mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# Настройки окна
play_speed = 4
win_width = 540
win_height = 990
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'

font.init()
f1 = font.Font(None, 36)
f2 = font.Font(None, 50)
lose = f1.render('Счет: ' + str(score), 1, (255, 255, 255))

window = display.set_mode((win_width, win_height))
ship = Player()
display.set_caption("duo balls")
background = transform.scale(image.load(img_back), (540, 990))

bullets = sprite.Group()

# Группы
monsters = sprite.Group()
particles = []

n, m = 0, 0
finish = False
game = True
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
            break

    if not finish:
        window.blit(background, (0, 0))
        draw.circle(window, (128, 128, 128), (270, 870), 100, 1)
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        ship.update()
        ship.draw()
        ship.sprites[0].update()
        ship.sprites[1].update()
        lose = f1.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(lose, (5, 10))

        n += 1 + 1 * play_speed / 100
        if n >= 150:
            play_speed += 0.2
            n = 0
            c = randint(1, 6) if score >= 10 else randint(1, 4)
            m = c
            x = 'asteroid2.png'
            if c == 1:
                monster = Enemy(x, 220, 0, 100, 100, play_speed)
                monsters.add(monster)
            if c == 2:
                monster = Enemy(x, 408, 40, 130, 40, play_speed)
                monsters.add(monster)
                monster = Enemy(x, 0, 0, 290, 40, play_speed)
                monsters.add(monster)
            if c == 3:
                monster = Enemy(x, 0, 40, 130, 40, play_speed)
                monsters.add(monster)
                monster = Enemy(x, 260, 0, 290, 40, play_speed)
                monsters.add(monster)
            if c == 4:
                monster = Enemy(x, 120, 0, 100, 100, play_speed)
                monsters.add(monster)
                monster = Enemy(x, 310, 0, 100, 100, play_speed)
                monsters.add(monster)
            if c == 5:
                monster = Enemy_Center(350, -100, 70, 70, play_speed)
                monsters.add(monster)
                n = 60
            if c == 6:
                monster = Enemy_Center( 118, -100, 70, 70, play_speed)
                monsters.add(monster)
                n = 60

        for i in list(monsters):
            if sprite.collide_rect(i, ship.sprites[0]) or sprite.collide_rect(i, ship.sprites[1]):
                i.image = transform.scale(image.load('finish.jpg'), (i.size_x, i.size_y))
                i.reset()
                ship.update()

                finish = True
                status = False


        [i.killl() for i in monsters if i.rect.y >= 1000]

        for i in list(bullets):
            for j in list(monsters):
                if sprite.collide_rect(i, j):
                    i.kill()
                    j.rect.y = 0
                    j.rect.x = randint(50, 450)
                    score += 1

                    c = randint(1, 2)
                    if c == 1:
                        x = 'asteroid2.png'
                    else:
                        x = 'asteroid.png'
                    j.image = transform.scale(image.load(x), (j.size_x, j.size_y))
    else:
        # Если игра окончена, показываем экран проигрыша
        show_game_over_screen(score)

        # Ожидание нажатия клавиши для перезапуска
        keys = key.get_pressed()
        if keys[K_SPACE]:  # Если нажата клавиша R
            # Сброс всех переменных и объектов
            score = 0
            finish = False
            play_speed = 3.5
            monsters.empty()  # Очистка группы врагов
            bullets.empty()  # Очистка группы пуль
            ship = Player()  # Создание нового игрока
    # Обновление экрана и FPS
    display.update()
    clock.tick(FPS)
