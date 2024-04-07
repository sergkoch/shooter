from pygame import *
from random import random, randrange, randint

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(img), (size_x, size_y))    
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if (keys_pressed[K_a] or keys_pressed[K_LEFT]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys_pressed[K_d] or keys_pressed[K_RIGHT]) and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys_pressed[K_SPACE]:
            self.fire()

    def fire(self):
        shoot.play()
        bullets.add(
            Bullet(
                bullet_spr,
                self.rect.centerx - (15 // 2), self.rect.top,
                15, 15, 20
            )
        )

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.y = -50
            self.rect.x = randint(0, win_width - 80)
            self.speed = randint(3, 5)
        
            global lost
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -10:
            self.kill()
            
lost = 0
score = 0

max_lost = 3
goal_score = 2

bg_mus = 'space.ogg'
img_rocket = 'rocket.png'
img_bg = 'galaxy.jpg'
img_enemy = 'ufo.png'
shoot_snd = 'fire.ogg'
bullet_spr = 'bullet.png'

rocket_size_x = 80
rocket_size_y = 100
rocket_spd = 10

mixer.init()
mixer.music.load(bg_mus)
mixer.music.play()

shoot = mixer.Sound(shoot_snd)

font.init()
label_font = font.Font(None, 36)

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_bg), (win_width, win_height))

ship = Player(img_rocket, (win_width // 2) - (rocket_size_x // 2), win_height - rocket_size_y, rocket_spd, rocket_size_x, rocket_size_y)

en = Enemy(img_enemy, 100, -40, 10, 80, 50,)

monsters = sprite.Group()
for _ in range(5):
    monsters.add(
        Enemy(img_enemy,
                randint(0, win_width - 80), -40,
                randint(3, 5),
                80, 50)
    )

bullets = sprite.Group()

finish = False
run = True

while run:
    time.delay(50)
    
    for e in event.get():
        if e.type == QUIT:
            run = False
            
    if not finish:
        window.blit(background, (0, 0))

        window.blit(
            label_font.render(
                f'Счет: {score}', True, (255, 255, 255)
            ), (10, 30)
        )

        window.blit(
        label_font.render(
            f'Пропущено: {lost}', True, (255, 255, 255)
        ), (10, 60)
        )


        colliders = sprite.groupcollide(monsters, bullets, True, True)
        for _ in colliders:
            score += 1
            monsters.add(
            Enemy(img_enemy,
                    randint(0, win_width - 80), -40,
                    randint(3, 5),
                    80, 50)
            )

        if score >= goal_score:
            finish = True
            window.blit(
        font.Font(None, 100).render(
            f'ПОБЕДА!', True, (0, 255, 20)
        ), (175, 200)
        )

        if lost >= max_lost:
            finish = True
            window.blit(
        font.Font(None, 100).render(
            f'ПОРАЖЕНИЕ!', True, (255, 0, 0)
        ), (175, 200)
        )

        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

        ship.update()

        ship.reset()

        display.update()