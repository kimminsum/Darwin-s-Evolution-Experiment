import pygame
from pygame.locals import *
from time import*
from random import*

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
ERROR = 5
CELL_NO = 10
FOOD_NO = 10
MOVE_LIMIT = 3
food_w_av, food_h_av = 0, 0
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
cell_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()
all_group = pygame.sprite.Group()
clock = pygame.time.Clock()


def move(x, y, dst_x, dst_y, side_w, side_h, v, move_limit):
    if abs(x - dst_x) > ERROR and x <= dst_x:
        x += v
    elif abs(x - dst_x) > ERROR and x > dst_x:
        x -= v
    if abs(y - dst_y) > ERROR and y <= dst_y:
        y += v
    elif abs(y - dst_y) > ERROR and y > dst_y:
        y -= v

    if abs(x - dst_x) <= ERROR and abs(y - dst_y) <= ERROR:
        dst_x = randint(side_w, WINDOW_WIDTH - side_w)
        dst_y = randint(side_h, WINDOW_HEIGHT - side_h)
        move_limit -= 1
    return [x, y, dst_x, dst_y, move_limit]

def divid_cell(cell_hit, times):
    for hit in cell_hit:
        hit.move_limit = MOVE_LIMIT
        hit.collide += 1
        if hit.collide%times == 0 and hit.collide != 0:
            random_size_w = randint(-2,2)
            random_size_h = randint(-2,2)
            hit.side_w += random_size_w
            hit.side_h += random_size_h
            hit.rect.w += random_size_w
            hit.rect.h += random_size_h
            if hit.side_w < 3:
                hit.side_w = 3
                hit.rect.w = 3
            elif hit.side_h < 3:
                hit.side_h = 3
                hit.rect.h = 3
            hit.v += randint(-1,1)
            if hit.v <= 0:
                hit.v = 1
            cell = Cell(hit.rect.x, hit.rect.y, hit.side_w, hit.side_h, hit.v)
            cell_group.add(cell)
            all_group.add(cell)

def divid_food(seconds, millis):
    if seconds % 5 == 0 and millis <= 16:
        for food in food_group:
            random_size_w = randint(-2,2)
            random_size_h = randint(-2,2)
            food.side_w += random_size_w
            food.side_h += random_size_h
            food.rect.w += random_size_w
            food.rect.h += random_size_h
            if food.side_w < 3:
                food.side_w = 3
                food.rect.w = 3
            elif food.side_h < 3:
                food.side_h = 3
                food.rect.h = 3
            N_food = Food(food.rect.x, food.rect.y, food.side_w, food.side_h, 1)
            food_group.add(N_food)
            all_group.add(N_food)

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, side_w, side_h, v):
        super().__init__()
        self.x = x
        self.y = y
        self.v = v
        self.side_w = side_w
        self.side_h = side_h
        self.collide = 0
        self.move_limit = MOVE_LIMIT
        self.dst_x = randint(self.side_w, WINDOW_WIDTH - self.side_w)
        self.dst_y = randint(self.side_h, WINDOW_HEIGHT - self.side_h)
        self.color = pygame.Color("red")
        self.image = pygame.Surface((self.side_w, self.side_h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def update(self):
        if self.v >= 6:
            self.v = 6
        self.li = move(self.rect.x, self.rect.y, self.dst_x, self.dst_y, self.side_w, self.side_h, self.v, self.move_limit)
        self.rect.x = self.li[0]
        self.rect.y = self.li[1]
        self.dst_x = self.li[2]
        self.dst_y = self.li[3]
        self.move_limit = self.li[4]
        self.image = pygame.Surface((self.side_w, self.side_h), pygame.SRCALPHA)
        self.image.fill(self.color)


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, side_w, side_h, v):
        super().__init__()
        self.x = x
        self.y = y
        self.v = v
        self.side_w = side_w
        self.side_h = side_h
        self.collide = 0
        self.move_limit = MOVE_LIMIT
        self.dst_x = randint(self.side_w, WINDOW_WIDTH - self.side_w)
        self.dst_y = randint(self.side_h, WINDOW_HEIGHT - self.side_h)
        self.color = pygame.Color("blue")
        self.image = pygame.Surface((self.side_w, self.side_h), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def update(self):
        if self.v >= 8:
            self.v = 8
        self.li = move(self.rect.x, self.rect.y, self.dst_x, self.dst_y, self.side_w, self.side_h, self.v, 1)
        self.rect.x = self.li[0]
        self.rect.y = self.li[1]
        self.dst_x = self.li[2]
        self.dst_y = self.li[3]
        self.image = pygame.Surface((self.side_w, self.side_h), pygame.SRCALPHA)
        self.image.fill(self.color)


def main():
    pygame.init()
    pygame.display.set_caption("Evolution Simulation")
    food_w_av, food_h_av = 0, 0

    # add antity
    for i in range(CELL_NO):
        cell = Cell(randint(20, WINDOW_WIDTH - 20),
                    randint(20, WINDOW_HEIGHT - 20),
                    20, 20,
                    1)
        cell_group.add(cell)
        all_group.add(cell)

    for i in range(FOOD_NO):
        food = Food(randint(20, WINDOW_WIDTH - 20),
                    randint(20, WINDOW_HEIGHT - 20),
                    20, 20,
                    1)
        food_group.add(food)
        all_group.add(food)


    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        clock.tick(60)
        ticks = pygame.time.get_ticks()
        millis = ticks % 1000
        seconds = int(ticks/1000 % 60)
        if len(food_group) < 10:
            print("!!!LOW FOOD!!!")
            for food in food_group:
                food_w_av += food.rect.w
                food_h_av += food.rect.h
            food_w_av = round(food_w_av/len(food_group))
            food_h_av = round(food_h_av/len(food_group))

            for i in range(10):
                food = Food(randint(20, WINDOW_WIDTH - 20),
                            randint(20, WINDOW_HEIGHT - 20),
                            food_w_av, food_h_av,
                            1)
                food_group.add(food)
                all_group.add(food)
            food_w_av, food_h_av = 0, 0
        divid_food(seconds, millis)
        cell_hit = pygame.sprite.groupcollide(cell_group, food_group, False, True)
        divid_cell(cell_hit, 5)

        for cell in cell_group:
            if cell.move_limit == 0:
                cell.kill()

        SCREEN.fill(pygame.Color("gray"))
        all_group.draw(SCREEN)
        all_group.update()
        pygame.display.update()

if __name__=="__main__": main()
