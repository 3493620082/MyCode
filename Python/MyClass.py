# -*- coding:utf-8 -*-
# ---
# 作者:Administrator
# 日期:2021-06-01
# ---
import random
import pygame


class myPlane(pygame.sprite.Sprite):                            # 玩家飞机
    def __init__(self, screen, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("img/me1.png").convert_alpha()
        self.image2 = pygame.image.load("img/me2.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image1)
        self.rect = self.image1.get_rect()
        self.width, self.height = screen_size[0], screen_size[1]
        self.rect.left, self.rect.bottom = (self.width - self.rect.width) // 2, self.height - 10

        self.screen = screen
        self.speed = 10
        self.switch_image = True
        self.delay = 100

        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("img/me_destroy_1.png").convert_alpha(),
                                    pygame.image.load("img/me_destroy_2.png").convert_alpha(),
                                    pygame.image.load("img/me_destroy_3.png").convert_alpha(),
                                    pygame.image.load("img/me_destroy_4.png").convert_alpha()])
        self.active = True
        self.down_sound = pygame.mixer.Sound("music/enemy3_down.mp3")
        self.down_sound.set_volume(0)

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.height - 10:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.height - 10

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width

    def animation(self):
        if self.switch_image:
            self.screen.blit(self.image1, self.rect)
        else:
            self.screen.blit(self.image2, self.rect)
        if self.delay % 5 == 0:
            self.switch_image = not self.switch_image
        self.delay -= 1
        if self.delay == 0:
            self.delay = 100

    def time_delay(self):                       # 作为整个游戏的动态切换时钟
        self.delay -= 1
        if self.delay == 0:
            self.delay = 100

    def reset(self):                            # 添加重生的方法
        self.active = True
        self.rect.left, self.rect.bottom = (self.width - self.rect.left) // 2, self.height - 10

    def play_sound(self):                       # 播放重生音效
        self.down_sound.play()


class Bullet(pygame.sprite.Sprite):                         # 我方子弹
    def __init__(self, position, direction):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("img/bullet2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 12
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = direction

    def move(self):
        if self.direction:
            self.rect.top -= self.speed
            if self.rect.top < 0:
                self.active = False
        else:
            self.rect.top += self.speed
            if self.rect.top > 700:
                self.active = True

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True


class BigEnemy(pygame.sprite.Sprite):                   # 大型敌机
    ENERGY = 20

    def __init__(self, screen_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("img/enemy3_n1.png").convert_alpha()

        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("img/enemy3_down1.png").convert_alpha(),
                                    pygame.image.load("img/enemy3_down2.png").convert_alpha(),
                                    pygame.image.load("img/enemy3_down3.png").convert_alpha(),
                                    pygame.image.load("img/enemy3_down4.png").convert_alpha()])
        self.rect = self.image.get_rect()
        self.width, self.height = screen_size[0], screen_size[1]
        self.speed = 1  # 敌机移动速度
        self.active = True  # 敌机的生存状态
        self.energy = BigEnemy.ENERGY  # 敌机血量

        # 敌机的位置是随机出现的
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                        random.randint(-15 * self.height, -5 * self.height)
        self.mask = pygame.mask.from_surface(self.image)

        self.fly_sound = pygame.mixer.Sound("music/enemy3_flying.mp3")
        self.fly_sound.set_volume(1.5)
        self.down_sound = pygame.mixer.Sound("music/enemy3_down.mp3")
        self.down_sound.set_volume(1)

    def move(self):
        if self.rect.top < self.height - 60:
            self.rect.top += self.speed
        else:
            self.reset()
        if self.rect.bottom == -50:
            self.fly_sound.play()

    def reset(self):
        self.active = True
        self.energy = BigEnemy.ENERGY
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                        random.randint(-15 * self.height, -5 * self.height)

    def play_sound(self):
        self.fly_sound.stop()
        self.down_sound.play()


class MidEnemy(pygame.sprite.Sprite):
    ENERGY = 10

    def __init__(self, screen_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("img/enemy2.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("img/enemy2_down1.png").convert_alpha(),
                                    pygame.image.load("img/enemy2_down2.png").convert_alpha(),
                                    pygame.image.load("img/enemy2_down3.png").convert_alpha(),
                                    pygame.image.load("img/enemy2_down4.png").convert_alpha()])
        self.rect = self.image.get_rect()
        self.width, self.height = screen_size[0], screen_size[1]
        self.speed = 1
        self.active = True
        self.energy = MidEnemy.ENERGY
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                        random.randint(-10 * self.height, -self.height)
        self.mask = pygame.mask.from_surface(self.image)

        self.down_sound = pygame.mixer.Sound("music/enemy3_down.mp3")
        self.down_sound.set_volume(0)

    def move(self):
        if self.rect.top < self.height - 60:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.ENERGY
        self.rect.left, self.rect.top = random.randint(0 ,self.width - self.rect.width), \
                                        random.randint(-10 * self.height, 0)

    def play_sound(self):
        self.down_sound.play()


class SmallEnemy(pygame.sprite.Sprite):                     # 小型敌机
    def __init__(self, screen_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("img/enemy1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("img/enemy1_down1.png").convert_alpha(),
            pygame.image.load("img/enemy1_down2.png").convert_alpha(),
            pygame.image.load("img/enemy1_down3.png").convert_alpha(),
            pygame.image.load("img/enemy1_down4.png").convert_alpha()])
        self.rect = self.image.get_rect()
        self.width, self.height = screen_size[0], screen_size[1]
        self.speed = 2
        self.active = True
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                        random.randint(-5 * self.height, 0)
        self.mask = pygame.mask.from_surface(self.image)

        self.down_sound = pygame.mixer.Sound("music/enemy3_down.mp3")
        self.down_sound.set_volume(0)

    def move(self):
        if self.rect.top < self.height - 60:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                        random.randint(-5 * self.height, 0)

    def play_sound(self):
        self.down_sound.play()
