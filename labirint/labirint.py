from pygame import *
'Картинки'
img_back = 'white_back.jpg'
img_hero = 'krug.png'
img_enemy = 'kvadrat.png'
img_goal = 'sus.png'
img_bullet = 'bullet.png'
'Музыка'
mixer.init()
mixer.music.load('music.ogg')
mixer.music.play()
fire = mixer.Sound('fire_music.ogg')
"Шрифт"
font.init()
font = font.SysFont('Comic Sans Ms', 50)
win = font.render('ты выиграл!', True,(0,0,0))
lose = font.render('ты проиграл!', True,(0,0,0))
'Классы'
class GameSprite(sprite.Sprite): #Родитель для других классов
    def __init__(self, player_image, player_x, player_y, width, height, speed):
        sprite.Sprite.__init__(self) #Конструктор класса Sprite
        self.image = transform.scale(image.load(player_image),(width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 30:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 30:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.right, self.rect.centery, 30,20,15)
        bullets.add(bullet)
class Enemy(GameSprite):
    side = 'left'
    def update(self):
        if self.rect.x <= 520:
            self.side = 'right'
        if self.rect.x >= win_width -65:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Enemy2(GameSprite):
    side = 'up'
    def update(self):
        if self.rect.y <= 30:
            self.side = 'up'
        if self.rect.y >= win_width - 530:
            self.side = 'down'
        if self.side == 'down':
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
class Enemy3(GameSprite):
    side = 'up'
    def update(self):
        if self.rect.y <= 30:
            self.side = 'up'
        if self.rect.y >= win_width - 350:
            self.side = 'down'
        if self.side == 'down':
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
class Enemy4(GameSprite):
    side = 'left'
    def update(self):
        if self.rect.x <= 120:
            self.side = 'right'
        if self.rect.x >= win_width -230:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
            
class Wall(sprite.Sprite):
    def __init__(self,red, green, blue, wall_x, wall_y, width, height):
        super().__init__()
        self.red = red
        self.green = green
        self.blue = blue
        self.w = width
        self.h = height
        self.image = Surface((self.w, self.h))
        self.image.fill((red, green, blue))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width+10:
            self.kill()
            fire.play()

'окно игры'
win_width = 700
win_height = 500
display.set_caption('Лабиринт')
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load(img_back), (win_width, win_height))
'персонажи'
hero = Player(img_hero, 5, win_height - 80, 25,25 ,3)
monster = Enemy(img_enemy,win_width - 150,190,55,40,5)
final = GameSprite(img_goal, win_width - 120, win_height - 80,65,65,0)
monster2 = Enemy2(img_enemy, win_width - 580,60,55, 40, 4)
monster3 = Enemy3(img_enemy, win_width - 480,60,55, 40, 4)
monster4 = Enemy4(img_enemy,win_width - 580,420,55,40,4)

'стены'
w1 = Wall(154,205,50,100,20,580,10)
w2 = Wall(154,205,50,680,20,10,470)
w3 = Wall(154,205,50,400,20,10,380)
w4 = Wall(154,205,50,100,130,10,360)
w5 = Wall(154,205,50,100,330,110, 10)
w6 = Wall(154,205,50,200,400,210,10)
w7 = Wall(154,205,50,300,130,10,200)
w8 = Wall(154,205,50,200,130,10,200)
w9 = Wall(154,205,50,100,480, 580, 10)
w10 = Wall(154,205,50,520,180,10,300)
'группы спрайтов'
walls = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()
'добавление спрайтов в группу'
monsters.add(monster)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
walls.add(w1)
walls.add(w2)
walls.add(w3)
walls.add(w4)
walls.add(w5)
walls.add(w6)
walls.add(w7)
walls.add(w8)
walls.add(w9)
walls.add(w10) 
'счетчик'
points = 0
'игровой цикл'
game = True
finish = False
clock = time.Clock()
FPS = 60
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()
    if finish != True:
        window.blit(back, (0,0))

        walls.draw(window)
        monsters.update()
        monsters.draw(window)
        hero.reset()
        hero.update()
        final.reset()
        bullets.draw(window)
        bullets.update()
        sprite.groupcollide(bullets, walls, True, False)
        if sprite.groupcollide(bullets, monsters, True, True):
            points += 1
        x = font.render(str(points), True, (0,0,0))
        window.blit(x, (10,10))
        
        #Проигрыш
        if sprite.spritecollide(hero, monsters, False):
            finish = True
            window.blit(lose, (200, 200))
        if sprite.spritecollide(hero, walls, False):
            finish = True
            window.blit(lose, (200, 200))
        #Выигрыш
        if sprite.collide_rect(hero, final):
            finish = True
            window.blit(win, (200, 200))
    display.update()
    clock.tick(FPS)
