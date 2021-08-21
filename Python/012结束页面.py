# -*- coding:utf-8 -*-
# ---
# 作者:Administrator
# 日期:2021-06-02
# ---

import pygame
import sys
import MyClass


pygame.init()
screen_size = width, height = 480, 700
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("飞机大战")
bg = pygame.image.load("img/background1.png").convert()

pygame.mixer.music.load("music/Pacific Rim.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


def add_big_enemies(group1, group2, num):                       # 创建大型敌机
    for big_enemies in range(num):
        each_big_enemy = MyClass.BigEnemy(screen_size)
        group1.add(each_big_enemy)
        group2.add(each_big_enemy)


def add_mid_enemies(group1, group2, num):                       # 创建大型敌机
    for big_enemies in range(num):
        each_mid_enemy = MyClass.MidEnemy(screen_size)
        group1.add(each_mid_enemy)
        group2.add(each_mid_enemy)


def add_small_enemies(group1, group2, num):                       # 创建大型敌机
    for big_enemies in range(num):
        each_small_enemy = MyClass.SmallEnemy(screen_size)
        group1.add(each_small_enemy)
        group2.add(each_small_enemy)


def main():
    clock = pygame.time.Clock()

    heroPlane = MyClass.myPlane(screen, screen_size)

    enemies = pygame.sprite.Group()

    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 5)

    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 10)

    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    bullet1 = []                                    # 生成己方飞机的子弹序列
    bullet1_index = 0                               # 子弹的序号
    BULLET1_NUM = 5                                 # 表示子弹5颗连发，刚好超过屏幕

    score = 0                                                       # 定义一个变量存放分数
    score_font = pygame.font.Font("font/微软雅黑 常规.ttc", 30)           # 定义一个font对象，显示结果的字体
    WhiteFont = (255, 255, 255)

    for i in range(BULLET1_NUM):                    # 序列生成子弹
        bullet1.append(MyClass.Bullet(heroPlane.rect.midtop, True))     # 子弹射击方向向上

    small_destroy_index = 0
    mid_destroy_index = 0
    big_destroy_index = 0
    hero_destroy_index = 0                      # 击毁后我方飞机动画的序号

    life_image = pygame.image.load("img/life.png").convert_alpha()      # 加载血量的图片
    life_rect = life_image.get_rect()                                   # 获取血量的rect对象
    life_NUM = 5                                                        # 设置血量为3

    gameover_font = pygame.font.Font("font/微软雅黑 常规.ttc", 48)  # 显示最后的结果
    again_image = pygame.image.load("img/again.png").convert_alpha()  # 加载重新开始
    gameover_image = pygame.image.load("img/gameover.png").convert_alpha()  # 加载结束游戏

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            heroPlane.moveUp()
        if key_pressed[pygame.K_DOWN]:
            heroPlane.moveDown()
        if key_pressed[pygame.K_LEFT]:
            heroPlane.moveLeft()
        if key_pressed[pygame.K_RIGHT]:
            heroPlane.moveRight()

        # screen.blit(bg, (0, 0))
        heroPlane.time_delay()

        heroPlane.time_delay()                      # 运行动态时钟

        if life_NUM > 0:                                                            # 判断血量是否大于0
            screen.blit(bg, (0, 0))
            for each in big_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    if not (heroPlane.delay % 3):
                        screen.blit(each.destroy_images[big_destroy_index], each.rect)
                        big_destroy_index = (big_destroy_index + 1) % 4
                        if big_destroy_index == 0:
                            each.play_sound()
                            score += 50
                            each.reset()

            for each in mid_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    if not (heroPlane.delay % 3):
                        screen.blit(each.destroy_images[mid_destroy_index], each.rect)
                        big_destroy_index = (big_destroy_index + 1) % 4
                        if big_destroy_index == 0:
                            each.play_sound()
                            score += 25
                            each.reset()

            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    if not (heroPlane.delay % 3):
                        screen.blit(each.destroy_images[small_destroy_index], each.rect)
                        big_destroy_index = (big_destroy_index + 1) % 4
                        if big_destroy_index == 0:
                            each.play_sound()
                            score += 10
                            each.reset()

            if heroPlane.active:  # 判断我方飞机的状态
                heroPlane.animation()  # 如果存活就继续移动
            else:
                if not (heroPlane.delay % 3):
                    screen.blit(heroPlane.destroy_images[hero_destroy_index], heroPlane.rect)  # 绘制坠毁的图片
                    hero_destroy_index = (hero_destroy_index + 1) % 4  # 更改图片的序号
                    if hero_destroy_index == 0:  # 如果是最后一张图片
                        life_NUM -= 1  # 血量减1
                        heroPlane.play_sound()  # 播放坠毁音效
                        heroPlane.reset()  # 重生飞机

            if life_NUM > 0:
                for i in range(life_NUM):
                    screen.blit(life_image, (width - 10 - (i + 1) * life_rect.width, height - 10 - life_rect.height))

            if not (heroPlane.delay % 10):
                bullet1[bullet1_index].reset(heroPlane.rect.midtop)
                bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            enemies_collided = pygame.sprite.spritecollide(heroPlane, enemies, False, pygame.sprite.collide_mask)

            if enemies_collided:  # 如果产生重合那么就死亡
                heroPlane.active = False  # 更改己方飞机的存活状态
                for each in enemies_collided:  # 产生重合
                    each.active = False  # 敌方飞机也会爆炸

            score_surface = score_font.render("Score: %s" % str(score), True, WhiteFont)  # 将需要显示的文字转换为surface对象
            screen.blit(score_surface, (10, 5))  # 将结果绘制出来
        else:
            screen.blit(bg, (0, 0))
            bullet1 = []  # 生成己方飞机的子弹序列
            bullet1_index = 0  # 子弹的序号
            BULLET1_NUM = -1  # 表示子弹5颗连发，刚好超过屏幕

            if not (heroPlane.delay % 10):
                # bullet1[bullet1_index].reset(heroPlane.rect.midtop)
                bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            pygame.mixer.music.stop()  # 先把背景音乐关了

            # 分别显示分数、重新开始和结束游戏
            gameover_score = gameover_font.render("Score : %s" % str(score), True, WhiteFont)
            screen.blit(gameover_score, (100, 200))
            screen.blit(again_image, (90, 350))
            screen.blit(gameover_image, (90, 450))

            mouse_down = pygame.mouse.get_pressed()  # 检测按键是否按下
            if mouse_down[0]:  # 如果按键的左键按下了
                pos = pygame.mouse.get_pos()  # 获取鼠标的坐标
                if 90 < pos[0] < 390 and 350 < pos[1] < 390:  # 如果是在重新开始的范围
                    pygame.mixer.music.play()
                    main()  # 重新调用main开始游戏
                elif 90 < pos[0] < 390 and 450 < pos[1] < 490:  # 如果在结束游戏的范围
                    pygame.quit()  # 退出pygame
                    sys.exit()  # 关闭进程

        for each in bullet1:
            if each.active:
                each.move()
                screen.blit(each.image, each.rect)
                enemies_hit = pygame.sprite.spritecollide(each, enemies, False, pygame.sprite.collide_mask)     # 检测子弹是否与敌机发生碰撞
                if enemies_hit:
                    each.active = False
                    for e in enemies_hit:
                        if e in mid_enemies or e in big_enemies:            # 如果击中的是中型，大型敌机，则扣血
                            e.energy -= 1
                            if e.energy == 0:               # 如果血扣完了，则敌机爆炸
                                e.active = False
                        else:                               # 如果是小飞机，直接爆炸
                            e.active = False
            else:
                each.reset(heroPlane.rect.midtop)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
