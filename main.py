#coding:utf-8

#    Je veux rentrer !
#    Programme sous license GPL v3
#    Python 3
#    Pygame 1.9
#    Par :
#    Mael Le Boulicaut et Evan Diberder
#    v0.5 

import pygame
from pygame.locals import *

#Constantes
ECRAN_LONGUEUR = 1280
ECRAN_HAUTEUR = 720
bgcredit = pygame.image.load("bkgcredits.png")
pygame.mixer.init(44100, -16,2,2048)#on initialise mixer (frequence du son, nombre de bits, etc)
musique = pygame.mixer.music.load("menu.ogg")
sonjump = pygame.mixer.Sound("jump.ogg")
perso = pygame.image.load("persomenu1.png")
fondmenu = pygame.image.load("bkgmenu.png")

#Classes
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
        bloc_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for bloc in bloc_hit_list:
            if self.change_x > 0:
                self.rect.right = bloc.rect.left
            elif self.change_x < 0:
                self.rect.left = bloc.rect.right
        self.rect.y += self.change_y
        bloc_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for bloc in bloc_hit_list:
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
            sonjump.play()
            self.change_y = -10#-10 car les coordonnéés partent du haut, cela correspond à +10 dans un repère orthonormé classique

    def deplacement_gauche(self):
        self.change_x = -6 #on déplace le sprite de 6 pixels
 
    def deplacement_droit(self):
        self.change_x = 6#on déplace le sprite de 6 pixels
 
    def stop(self):
        self.change_x = 0 #on force l'arret
 
class Platform(pygame.sprite.Sprite):
    def __init__(self, longueur, hauteur):
        super().__init__()
        self.image = pygame.Surface([longueur, hauteur])
        self.image.fill((0,100,50))
        self.rect = self.image.get_rect()

