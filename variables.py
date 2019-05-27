import pygame
import copy
from pygame.locals import *
import main

#Constantes
ECRAN_LONGUEUR = 1280
ECRAN_HAUTEUR = 720
bgcredit = pygame.image.load("bkgcredits.png")
pygame.mixer.init(44100, -16,2,2048)#on initialise mixer (frequence du son, nombre de bits, etc)
pygame.font.init()
musique = pygame.mixer.music.load("menu.ogg")
ville = pygame.mixer.Sound("ville.ogg")#
poubelle = pygame.mixer.Sound("poubelle.ogg")#
chat = pygame.mixer.Sound("chatson.ogg")#
sonreve = pygame.mixer.Sound("dream.ogg")
margot = pygame.mixer.Sound("margot.ogg")#
sonjump = pygame.mixer.Sound("jump.ogg")#
songameover = pygame.mixer.Sound("gameover.ogg")
soncanette = pygame.mixer.Sound("soncanette.ogg")
perso = pygame.image.load("persomenu1.png")
fondmenu = pygame.image.load("bkgmenu.png")
bggameover = pygame.image.load("bkgameover.png")
defaultJoueurPosition = Rect(50, ECRAN_HAUTEUR - 200, 60, 100)#position du joueur par default : (x,y,longueur,hauteur)
bg = pygame.image.load("background.png")
defaultEnemyMargotPosition = Rect(240,402,60,110)
defaultEnemyChatPosition = Rect(163, 0, 60, 110)
font = pygame.font.Font(None,36)
textscore = font.render("Score:",1,(100,100,100))

#Variables
position="Droite"
menu=True#variable boolèene menu qui défini si on démarre la boucle menu ou non
credit=False#de meme avec l'écran des crédits et gameover
gameover=False
jeu=False
score = 0
textscorechiffre = font.render(str(score),1,(100,100,100))
