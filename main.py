#coding:utf-8
import pygame
from pygame.locals import *

VERT = (0,255,0)
BLANC = (255,255,255)
NOIR = (0,0,0)
BLEU = (0,0,255)
ROUGE = (255, 0, 0)
ECRAN_LONGUEUR = 1280
ECRAN_HAUTEUR = 720
bg = pygame.image.load("background.png")
pygame.mixer.init(44100, -16,2,2048)
sonjump = pygame.mixer.Sound("jump.ogg")
class Joueur(pygame.sprite.Sprite):
    def __init__(self):#Constructeur
        super().__init__() #Appelle le constructeur de la classe mère
        longueur = 60
        hauteur = 100
        self.image = pygame.image.load("persocorentin.png")
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.level = None
 
    def update(self):
        #Met à jour le joueur
        self.grav()
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
 
    def grav(self):
        #Calcule la gravité
        if self.change_y == 0: #Si le sprite ne bouge plus
            self.change_y = 1 #Le faire bouger de 1 px
        else:
            self.change_y += .35 #sinon le faire bouger de 0.35 px
        if self.rect.y >= ECRAN_HAUTEUR - self.rect.height and self.change_y >= 0: #Si le sprite est en bas de l'ecran moins la hauteur du sprite car sinon ce serait en dessous
            self.change_y = 0 #on stoppe le sprite
            self.rect.y = ECRAN_HAUTEUR - self.rect.height #on met le sprite tout en bas
 
    def jump(self):
        #Permet le saut

        #Vérifie s'il y a une collision à 2 pixels au dessus
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        #Effectue le saut
        if len(platform_hit_list) > 0 or self.rect.bottom >= ECRAN_HAUTEUR:
            self.change_y = -10

    def go_left(self):
        self.change_x = -6 #on déplace le sprite de 6 pixels
 
    def go_right(self):
        self.change_x = 6#on déplace le sprite de 6 pixels
 
    def stop(self):
        self.change_x = 0 #on force l'arret
 
class Platform(pygame.sprite.Sprite):
    def __init__(self, longueur, hauteur):
        super().__init__()
        self.image = pygame.Surface([longueur, hauteur])
        self.image.fill(VERT)#a modifier
        self.rect = self.image.get_rect()

class Level(object):#Classe Niveau en general
    def __init__(self, joueur):

        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.joueur = joueur
        self.background = None
    def update(self):
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, ecran):
        self.platform_list.draw(ecran)
        self.enemy_list.draw(ecran)

class Level_01(Level): #Classe Level 1 qui prend comme base la classe Level

    def __init__(self, joueur):
        """ Creattion du level 1. """
        super().__init__(joueur)#On ajout les variables du init de Level dans cet init
 
        level = [[210, 70, 500, 500], #plateformes du niveau
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 [350, 400, 700, 700],
                 [210, 70, 500, 500],
                 [710, 70, 500, 400],
                 [710, 70, 600, 300],
                 [350, 70, 0, 0],
                 ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.joueur = self.joueur
            self.platform_list.add(block)

#Boucle principale
pygame.init()
ecran = pygame.display.set_mode([ECRAN_LONGUEUR, ECRAN_HAUTEUR])
pygame.display.set_caption("Global Num")
joueur = Joueur()
level_list = []
level_list.append( Level_01(joueur) )
current_level_no = 0
current_level = level_list[current_level_no]
active_sprite_list = pygame.sprite.Group()
joueur.rect.x = 340
joueur.rect.y = ECRAN_HAUTEUR - joueur.rect.height
joueur.level = current_level
active_sprite_list.add(joueur)
done = False
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:#Si une touche est préssée
            if event.key == pygame.K_LEFT:#La touche fleche gauche :
                joueur.go_left()
            if event.key == pygame.K_RIGHT:#etc
                joueur.go_right()
            if event.key == pygame.K_UP:
                sonjump.play()
                joueur.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and joueur.change_x < 0:
                joueur.stop()
                sonjump.stop()
            if event.key == pygame.K_RIGHT and joueur.change_x > 0:
                joueur.stop()
    active_sprite_list.update()
    current_level.update()
    if joueur.rect.right > ECRAN_LONGUEUR:
        joueur.rect.right = ECRAN_LONGUEUR
    if joueur.rect.left < 0:
        joueur.rect.left = 0
    ecran.blit(bg, (0, 0))
    current_level.draw(ecran)
    active_sprite_list.draw(ecran)
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
