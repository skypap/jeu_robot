# Project setup

import pygame as pg
import random
from settings import *
from sprites import *
from os import path


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.level = LEVEL
        self.score = 0
        self.start_ticks = pg.time.get_ticks()
        self.next_level = False
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        background = pg.image.load(path.join(img_dir, "background.jpg")).convert()
        img_go = pg.image.load(path.join(img_dir, "game_over.jpg")).convert()
        self.img_pivot = pg.image.load(path.join(img_dir, "pivot.png")).convert()
        self.background = pg.transform.scale(background, (WIDTH, HEIGHT))
        self.img_go = pg.transform.scale(img_go, (WIDTH, HEIGHT))
        # load trame sonore
        self.snd_dir = path.join(self.dir, 'snd')
        self.go_sound = pg.mixer.Sound(path.join(self.snd_dir, 'game_over.ogg'))
        self.art_sound = pg.mixer.Sound(path.join(self.snd_dir, 'click.wav'))
        self.imp_sound = pg.mixer.Sound(path.join(self.snd_dir, 'impact.aif'))
        self.goal_sound = pg.mixer.Sound(path.join(self.snd_dir, 'you_win.ogg'))
    #     with open(path.join(self.dir, HS_FILE), 'r') as f:
    #         try:
    #             self.highscore = int(f.read())
    #         except:
    #             self.highscore = 0

    def new(self):
        # start a new game
        self.level1()
        pg.mixer.music.load(path.join(self.snd_dir, 'Sax_Guy.ogg'))
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1) #joue infini
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            self.sel_level()
        pg.mixer.music.fadeout(500)

    def sel_level(self):
        if((self.level == 2) and (self.next_level == True)):
            for sprite in self.all_sprites:
                sprite.kill()
            self.next_level = False
            self.score += self.score_temp
            self.level2()

        if((self.level == 3) and (self.next_level == True)):
            for sprite in self.all_sprites:
                sprite.kill()
            self.next_level = False
            self.score += self.score_temp
            self.level3()

    def update(self):
        # Game Loop - Update
        self.calcul_score()
        self.all_sprites.update()
        # TODO mettre collision ds les sprites
        obs_hits = pg.sprite.spritecollide(self.eff, self.obstacles, False)
        goal_hits = pg.sprite.spritecollide(self.eff, self.goals, False)
        if obs_hits:
            # self.imp_sound.play()# trop de delay
            # recommence
            for sprite in self.all_sprites:
                sprite.kill()
            self.playing = False

        if goal_hits:
            pg.time.wait(1000) # a effacer qd les collision seront ds les classes
            self.goal_sound.play()
            self.next_level = True
            self.level += 1
            if self.level == NB_LEVEL+1:
                for sprite in self.all_sprites:
                    sprite.kill()
            self.playing = False


    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score_temp), 22, BLUE, WIDTH / 2, 15)
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Office.ogg'))
        pg.mixer.music.play(loops=-1)  # joue infini
        self.screen.blit(self.background, (0, 0))
        self.draw_text(TITLE, 48, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Controlle:", 22, BLACK, 50, HEIGHT / 2)
        self.draw_text("Articulation 1 -> 'A' : horaire, 'Z' : anti-horaire ", 22, BLACK, WIDTH / 2, HEIGHT / 2+30)
        self.draw_text("Articulation 2 -> 'S' : horaire, 'X' : anti-horaire ", 22, BLACK, WIDTH / 2, HEIGHT / 2+60)
        self.draw_text("Appuyez sur une touche pour commencer", 22, BLACK, WIDTH / 2, HEIGHT * 3.5 / 4)
        # self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        self.screen.blit(self.img_go, (0, 0))
        if not self.running:
            return  # Ferme le jeu qd on click sur x sans passer par GO

        def texte_fin(couleur):
            self.draw_text("Vous avez obtenue :" + str(self.score)+" points", 22, couleur, WIDTH / 2, HEIGHT / 2)
            self.draw_text("Appuyez sur une touche pour commencer", 22, couleur, WIDTH / 2, HEIGHT * 3 / 4)

        if self.level > NB_LEVEL:
            self.score += self.score_temp
            self.draw_text("Bravo", 48, WHITE, WIDTH / 2, HEIGHT / 4)
            texte_fin(WHITE)
        else:
            self.go_sound.play()
            self.draw_text("GAME OVER", 48, RED, WIDTH / 2, HEIGHT / 4)
            texte_fin(RED)

        # if self.score > self.highscore:
        #     self.highscore = self.score
        #     self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        #     with open(path.join(self.dir, HS_FILE), 'w') as f:
        #         f.write(str(self.score))
        # else:
        #     self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        self.level = 1
        self.score = 0
        pg.display.flip()
        self.wait_for_key()

    # def end_screen(self):
    #     self.screen.fill(BLUE)
    #     if not self.running:
    #         return  # Ferme le jeu qd on click sur x sans passer par GO
    #     self.draw_text("Bravo", 48, WHITE, WIDTH / 2, HEIGHT / 4)
    #     self.draw_text("Vous avez obtenue :" + str(self.score)+" points", 22, WHITE, WIDTH / 2, HEIGHT / 2)
    #     self.draw_text("Appuyez sur une touche pour commencer", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
    #     pg.display.flip()
    #
    #     self.wait_for_key()
    #     self.new()

    def calcul_score(self):
        delay = (pg.time.get_ticks()-self.start_ticks)/1000
        tau = 50  # constante de temps
        if(delay > 0.5):
            self.score_temp = int(SCORE*math.exp(-delay/tau))

    def inter_level_screen(self):
        pass

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

# mettre le design des level ds un fichier json
    def level1(self):
        self.score_temp = SCORE
        self.start_ticks = pg.time.get_ticks()

        self.all_sprites = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.goals = pg.sprite.Group()
        self.robot = ArmRR()
        self.eff = Effecteur()
        self.pivot = Pivot(self.img_pivot)
        goal1 = Goal(250, 150, 200, 50)
        # self.all_sprites.add(self.robot, self.pivot, self.eff)
        obs1 = Obstacles(0, 200, 450, 50)
        obs2 = Obstacles(WIDTH-50, 200, 50, 50)
        self.all_sprites.add(goal1)
        self.all_sprites.add(obs1, obs2)
        self.all_sprites.add(self.robot, self.pivot, self.eff)
        self.obstacles.add(obs1, obs2)
        self.goals.add(goal1)
        self.robot.update()
        self.eff.update()


    def level2(self):
        self.start_ticks = pg.time.get_ticks()
        self.score_temp = SCORE
        self.all_sprites = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.goals = pg.sprite.Group()
        self.robot = ArmRR(l1=200,l2=130)
        self.eff = Effecteur(l1=200,l2=130)
        self.pivot = Pivot(self.img_pivot)
        goal1 = Goal(WIDTH-150, 100, 200, 50)
        # self.all_sprites.add(self.robot, self.pivot, self.eff)
        obs1 = Obstacles(50, 200, 200, 50, True)
        self.all_sprites.add(goal1)
        self.all_sprites.add(obs1)
        self.all_sprites.add(self.robot, self.pivot, self.eff)
        self.obstacles.add(obs1)
        self.goals.add(goal1)
        self.obstacles.update()
        self.robot.update()
        self.eff.update()
        self.run()

    def level3(self):
        self.start_ticks = pg.time.get_ticks()
        self.score_temp = SCORE
        self.all_sprites = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.goals = pg.sprite.Group()
        self.robot = ArmRR()
        self.eff = Effecteur()
        self.pivot = Pivot(self.img_pivot)
        goal1 = Goal(250, 200, 50, 50)
        # self.all_sprites.add(self.robot, self.pivot, self.eff)
        obs1 = Obstacles(400, 300, 50, 50)
        obs2 = Obstacles(350, 250, 50, 50)
        obs3 = Obstacles(200, 200, 50, 50)
        obs4 = Obstacles(100, 100, 50, 50)
        self.all_sprites.add(goal1)
        self.all_sprites.add(obs1, obs2, obs3, obs4)
        self.all_sprites.add(self.robot, self.pivot, self.eff)
        self.obstacles.add(obs1, obs2, obs3, obs4)
        self.goals.add(goal1)
        self.robot.update()
        self.eff.update()
        self.run()


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    # if(g.level > NB_LEVEL):
    #     g.running = True
    g.show_go_screen()

pg.quit()
