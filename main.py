from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
# student_code_starts
import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 加载背景图片
bg = pygame.image.load('pic/背景.png')
fg = pygame.image.load('pic/前景.png')

# 火鸟状态图片
fly = pygame.image.load('pic/飞行状态.png')
freeze = pygame.image.load('pic/冰冻状态.png')

# 子弹图片
pistol = pygame.image.load('pic/冰.png')

# 加载冰弹音效
sound_ice = pygame.mixer.Sound('music/冰弹音效.mp3')

# 加载瞄准器图片和矩形框
sight = pygame.image.load('pic/瞄准器.png')
sight_rect = sight.get_rect()

# 加载小火鸟朝右的图片，装进列表里
right = []
for i in range(10):
    right.append(pygame.image.load(f'pic/小鸟朝右{i}.png'))

# 加载小火鸟朝左的图片，装进列表里
left = []
for i in range(10):
    left.append(pygame.image.load(f'pic/小鸟朝左{i}.png'))

# 获取小火鸟矩形框
bird_rect = right[0].get_rect()

# 创建循环变量
tag = 0
# 加载小火鸟冰冻图片
ice = pygame.image.load('pic/小鸟冰冻.png')

# 创建状态列表
birds = []

# 创建计分变量
num = 0

# 加载字体
font = pygame.font.Font('font/方正.TTF', 30)

# 创建子弹计数变量
bullet = 0


# 小火鸟重新开始
def restart():
    global status, speedx, speedy, num, bullet
    bullet = 3
    status = 'fly'

    bird_rect.x = random.randint(200, 500)
    bird_rect.y = 500

    speedx = random.randint(3, 6) * random.choice([1, -1])
    speedy = random.randint(-12, -7)

    birds.append('fly')
    num += 1
    if num == 11:
        birds.pop()


# 小火鸟移动函数
def move():
    bird_rect.x += speedx
    bird_rect.y += speedy
    # 超出边界
    if bird_rect.x > 800 or bird_rect.x < 0 or bird_rect.y < 0 or bird_rect.y > 600:
        restart()  # 小鸟回到初始化状态


# 小鸟回到初始化状态
restart()

# 主循环模块
while True:
    # 遍历事件队列
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 点击右上角的'X'，终止主循环
            sys.exit()
        # 鼠标按下事件
        if event.type == pygame.MOUSEBUTTONDOWN and bullet > 0:
            sound_ice.play()  # 播放冰弹音效
            bullet -= 1 # 射出子弹
            if bird_rect.collidepoint(pos):
                status = 'freeze'  # 修改状态为冰冻
                speedx = 0
                speedy = 10
                # 列表中最后一只小鸟状态修改为冰冻
                birds[-1] = 'freeze'

    # 绘制背景
    screen.blit(bg, (0, 0))

    # 判断游戏是否进行到第 10 只鸟
    if num <= 10:

        # 小火鸟移动
        move()

        # 根据小火鸟状态，切换图片
        if status == 'fly':
            if speedx > 0:
                screen.blit(right[tag % 10], bird_rect)
            else:
                screen.blit(left[tag % 10], bird_rect)
            tag += 1
        else:
            screen.blit(ice, bird_rect)

    else:
        score = 0
        for value in birds:
            if value == 'freeze':
                score += 10
        # 显示最终得分
        text = font.render('你的得分：' + str(score), 1, 'black')
        screen.blit(text, (280, 200))

        # 显示称号
        if score > 70:
            string = '神枪手'
        elif score > 40:
            string = '加油，你还能进步'
        else:
            string = '描边大师'
        score_text = font.render(string, 1, 'black')
        screen.blit(score_text, (280, 250))



    # 获取鼠标坐标
    pos = pygame.mouse.get_pos()
    # 移动瞄准器矩形框
    sight_rect.center = pos
    # 绘制瞄准器
    screen.blit(sight, sight_rect)
    # 绘制前景
    screen.blit(fg, (0, 0))

    # 画出命中情况
    for i, value in enumerate(birds):
        if value == 'fly':
            screen.blit(fly, (100 + i * 50, 500))
        else:
            screen.blit(freeze, (100 + i * 50, 500))

    # 画出子弹情况
    for i in range(bullet):
        screen.blit(pistol, (680 - i * 20, 500))

    clock.tick(40)  # 设置刷新率
    pygame.display.update()  # 重绘界面

# student_code_ends