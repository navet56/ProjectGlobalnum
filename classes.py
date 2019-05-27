import pygame
import copy
from pygame.locals import *
import variables

#Classes
class Joueur(pygame.sprite.Sprite):
    def __init__(self):#Constructeur
        super().__init__()
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
        bloc_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)#collisions
        
        #Les boucles suivantes permettent de bloquer les coordonnées du joueur aux coordonnées de blocs de collisions
        for bloc in bloc_hit_list:
            if self.change_x > 0:#pour toutes les blocs de collision, si il y a un deplacement du perso : la position droite du perso devient la position gauche du bloc (pour bloquer)
                self.rect.right = bloc.rect.left
            elif self.change_x < 0:#et inversement
                self.rect.left = bloc.rect.right
        self.rect.y += self.change_y
        bloc_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for bloc in bloc_hit_list:#pareil pour  le deplacement verticale
            if self.change_y > 0:
                self.rect.bottom = bloc.rect.top
            elif self.change_y < 0:
                self.rect.top = bloc.rect.bottom
            self.change_y = 0

    def grav(self):
        #Calcule la gravité
        if self.change_y == 0: #Si le sprite ne bouge plus
            self.change_y = 1 #Le faire bouger de 1 px
        else:
            self.change_y += .4 #sinon le faire bouger de 0.4 px

    def jump(self):
        #Permet le saut
        #Vérifie s'il y a une collision à 2 pixels au dessus
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        
        #Effectue le saut
        if len(platform_hit_list) > 0:#si on est sur une plateforme (si il y a collision entre le joueur et la platefroem): on saute
            sonjump.play()
            self.change_y = -14#-14 car les coordonnéés partent du haut, cela correspond à +14 dans un repère orthonormé classique

    def deplacement_gauche(self):
        self.change_x = -6 #on déplace le sprite de 6 pixels vers la gauche

    def deplacement_droit(self):
        self.change_x = 6#on déplace le sprite de 6 pixels vers la droite

    def stop(self):
        self.change_x = 0 #on force l'arret

class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("canette.png")
        self.rect = self.image.get_rect()
        self.tir = False
    def update(self):
        projectile_list.draw(ecran)
        if self.tir == True:
            if position=="Droite":
                self.rect.x += 6
            else:
                self.rect.x -= 6
        if self.rect.x > 600 or self.rect.x < 100:
            self.rect.y += 6
        if self.rect.y >= 720 or self.rect.x <= 0:
            self.rect.x = joueur.rect.x + 30
            self.rect.y = joueur.rect.y + 40
            self.tir = False

class EnemyMargot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("persopamargot.png")
        #self.rect = self.image.get_rect()
        self.rect = copy.deepcopy(defaultEnemyMargotPosition)
        self.level = None
        
class EnemyChat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("chat.png")
        #self.rect = self.image.get_rect()
        self.rect = copy.deepcopy(defaultEnemyChatPosition)
        self.level = None

class Plateforme(pygame.sprite.Sprite):
    def __init__(self, longueur, hauteur):
        super().__init__()
        self.image = pygame.Surface([longueur, hauteur])
        self.image.fill((255,100,50))#Couleur des plateformes (RVB)
        self.rect = self.image.get_rect()

class Level(object):#Classe Niveau en general
    def __init__(self, joueur):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.joueur = joueur
        self.monde_scrolling = 0#on définit le scrolling comme étant nul de base

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, ecran):
        ecran.blit(bg,(self.monde_scrolling // 1,0))
        self.platform_list.draw(ecran)
        self.enemy_list.draw(ecran)

    def scrolling(self, shift_x):#procédure scrolling 
        self.monde_scrolling += shift_x
        for platform in self.platform_list:#pour toutes les platformes
            platform.rect.x += shift_x#on les déplacent
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
    def resetScrolling(self):#permet de reset le scrolling
        for platform in self.platform_list:
            platform.rect.x -= self.monde_scrolling#permet de remettre les plateformes à leur position initiale
        for enemy in self.enemy_list:
            enemy.rect.x -= self.monde_scrolling#permet de remetre les ennemis à leur position initiale
        self.monde_scrolling = 0#on définit le scrolling du monde à 0
        
    def resetJeu(self): #permet de reset le jeu
        joueur.stop()#on stoppe l'avancer du perso
        current_level.resetScrolling()#on reset le scrolling
        joueur.rect = copy.deepcopy(defaultJoueurPosition)#on utilise copy.deepcopy car faire joueur.rect = defaultJoueurPosition ne fonctionne pas, il ne prend pas la valeur
        projectile.tir = False
        enemymargot.rect = copy.deepcopy(defaultEnemyMargotPosition)
        enemychat.rect = copy.deepcopy(defaultEnemyChatPosition)
        score = 0

class Level_01(Level): #Classe Level 1 qui prend comme base la classe Level
    def __init__(self, joueur):
        """ Creation du level 1. """
        super().__init__(joueur)#On ajout les variables du init de Level dans cet init
        self.level_limit = -1650

        level = [[100, 2, 20, 630],#plateformes du niveau
                 [100, 2, 250, 510],#[longueur, largeur, x, y]
                 [200, 2, 420, 338],
                 [580, 2, 780, 150],
                 [273, 2, 1, 100],
                 [150, 2, 1500, 615],
                 [400, 2, 1550, 375],
                 [400, 2, 2200, 625],
                 ]
        
        for platform in level:#pour toutes les plateformes dans la liste des plateformes du niveau
             bloc = Plateforme(platform[0], platform[1])#bloc est de longueur et largeur par exemple 100,30
             bloc.rect.x = platform[2]#la plateforme se situe en x = 400 par ex
             bloc.rect.y = platform[3]#pareil pour y
             bloc.joueur = self.joueur
             self.platform_list.add(bloc)#on ajoute bloc à la liste des plateformes 
