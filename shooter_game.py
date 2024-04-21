from pygame import *
from random import*
#классы)
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
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
        if keys[K_RIGHT] and self.rect.x < 695:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_ybicanubov, self.rect.centerx, self.rect.top, 2, 6, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    #enemy movement
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

#Экран(тащит на себе всю тусовку)
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
galaxy = transform.scale(image.load('galaxy.jpg'), (700, 500))

#aga
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_ybicanubov = 'bullet.png'
score = 0 #вынесено
lost = 0 #помиловано
max_lost = 3
goal = 10
font.init()
font1 = font.SysFont(None, 80)
win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE!', True, (180,0,0))

font2 = font.Font(None, 36)
#Создание чупапиков
destroyer = Player(img_hero, 5, win_height-100, 80, 100, 10)
zhertvi = sprite.Group()
for i in range(1,6):
    monstertrukk = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1,5))
    zhertvi.add(monstertrukk)
bullets = sprite.Group()

#Музыка(непосредственно Каха)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#shrift
font.init()
font2 = font.Font(None, 36)

clock = time.Clock()
FPS = 60
finish = False
game = True

#Гэйм цикл)))
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                destroyer.fire()
    if not finish:
        window.blit(galaxy, (0,0))

        collides = sprite.groupcollide(zhertvi, bullets, True, True)
        for c in collides:
            score += 1
            monstertrukk = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1,5))
            zhertvi.add(monstertrukk)

        if sprite.spritecollide(destroyer, zhertvi, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render('Казнено:' + str(score), 1 , (255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render('Помиловано:' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10, 50))

        destroyer.update()
        destroyer.reset()
        zhertvi.update()
        zhertvi.draw(window)
        bullets.update()
        bullets.draw(window)
        display.update()
        clock.tick(FPS)
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in zhertvi:
            m.kill()

        time.delay(3000)
        for i in range(1,6):
            monstertrukk = Enemy(img_enemy, randint(80, win_width-80),-40, 80, 50, randint(1,5))
            zhertvi.add(monstertrukk)
    time.delay(50)






     