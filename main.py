#coding:utf-8

#    Je veux rentrer !
#    Python 3
#    Pygame 1.9
#    Par :
#    Mael Le Boulicaut et Evan Diberder
#    v1.0

import pygame
import copy
from pygame.locals import *

#Constantes
ECRAN_LONGUEUR = 1280
ECRAN_HAUTEUR = 720
bgcredit = pygame.image.load("bkgcredits.png")
pygame.mixer.init(44100, -16,2,2048)#on initialise mixer (frequence du son, nombre de bits, etc)
pygame.font.init()
musique = pygame.mixer.music.load("menu.ogg")
sonjump = pygame.mixer.Sound("jump.ogg")
songameover = pygame.mixer.Sound("gameover.ogg")
soncanette = pygame.mixer.Sound("soncanette.ogg")
perso = pygame.image.load("persomenu1.png")
fondmenu = pygame.image.load("bkgmenu.png")
bggameover = pygame.image.load("bkgameover.png")
defaultJoueurPosition = Rect(50, ECRAN_HAUTEUR - 200, 60, 100)#position du joueur par default : (x,y,longueur,hauteur)
bg = pygame.image.load("background.png")
defaultEnemyMargotPosition = Rect(240,402,60,110)
score = 0
font = pygame.font.Font(None,36)
textscorechiffre = font.render(str(score),1,(100,100,100))
textscore = font.render("Score:",1,(100,100,100))

#Variables
position="Droite"
menu=True#variable boolèene menu qui défini si on démarre la boucle menu ou non
credit=False#de meme avec l'écran des crédits et gameover
gameover=False


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
        
        #Les boucles suivantes permettent de bloquer les coordonnée du joueur aux coordonnées de blocs de collisions
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
        if self.rect.y >= ECRAN_HAUTEUR - self.rect.height and self.change_y >= 0: #Si le sprite est en bas de l'ecran moins la hauteur du sprite (car sinon ce serait en dessous)
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
        if self.rect.x > 600 or self.rect.x < 20:
            self.rect.y += 6
        if self.rect.y >= 720 or self.rect.x <= 0:
            self.rect.x = joueur.rect.x + 30
            self.rect.y = joueur.rect.y + 40
            self.tir = False

class EnemyChat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("persopamargot.png")
        self.rect = self.image.get_rect()
        self.rect = copy.deepcopy(defaultEnemyMargotPosition)
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
        enemychat.rect = copy.deepcopy(defaultEnemyMargotPosition)
        score = 0
        bg = pygame.image.load("background.png")

    def scrolling(self, shift_x):#procédure scrolling 
        self.monde_scrolling += shift_x
        for platform in self.platform_list:#pour toutes les platformes
            platform.rect.x += shift_x#on les déplacent
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

class Level_01(Level): #Classe Level 1 qui prend comme base la classe Level
    def __init__(self, joueur):
        """ Creation du level 1. """
        super().__init__(joueur)#On ajout les variables du init de Level dans cet init
        self.level_limit = -1000

        level = [[100, 2, 20, 630],#plateformes du niveau
                 [100, 2, 250, 510],#[longueur, largeur, x, y]
                 [200, 2, 420, 338],
                 [300, 2, 780, 150],
                 [273, 2, 1, 100],
                 [50, 2, 1300, 300],
                 [100, 2, 1500, 600],
                 ]
        
        for platform in level:#pour toutes les plateformes dans la liste des plateformes du niveau
             bloc = Plateforme(platform[0], platform[1])#bloc est de longueur et largeur par exemple 100,30
             bloc.rect.x = platform[2]#la plateforme se situe en x = 400 par ex
             bloc.rect.y = platform[3]#pareil pour y
             bloc.joueur = self.joueur
             self.platform_list.add(bloc)#on ajoute bloc à la liste des plateformes
        
class Level_02(Level): #Classe Level 2
    def __init__(self, joueur):
        """ Creation du level 2. """
        super().__init__(joueur)#On ajout les variables du init de Level dans cet init
        self.level_limit = -1000

        level = [[100, 2, 30, 630],#plateformes du niveau
                 [100, 2, 260, 510],#[longueur, largeur, x, y]
                 [273, 2, 1, 100],
                 ]
        
        for platform in level:#pour toutes les plateformes dans la liste des plateformes du niveau
             bloc = Plateforme(platform[0], platform[1])#bloc est de longueur et largeur par exemple 100,30
             bloc.rect.x = platform[2]#la plateforme se situe en x = 400 par ex
             bloc.rect.y = platform[3]#pareil pour y
             bloc.joueur = self.joueur
             self.platform_list.add(bloc)#on ajoute bloc à la liste des plateformes
        
