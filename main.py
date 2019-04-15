#coding:utf-8
import pygame

VERT = (0,255,0)
BLANC = (255,255,255)
NOIR = (0,0,0)
BLEU = (0,0,255)
ROUGE = (255, 0, 0)
ECRAN_LONGUEUR = 1280
ECRAN_HAUTEUR = 720

class Joueur(pygame.sprite.Sprite):
    def init(self):
        """ Constructor function """
        super().init() #Appelle le constructeur de la classe mère
        longueur = 40
        hauteur = 60
        self.image = pygame.Surface([longueur, hauteur])
        self.image.fill(ROUGE)
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.level = None
 
    def update(self):
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
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        if self.rect.y >= ECRAN_HAUTEUR - self.rect.hauteur and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = ECRAN_HAUTEUR - self.rect.hauteur
 
    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        if len(platform_hit_list) > 0 or self.rect.bottom >= ECRAN_LONGUEUR:
            self.change_y = -10

    def go_left(self):
        self.change_x = -6
 
    def go_right(self):
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
    def init(self, longueur, hauteur):
        super().init()
        self.image = pygame.Surface([longueur, hauteur])
        self.image.fill(VERT)
        self.rect = self.image.get_rect()

class Level(object):#Classe Niveau en general
    def init(self, joueur):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.joueur = joueur
        self.background = None
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, ecran):
        """ Draw everything on this level. """
        ecran.fill(BLEU)
        self.platform_list.draw(ecran)
        self.enemy_list.draw(ecran)

class Level_01(Level): #Classe Level1 qui prend comme base la classe Level

    def init(self, joueur):
        """ Creattion du level 1. """
        Level.init(self, joueur)#On ajout les variables du init de Level dans cet init
 
        level = [[210, 70, 500, 500],
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
level_list.append( Level_01() )
current_level_no = 0
current_level = level_list[current_level_no]
active_sprite_list = pygame.sprite.Group()
joueur.level = current_level
joueur.rect.x = 340
joueur.rect.y = ECRAN_HAUTEUR - joueur.rect.hauteur
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
                joueur.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and joueur.change_x < 0:
                joueur.stop()
            if event.key == pygame.K_RIGHT and joueur.change_x > 0:
                joueur.stop()
    active_sprite_list.update()
    current_level.update()
    if joueur.rect.right > ECRAN_LONGUEUR:
        joueur.rect.right = ECRAN_LONGUEUR
    if joueur.rect.left < 0:
        joueur.rect.left = 0
    current_level.draw(ecran)
    active_sprite_list.draw(ecran)
    clock.tick(20)
    pygame.display.flip()
pygame.quit()
