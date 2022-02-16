#!/usr/bin/env python3
from dataclasses import dataclass, field
import pygame.freetype
from typing import List
from pygame.locals import *
import random, pygame, os, sys
'''
'''
@dataclass(frozen=True)
class Colour:
    BLACK: tuple
    WHITE: tuple
    GREEN: tuple
    GREEN_1: tuple
    GREEN_2: tuple
    GREEN_3: tuple
    GREEN_4: tuple
    RED: tuple

@dataclass
class __:
    SC_WD: int
    SC_HT: int
    CELLSIZE: int
    FOODSIZE : int
    FOODBORDER: int
    error: int
    running: bool = True
    color_list: List[tuple] = field(default_factory=list)
    foods: List[int] = field(default_factory=list)
'''
'''
colour = Colour(BLACK=pygame.Color('grey12'),
                WHITE=(255,255,255),
                GREEN=(0,200,0),
                GREEN_1=(0,140,0),
                GREEN_2=(0,80,0),
                GREEN_3=(0,60,0),
                GREEN_4=(0,20,0),
                RED=(180,0,0))

_ = __(SC_WD=1400, # 1280
        SC_HT=800,
        CELLSIZE=10,
        FOODSIZE=10,
        FOODBORDER=120,
        error=5,
        color_list=[colour.GREEN_4,colour.GREEN_3,colour.GREEN_2,colour.GREEN_1,colour.GREEN])
SCREEN = pygame.display.set_mode((_.SC_WD, _.SC_HT))
'''
'''
class Cell(pygame.sprite.Sprite):
    def __init__(self, color, x, y, ran, radius, v):
        super().__init__()
        self.ran = ran
        if self.ran < 0.25: # top
            self.x = random.randint(_.CELLSIZE*2, _.SC_WD - _.CELLSIZE*2)
            self.y = random.randint(_.CELLSIZE*2, 100)
        elif self.ran < 0.5: # bottom
            self.x = random.randint(_.CELLSIZE*2, _.SC_WD - _.CELLSIZE*2)
            self.y = random.randint(_.SC_HT - 100, _.SC_HT - _.CELLSIZE*2)
        elif self.ran < 0.75: # right
            self.x = random.randint(_.SC_WD - 100, _.SC_WD - _.CELLSIZE*2)
            self.y = random.randint(_.CELLSIZE*2, _.SC_HT - _.CELLSIZE*2)
        elif self.ran == 2:
            self.x = x
            self.y = y
        else: # left
            self.x = random.randint(_.CELLSIZE*2, 100)
            self.y = random.randint(_.CELLSIZE*2, _.SC_HT - _.CELLSIZE)

        self.ran_x = random.randint(_.CELLSIZE*2, _.SC_WD-_.CELLSIZE)
        self.ran_y = random.randint(_.CELLSIZE*2, _.SC_HT-_.CELLSIZE)
        self.color = color
        self.radius = radius
        self.v = v
        self.error = _.error
        self.divid = 0
        self.timer = 5
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def update(self):
        '''
        set destination
        '''
        if abs(self.rect.x - self.ran_x) > self.error and self.rect.x <= self.ran_x:
            self.rect.x += self.v
        elif abs(self.rect.x - self.ran_x) > self.error and self.rect.x > self.ran_x:
            self.rect.x -= self.v
        if abs(self.rect.y - self.ran_y) > self.error and self.rect.y <= self.ran_y:
            self.rect.y += self.v
        elif abs(self.rect.y - self.ran_y) > self.error and self.rect.y > self.ran_y:
            self.rect.y -= self.v

        if abs(self.rect.x - self.ran_x) <= self.error and abs(self.rect.y - self.ran_y) <= self.error:
            self.ran_x = random.randint(_.CELLSIZE *2, _.SC_WD-_.CELLSIZE *2)
            self.ran_y = random.randint(_.CELLSIZE *2, _.SC_HT-_.CELLSIZE *2)
            self.timer -= 1
        '''
        color change
        '''
        self.color = _.color_list[self.timer-1]
        self.image = pygame.Surface((self.radius *2, self.radius *2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((_.FOODSIZE,_.FOODSIZE))
        self.image.fill(colour.RED)
        x = random.randint(_.FOODBORDER, _.SC_WD-_.FOODBORDER)
        y = random.randrange (_.FOODBORDER, _.SC_HT-_.FOODBORDER)
        self.rect = self.image.get_rect(center = (x, y))
'''
'''
def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Game')
    font=pygame.freetype.SysFont(None, 30)
    font.origin=True
    cell_group = pygame.sprite.Group()
    food_group = pygame.sprite.Group()
    all_antity = pygame.sprite.Group()
    '''
    '''
    for i in range(10):
        cell = Cell(colour.GREEN, 0, 0, random.random(), _.CELLSIZE, 2)
        cell_group.add(cell)
        all_antity.add(cell)
    for i in range(40):
        food = Food()
        food_group.add(food)
        all_antity.add(food)
    '''
    '''
    while _.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _.running = False
        '''
        timer
        '''
        clock.tick(60)
        ticks=pygame.time.get_ticks()
        millis=ticks%1000
        seconds=int(ticks/1000 % 60)
        minutes=int(ticks/60000 % 24)
        if seconds %10 == 0 and millis <= 16: # add more foods per 10secs
            for i in range(40): ##########
                food = Food()
                food_group.add(food)
                all_antity.add(food)

        hit_list = pygame.sprite.groupcollide(cell_group, food_group, False, True)
        for block in hit_list:
            block.divid += 1
            block.timer = 5
            '''
            divid account
            '''
            if block.divid%10 == 0 and block.divid != 0:
                if block.v >= 8:
                    block.v = 8
                '''
                evolve
                '''
                block.v += random.randint(-2, 2)
                if block.v <= 1:
                    block.v = 1
                delta = random.randint(-5, 5)
                block.rect.w += delta *2
                block.rect.h += delta *2
                block.radius += delta
                if block.radius < 2:
                    block.radius = 2
                cell = Cell(colour.GREEN, block.rect.x, block.rect.y, 2, block.radius, block.v)
                cell_group.add(cell)
                all_antity.add(cell)

        for cell in cell_group:
            if cell.timer == 0:
                cell.kill()
        SCREEN.fill(colour.BLACK)
        all_antity.draw(SCREEN)
        out='{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
        font.render_to(SCREEN, (20, 40), out, pygame.Color('dodgerblue'))
        all_antity.update()
        pygame.display.update()

    pygame.quit()
'''
'''
if __name__ == '__main__': 
    main()