class Level(object):#Classe Niveau en general
    bg = pygame.image.load("background.png")
    def __init__(self, joueur):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.joueur = joueur
        self.monde_scrolling = 0#on définit le scrolling comme étant nul de base
        
    def update(self):
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, ecran):
        ecran.blit(self.bg,(self.monde_scrolling // 1,0))
        self.platform_list.draw(ecran)
        self.enemy_list.draw(ecran)
        
    def scrolling(self, shift_x):#scrolling 
        self.monde_scrolling += shift_x
        for platform in self.platform_list:#pour toutes les platformes
            platform.rect.x += shift_x#on les déplacent
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

class Level_01(Level): #Classe Level 1 qui prend comme base la classe Level
    def __init__(self, joueur):
        """ Creattion du level 1. """
        super().__init__(joueur)#On ajout les variables du init de Level dans cet init
        self.level_limit = -1000

        level = [[100, 30, 100, 600],#plateformes du niveau
                 [100, 30, 400, 700],#[longueur, largeur, x, y]
                 [100, 30, 500, 500],
                 [100, 30, 750, 400],
                 [100, 30, 1000, 300],
                 ]

        for platform in level:#pour toutes les plateformes dans la liste des plateformes du niveau
            bloc = Platform(platform[0], platform[1])#bloc est de longueur et largeur par exemple 100,30
            bloc.rect.x = platform[2]#la plateforme se situe en x = 400 par ex
            bloc.rect.y = platform[3]#pareil pour y
            bloc.joueur = self.joueur
            self.platform_list.add(bloc)#on ajoute bloc à la liste des plateformes

#Programme principale
pygame.init()
ecran = pygame.display.set_mode([ECRAN_LONGUEUR, ECRAN_HAUTEUR])
pygame.display.set_caption("Je veux rentrer !")
joueur = Joueur() #permet d'ecrire la classe Joueur() comme une variable
level_list = []#on définit la liste vide level_list
level_list.append( Level_01(joueur) )#on ajoute le niveau 1
current_level_no = 0
current_level = level_list[current_level_no]
active_sprite_list = pygame.sprite.Group()#on défini active_sprit_list comme un ensemble de sprite (sprite.Group)
joueur.rect.x = 340
joueur.rect.y = ECRAN_HAUTEUR - joueur.rect.height
joueur.level = current_level
active_sprite_list.add(joueur)#on ajoute le joueur dans la liste
continuer = 1#on défini continuer comme étant la variable qui va déterminer si la boucle princiaple se fait ou non
pygame.mixer.music.play(loops=-1)#on démarre la musique du menu

#Boucle principale
while continuer:
    menu=True#variable boolèene menu qui défini si on démarre la boucle menu ou non
    credit=False#de meme avec l'écran des crédits
    curseur=1#on défini curseur sur le bouton "Joueur" de base
    #Boucle menu
    while menu:#tant que menu=True
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    curseur=curseur-1
                    if curseur==0:
                    #si curseur va en dessous de 1, on le remet à 1, cela permet que curseur ne peut avoir que 3 valeurs
                        curseur=1
                elif event.key==pygame.K_DOWN:
                    curseur=curseur+1
                    if curseur==4:
                        curseur=3
                if event.key==pygame.K_RETURN:
                    if curseur==1:
                        pygame.mixer.music.stop()
                        jeu=True
                        menu=False
                        musique = pygame.mixer.music.load("level1.ogg")
                        pygame.mixer.music.play(loops=-1)
                    if curseur==2:
                        menu = False
                        credit = True
                    if curseur==3:
                        pygame.quit()
                        quit()
        #Animation de la main de curseur
        if curseur==1:
            perso = pygame.image.load("persomenu1.png").convert_alpha()
        if curseur==2:
            perso = pygame.image.load("persomenu2.png").convert_alpha()
        if curseur==3:
            perso = pygame.image.load("persomenu3.png").convert_alpha()
        #Affichage et mise à jour des élements de l'écran
        ecran.blit(fondmenu, (0,0))
        ecran.blit(perso,(760,237))
        pygame.display.update()
    #Boucle credits    
    while credit:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    credit=False
                    jeu=False
                    menu=True
        ecran.blit(bgcredit,(0,0))
        pygame.display.update()
    #Boucle jeu
    while jeu:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                jeu = False
            if event.type == pygame.KEYDOWN:#Si une touche est préssée
                if event.key == pygame.K_LEFT:#La touche fleche gauche :
                    joueur.deplacement_gauche()
                if event.key == pygame.K_RIGHT:#etc
                    joueur.deplacement_droit()
                if event.key == pygame.K_UP:
                    joueur.jump()
                if event.key == pygame.K_ESCAPE:
                    musique = pygame.mixer.music.load("menu.ogg")
                    pygame.mixer.music.play(loops=-1)
                    jeu=False
                    menu=True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and joueur.change_x < 0:
                    joueur.stop()
                if event.key == pygame.K_RIGHT and joueur.change_x > 0:
                    joueur.stop()
        #mise à jour des élements
        active_sprite_list.update()
        current_level.update()

        if joueur.rect.right >= 500:#si le personnage est à + de 500 px à droite : il reste à 500 et le scrolling s'effectue
            diff = joueur.rect.right - 500#diference entre la position du joueur et 500 px
            joueur.rect.right = 500
            current_level.scrolling(-diff)

        if joueur.rect.left <= 120:#pareil l'autre coté
            diff = 120 - joueur.rect.left
            joueur.rect.left = 120
            current_level.scrolling(diff)
 
        current_position = joueur.rect.x + current_level.monde_scrolling
        if current_position < current_level.level_limit:#si la positon du joueur dépasse les limite du niveau
            joueur.rect.x = 120#le joueur se place en x = 120 px
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                joueur.level = current_level

        if joueur.rect.left == ECRAN_HAUTEUR:#Test game over
            jeu=False
            credit=True#game over provisoire
        if joueur.rect.left < 0:
            joueur.rect.left = 0
        current_level.draw(ecran)
        active_sprite_list.draw(ecran)
        #pygame.time.Clock().tick(60)#vitesse du jeu
        pygame.display.flip()
        pygame.display.update()
pygame.quit()
