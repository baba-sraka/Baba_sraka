from pygame import *
from random import randint


score = 0 
mising = 0

font.init()
font2 = font.Font(None, 36)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_buls = 'bullet.png'
img_back = "fon.jpg"
img_hero = "lox.jpg"
img_enemy = 'bomsh.jpg'

class GameSprite(sprite.Sprite):

   def __init__(self, player_image, player_x, player_y, player_speed):

       sprite.Sprite.__init__(self)

       self.image = transform.scale(image.load(player_image), (50, 50))
       self.speed = player_speed

       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_a] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_d] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
        

   def fire(self):
       bullet = Bullet('bullet.png', self.rect.centerx, self.rect.centery, 15)
       chikahgo_buls.add(bullet)
    

   

class Enemy(GameSprite):
    def update(self):
        global mising
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = randint(-200, -50)           
            self.rect.x = randint(0, 650)
            mising += 1



class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Shooter")
clock = time.Clock()
FPS = 60
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


ship = Player(img_hero, 400, 400, 5)

bomshs = sprite.Group()
for i in range(5):
    bomsh = Enemy('bomsh.jpg', randint(0, 650), randint(-200,-50),randint(1,2))
    bomshs.add(bomsh)

chikahgo_buls = sprite.Group()


finish = False

finish = False

run = True
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                ship.fire()



    if not finish:
        window.blit(background,(0,0))
        ship.reset()
        ship.update() 
        bomshs.update()
        bomshs.draw(window)
        chikahgo_buls.update()
        chikahgo_buls.draw(window)


        collides = sprite.groupcollide(bomshs, chikahgo_buls, True, True)
        for c in collides:
            score += 1
            bomsh = Enemy('bomsh.jpg', randint(0, 650), randint(-200,-50),randint(1,2))
            bomshs.add(bomsh)
 
                            

        if sprite.spritecollide(ship, bomshs, False):
           finish = True

        text1 = font2.render('Счёт:' + str(score), 1, (255, 255, 200))
        text2 = font2.render('Пропущено:' + str(mising), 1, (255, 255, 200))
        text3 = font2.render('Ты Бот', 1,(0, 0, 200))

        window.blit(text1, (10, 20))
        window.blit(text2, (10, 50))
        window.blit(text3, (350, 250))
    display.update()
    clock.tick(FPS)
