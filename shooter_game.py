import os
os.environ['SDL_VIDEODRIVER'] = 'windib'
from pygame import *
from random import randint




init()
font.init()
font1 = font.Font(None, 80)
win = font1.render('¡GANASTE!', True, (255, 255, 255))
lose = font1.render('¡PERDISTE!', True, (180, 0, 0))
font2 = font.Font(None, 36)
font3 = font.Font(None, 60)
credit = font3.render('Creado por Yago', True, (255, 255, 255))


img_back = "galaxy.jpg" 
img_hero = "rocket.png" 
img_bullet = "bullet.png"
img_lose = "loosescreeen.png"
enemy = randint(1, 100)
if enemy >= 1 and enemy < 100:
   img_enemy = "ufo.png"
elif enemy == 100:
    img_enemy = "trump.png" 


score = 0 
lost = 0 
max_lost = 20
max_win = 10
max_win = 10

class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)

       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
   def fire(self):
       print(enemy)
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
       

class Enemy(GameSprite):
   def update(self):
       self.rect.y += self.speed
       global lost
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
           if score < max_win:
               monsters.add(Enemy(img_enemy, self.rect.x, self.rect.y, 80, 50, randint(1, 5)))

class Bullet(GameSprite):
   def update(self):
       self.rect.y += self.speed
       if self.rect.y < 0:
           self.kill()


class Particle(sprite.Sprite):
   def __init__(self, x, y, vx, vy):
       sprite.Sprite.__init__(self)
       self.image = Surface((4, 4))
       self.image.fill((255, 200, 0))
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       self.vx = vx
       self.vy = vy
       self.lifetime = 0.5
       self.creation_time = time.get_ticks()

   def update(self):
       elapsed = (time.get_ticks() - self.creation_time) / 1000.0
       if elapsed > self.lifetime:
           self.kill()
       else:
           self.rect.x += self.vx
           self.rect.y += self.vy
           self.vy += 0.3


class Particle(sprite.Sprite):
   def __init__(self, x, y, vx, vy):
       sprite.Sprite.__init__(self)
       self.image = Surface((4, 4))
       self.image.fill((255, 200, 0))
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       self.vx = vx
       self.vy = vy
       self.lifetime = 0.5
       self.creation_time = time.get_ticks()

   def update(self):
       elapsed = (time.get_ticks() - self.creation_time) / 1000.0
       if elapsed > self.lifetime:
           self.kill()
       else:
           self.rect.x += self.vx
           self.rect.y += self.vy
           self.vy += 0.3


win_width = 700
win_height = 500
display.set_caption("China raids North Korea!!!")
icon = transform.scale(image.load("ico.jpg"), (32, 32))
icon.set_colorkey((255, 255, 255))
window = display.set_mode((win_width, win_height))
display.set_icon(icon)
background = transform.scale(image.load(img_back), (win_width, win_height))


ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)


bullets = sprite.Group()
particles = sprite.Group()


finish = False
show_credits = False
finish_time = 0
cinematic_mode = False
cinematic_start = 0
last_spawn_time = time.get_ticks()
spawn_interval = 3000

run = True
while run:
   for e in event.get():
       if e.type == QUIT:
           run = False
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               ship.fire()


   if cinematic_mode:
       window.blit(background,(0,0))
       cinematic_elapsed = (time.get_ticks() - cinematic_start) / 1000.0
       cinematic_duration = 5
       if cinematic_elapsed < cinematic_duration:
           progress = cinematic_elapsed / cinematic_duration
           current_score = int(score - (score * progress))
           current_lost = int(lost + ((max_lost - lost) * progress))
           text_lose = font2.render("Fallos: " + str(current_lost), 1, (0,0,255))
           window.blit(text_lose,(10,80))
           text_win = font2.render("Puntos: " + str(current_score), 1, (0,0,255))
           window.blit(text_win,(10,50))
       else:
           finish = True
           finish_time = time.get_ticks()
           lost = max_lost
           score = 0
           cinematic_mode = False
   elif not finish:
       window.blit(background,(0,0))
       ship.update()
       text_lose = font2.render("Fallos: " + str(lost), 1, (0,0,255))
       window.blit(text_lose,(10,80))
       text_win = font2.render("Puntos: " + str(score), 1, (0,0,255))
       window.blit(text_win,(10,50))
       monsters.update()
       bullets.update()
       particles.update()
       current_time = time.get_ticks()
       if current_time - last_spawn_time > spawn_interval and score < max_win:
           new_enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(new_enemy)
           last_spawn_time = current_time
       for collision in sprite.groupcollide(monsters, bullets, True, True):
           score += 1
           for i in range(8):
               from math import cos, sin
               angle = (i / 8) * 6.28
               speed = 3
               vx = speed * cos(angle)
               vy = speed * sin(angle)
               particle = Particle(collision.rect.centerx, collision.rect.centery, vx, vy)
               particles.add(particle)
           bullet_x = collision.rect.centerx
           bullet_y = collision.rect.centery
           for i in range(4):
               from math import cos, sin
               angle = (i / 4) * 6.28
               speed = 2.5
               vx = speed * cos(angle)
               vy = speed * sin(angle)
               particle = Particle(bullet_x, bullet_y, vx, vy)
               particles.add(particle)
       if lost >= max_lost:
           finish = True
           finish_time = time.get_ticks()
       if score >= max_win:
           cinematic_mode = True
           cinematic_start = time.get_ticks()
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
       particles.draw(window)


   else:
       elapsed = (time.get_ticks() - finish_time) / 1000.0
       if elapsed < 7:
           lose_screen = transform.scale(image.load(img_lose), (win_width, win_height))
           window.blit(lose_screen, (0,0))
       else:
           window.fill((0, 0, 0))
           window.blit(credit, (win_width//2 - credit.get_width()//2, win_height//2 - credit.get_height()//2))

   display.update()

   time.delay(50)