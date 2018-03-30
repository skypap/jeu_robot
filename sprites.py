# Class sprites
import pygame as pg
from settings import *
import random

import math


def deg2rad(angle):
    return angle*2*math.pi/360


class Pivot(pg.sprite.Sprite):
    def __init__(self, img_pivot):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(img_pivot, (100, 100))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (REP_FIXE[0] + 5, REP_FIXE[1] - 10)


class Obstacles(pg.sprite.Sprite):
        def __init__(self, x, y, w, h, mobile = False):
            pg.sprite.Sprite.__init__(self)
            self.temp = True
            self.w = w
            self.mobile = mobile
            self.image = pg.Surface((w, h))
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            if mobile:
                self.speedy = 0
                self.speedx = 10
            else:
                self.speedy = 0
                self.speedx = 0

        def update(self):
            temp = self.temp
            if self.rect.x < WIDTH and temp:
                self.rect.y += 0
                self.rect.x += self.speedx
            if self.rect.x >= WIDTH and temp:
                self.temp = False
            if (temp == False):
                self.rect.y += 0
                self.rect.x -= self.speedx
            if self.rect.x <= 0:
                self.temp = True

                # if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                #     self.rect.x = random.randrange(WIDTH - self.rect.width)
                #     self.rect.y = random.randrange(-100, -40)
                #     self.speedy = random.randrange(1, 8)


class Goal(pg.sprite.Sprite):
        def __init__(self, x, y, w, h):
            pg.sprite.Sprite.__init__(self)
            self.image = pg.Surface((w, h))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y


class ArmRR(pg.sprite.Sprite):
    def __init__(self, l1=200, l2=200):
        pg.sprite.Sprite.__init__(self)
        self.l1 = l1
        self.l2 = l2
        self.t1 = math.pi/6
        self.t2 = 5*math.pi/6
        self.eff = self.pgd(self.l1, self.l2, self.t1, self.t2)
        self.image = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.draw(self.l1, self.l2, self.t1, self.t2)

    def draw(self, l1, l2, t1, t2):
        self.eff = self.pgd(l1, l2, t1, t2)
        return pg.draw.lines(self.image, BLACK, False,
                            [[REP_FIXE[0], REP_FIXE[1]],
                             [REP_FIXE[0]+l1*math.cos(t1),
                              REP_FIXE[1] - l1*math.sin(t1)],
                             [self.eff[0], self.eff[1]]], 10)

    def pgd(self, l1, l2, t1, t2):
        return [REP_FIXE[0]+l1*math.cos(t1) + l2*math.cos(t1+t2),
                REP_FIXE[1]-l1*math.sin(t1) - l2*math.sin(t1+t2)]

    def update(self):
        self.speedt1 = 0
        self.speedt2 = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_z]:
            # self.game.art_sound.play()
            self.speedt1 = -deg2rad(1)
        if keystate[pg.K_a]:
            self.speedt1 = deg2rad(1)
        if keystate[pg.K_x]:
            self.speedt2 = -deg2rad(1)
        if keystate[pg.K_s]:
            self.speedt2 = deg2rad(1)
        self.t1 += self.speedt1
        self.t2 += self.speedt2
        self.image = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.draw(self.l1, self.l2, self.t1, self.t2)


class Effecteur(pg.sprite.Sprite):
        def __init__(self, l1=200 ,l2=200):
            pg.sprite.Sprite.__init__(self)
            # super(Effecteur, self).__init__(eff)
            self.eff_rob = ArmRR(l1,l2)
            self.eff = self.eff_rob.eff
            self.image = pg.Surface((60, 60))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.center = (self.eff[0], self.eff[1])

        def update(self):
            self.eff_rob.update()
            self.eff = self.eff_rob.eff
            self.image = pg.Surface((60, 60))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.center = (self.eff[0], self.eff[1])