#Programme principal
pygame.init()
ecran = pygame.display.set_mode([ECRAN_LONGUEUR, ECRAN_HAUTEUR])
pygame.display.set_caption("Je veux rentrer !")
joueur = Joueur()#permet d'ecrire la classe objet Joueur() comme une variable utilisable
enemychat = EnemyChat()
projectile = Projectile()
projectile_list = pygame.sprite.Group()
level_list = []#on définit la liste vide level_list
level_list.append( Level_01(joueur) )#on ajoute le niveau 1
current_level_no = 0
current_level = level_list[current_level_no]
current_level.enemy_list.add(enemychat)
active_sprite_list = pygame.sprite.Group()#on défini active_sprit_list comme un ensemble de sprite (sprite.Group)
joueur.rect = copy.deepcopy(defaultJoueurPosition)#on copie la valeur de defaultJoueurPosition dans joueur.rect et non pas la variable en elle-même
joueur.level = current_level
active_sprite_list.add(joueur)#on ajoute le joueur dans la liste
projectile_list.add(projectile)
continuer = 1#on défini continuer comme étant la variable qui va déterminer si la boucle princiaple se fait ou non
pygame.mixer.music.play(loops=-1)#on démarre la musique du menu

#Boucle principale
while continuer:
    curseur=1#on défini curseur sur le bouton "Joueur" de base
    #Boucle menu
    while menu:#tant que menu=True
        for event in pygame.event.get():
            if event.type==pygame.QUIT: quit()
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
    #Boucle game over
    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameover=False
                    jeu=False
                    menu=True
        ecran.blit(bggameover,(0,0))
        ecran.blit(textscorechiffre, (580,600))
        ecran.blit(textscore, (500,600))
        pygame.display.update()
        musique = pygame.mixer.music.load("menu.ogg")
    current_level.resetJeu()
    pygame.mixer.music.play(loops=-1)
    #Boucle jeu
    while jeu:
        #Evenements au clavier
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                jeu = False
            if event.type == pygame.KEYDOWN:#Si une touche est préssée
                if event.key == pygame.K_LEFT:#La touche fleche gauche :
                    joueur.deplacement_gauche()#éffecue le deplacement du joueur
                    joueur.image = pygame.image.load("persocorentin2.png") #On inverse l'image du joueur car il va dans l'autre sens
                    position="Gauche"
                if event.key == pygame.K_RIGHT:#etc
                    joueur.deplacement_droit()
                    joueur.image = pygame.image.load("persocorentin.png")
                    position="Droite"
                if event.key == pygame.K_UP:
                    joueur.jump()
                if event.key == pygame.K_SPACE:
                    projectile.update()
                    projectile.tir = True
                    soncanette.play()
                if event.key == pygame.K_ESCAPE:
                    musique = pygame.mixer.music.load("menu.ogg")
                    pygame.mixer.music.play(loops=-1)
                    jeu=False
                    menu=True
            if event.type == pygame.KEYUP:#si la touche est relachée :
                if event.key == pygame.K_LEFT and joueur.change_x < 0:
                    joueur.stop()
                if event.key == pygame.K_RIGHT and joueur.change_x > 0:
                    joueur.stop()

        #Mise à jour des élements
        active_sprite_list.update()
        current_level.update()

        if projectile.tir == False :#on met à jour le projectile constamment pour qu'il suit le joueur
            projectile.rect.x = joueur.rect.x + 30
            projectile.rect.y = joueur.rect.y + 40
        if joueur.rect.right >= 500:#si le personnage est à + de 500 px à droite : il reste à 500 et le scrolling s'effectue
            diff = joueur.rect.right - 500#diference entre la position du joueur et 500 px
            joueur.rect.right = 500
            current_level.scrolling(-diff)

        if joueur.rect.left <= 120:#pareil l'autre coté
            diff = 120 - joueur.rect.left
            joueur.rect.left = 120
            current_level.scrolling(diff)

        current_position = joueur.rect.x + current_level.monde_scrolling#on definit une variable qui montre la position du joueur virtuellement

        if current_position < current_level.level_limit:#si la positon du joueur dépasse les limite du niveau
            bg = pygame.image.load("bkgcredits.png")
            level_list = []
            level_list.append( Level_02(joueur))
            current_level.resetJeu()#on reset le scrolling
            current_level.draw(ecran)
            pygame.display.update()
            
        if pygame.sprite.collide_rect(projectile, enemychat) :
            enemychat.rect.x += 1200
            score += 1
            textscorechiffre = font.render(str(score),1,(100,100,100))
         
        if pygame.sprite.collide_rect(joueur, enemychat)  :
            jeu = False
            gameover= True
            
        if joueur.rect.bottom > ECRAN_HAUTEUR:#Game over
            gameover=True
            jeu=False
            songameover.play()

        if joueur.rect.left < 0: #si le joueur va trop sur la gauche
            joueur.rect.left = 0 #on le bloque a la limite de l'ecran

        current_level.draw(ecran)
        active_sprite_list.draw(ecran)

        if projectile.tir == True:#si on tire
            projectile.update()#faire le deplacement du projectile

        print("Position :", current_position)
        print("Niveau actuel :", current_level)
        print(score)
        ecran.blit(textscorechiffre, (1100,50))
        ecran.blit(textscore, (1020,50))
        pygame.time.Clock().tick(60)#vitesse du jeu
        pygame.display.update()
        #Fin de la boucle jeu
    #Fin de la boucle principale
pygame.quit()
