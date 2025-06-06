#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
win_width=700
win_heigt=500
window=display.set_mode((win_width,win_heigt))
background=transform.scale(image.load('galaxy.jpg'),(win_width,win_heigt))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
run=True
clock=time.Clock()
fire_sound=mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image=transform.scale(image.load(player_image),(size_x,size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x<win_width-80:
            self.rect.x+=self.speed
    def fire(self):
        bullet=Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)
ship=Player('rocket.png',300,400,80,100,10)
finish=False

class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global lost
        if self.rect.y>win_heigt:
            self.rect.x=randint(80,win_width-80)
            self.rect.y=-50
            lost=lost+1

class Bullet(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y<0:
            self.kill()

lost=0
monsters=sprite.Group()
asteroids=sprite.Group()
bullets=sprite.Group()
font.init()
font2=font.SysFont('Arial',33)
font1=font.SysFont('Arial',65)
lose=font1.render('You Lose',True,(255,0,0))
win=font1.render('You Win',True,(0,128,0))
life=3
score=0
rel_time=False
num_fire=0
for i in range(1,6):
    monster=Enemy('ufo.png',randint(80,win_width-80),-40,80,50,randint(1,5))
    monsters.add(monster)
for i in range(1,4):
    asteroid=Enemy('asteroid.png',randint(80,win_width-80),-40,80,50,randint(1,3))
    asteroids.add(asteroid)
while run:
    for e in event.get():
        if e.type==QUIT:
            run=False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                if num_fire<5 and rel_time==False:
                    num_fire=num_fire+1
                    fire_sound.play()
                    ship.fire()
                if num_fire>=5 and rel_time==False:
                    last_time=timer()
                    rel_time=True
    if not finish:

        window.blit(background,(0,0))
        ship.update()
        ship.reset()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.update()
        asteroids.draw(window)
        if rel_time==True:
            now_time=timer()
            if now_time-last_time<3:
                reload=font2.render('Wait,reload..',1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire=0
                rel_time=False
        collides=sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score=score+1
            monster=Enemy('ufo.png',randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters,False) or sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            life=life-1
        if  life==0 or lost>=8:
            finish=True
            window.blit(lose,(250,200))
        if score>=10:
            finish=True
            window.blit(win,(250,200))
        text=font2.render('Счет: '+str(score),1,(255,255,255))
        window.blit(text,(10,20))
        text_lose=font2.render('Пропущено: '+str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))
        if life==3:
            life_color=(0,150,0)
        if life==2:
            life_color=(150,150,0)
        if life==1:
            life_color=(150,0,0)
        text_life=font2.render(str(life),1,life_color)
        window.blit(text_life,(650,10))
    display.update()
    clock.tick(40)