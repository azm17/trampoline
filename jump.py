# -*- coding: utf-8 -*-

import sys
import pygame
import random
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE,K_SPACE,K_2,K_1
import android_3type_pic as my_func
import matplotlib.pyplot as plt
import copy
import math

# ===== Physical parameters =====
FPS = 30    # フレームレート [f/s]
DT = 1 / FPS # ステップ時間 [s]
G = 9.8      # 重力加速度 [kg.m/s^2]
K = 10       # ばね定数 [N/m]
C = 0.4

def first_message(sf, msg, h, color):
    sysfont = pygame.font.SysFont(None, 60)
    message = sysfont.render(msg, True, color)
    message_rect = message.get_rect()
    message_rect.center = (150,h)
    sf.blit(message, message_rect)
    pygame.time.delay(5)
    pygame.display.update()

def info_message(sf, msg, h, color):
    sysfont = pygame.font.SysFont(None, 30)
    message = sysfont.render(msg, True, color)
    message_rect = message.get_rect()
    message_rect.center = (50,h)
    sf.blit(message, message_rect)

class MyObject():
    def __init__(self, x, y, size_vertical, size_horizontal, name, draw_mode):
        # player settings
        self.name=name # オブジェクトの名前
        self.x = x
        self.y = y #オブジェクトの座標
        self.size_vertical = size_vertical# オブジェクトの大きさ
        self.size_horizontal = size_horizontal
        self.draw_mode = draw_mode
    
    def xy_body(self):# オブジェクトの範囲
        return {'x1':self.x,
                'x2':self.x + self.size_horizontal,
                'y1':self.y,
                'y2':self.y + self.size_vertical}
    
    def print_details(self):
        print(f"--------\nPosition: ({self.x},{self.y})")

class Ground(MyObject):# トランポリン
    def __init__(self, x, y, sv, sh, name, draw_mode):
        super(Ground, self).__init__(x, y, sv, sh, name, draw_mode)
    
    def draw(self, surface):
        # 矩形を描画 pygame.draw.rect(Surface, color, Rect, width=0)
        #if mode==0 or mode == 2:
        pygame.draw.rect(surface, 
                         (255, 255, 0), 
                         (self.x, self.y, self.size_horizontal, self.size_vertical))
        #if mode==1 or mode == 2:
        #    surface.blit(image, (self.x-22,self.y-10))
        
class Android(MyObject):# 主人公
    def __init__(self, x, y, sv, sh, name, draw_mode):
        super(Android, self).__init__(x, y, sv, sh, name, draw_mode)
        self.time = 0# 時間
        self.weight = 20# 重さ　
        self.velocity = 0# 速度
        self.start_position = y
        self.n_jump = 0
        self.image = [pygame.image.load("./jumping_android1.png"),
                      pygame.image.load("./crouching_android1.png"),#しゃがんでいるとき用1
                      pygame.image.load("./falling_android1.png")]#落ちるとき用2
    
    def draw(self, surface, x):
        if self.velocity > 0:
            form = 2
        else: 
            form = 0
        if x > 0:
            form = 1
        
        # 矩形を描画 pygame.draw.rect(Surface, color, Rect, width=0)
        if self.draw_mode == 0 or self.draw_mode == 2:
            pygame.draw.rect(surface, (0, 0, 255), (self.x, self.y, self.size_vertical, self.size_horizontal))
        if self.draw_mode == 1 or self.draw_mode == 2:
            surface.blit(self.image[form], (self.x-22,self.y-10))
    
    def print_details(self):
        print(f'----time:{round(self.time,1)}----\n'\
                          +f'Position: ({round(self.x,)},{round(self.y,1)})\n'\
                          +f'Velocity: {round(self.velocity,1)}\n'\
                          +f'Velocity: {round(self.velocity,1)}\n')

# 描画処理
def draw(surface, ground, android):
    surface.fill((0,0,0))# 画面初期化
    #pygame.time.delay(1)
    x = android.y + android.size_vertical - ground.y
    # オブジェクト表示
    android.draw(surface, x)
    ground.draw(surface)
    if x > 0:
        pygame.draw.line(surface, (255, 255, 0), 
                         (ground.x, ground.y), 
                         (android.x, android.y + android.size_vertical), 2)
        
        pygame.draw.line(surface, (255, 255, 0), 
                         (ground.x + ground.size_horizontal-3, ground.y), 
                         (android.x + android.size_horizontal, android.y + android.size_vertical), 2)
        
        pygame.draw.line(surface, (255, 255, 0), 
                         (android.x, android.y + android.size_vertical), 
                         (android.x + android.size_horizontal, android.y + android.size_vertical), 2)
    # スタート位置
    pygame.draw.line(surface, (255, 255, 255), 
                     (115,android.start_position),
                     (215,android.start_position), 1)
    # 頭の位置
    pygame.draw.line(surface, (255, 255, 255), (115,android.y), (215,android.y), 1)
    
    #msg=f"Height: {round(android.y,1)}"
    info_message(surface, "Number:", 10, (255,255,255))
    info_message(surface, f"{trial}", 30, (255,255,255))
    info_message(surface, "Time:", 50, (255,255,255))
    info_message(surface, f"{round(android.time)}", 70, (255,255,255))
    info_message(surface, "Height:", 90, (255,255,255))
    info_message(surface, f"{round(-(android.y-ground.y))}", 110, (255,255,255))
    info_message(surface, "Jump:", 130, (255,255,255))
    info_message(surface, f"{round(android.n_jump,1)}", 150, (255,255,255))
    
    
    
    pygame.display.update()
    
# 物理計算
def calculation(android, ground, Apply_force_down_t):
    global jump
    global tmp_t
    global jump2
    f = android.weight * G # 重力
    x = android.y + android.size_vertical - ground.y# トランポリンの表面との距離
    if x > 0:# トランポリンに衝突したとき
        tmp_t += DT
        f += -K * x
        #f += -C * android.velocity# 減衰
        if jump and tmp_t >= Apply_force_down_t:# ジャンプする
            f += 2*android.weight * G
            #print(f'T_J: {tmp_t}\nAFD: {Apply_force_down_t}\n')
            jump = False
        if jump2:
            #print("AAA")
            android.n_jump+=1
            jump2=False
    else:
        jump2=True
        tmp_t = 0
        jump = True
    # 動きの計算
    alpha = f / android.weight# a = f / m （ニュートンの運動方程式），加速度を求める
    android.velocity += alpha * DT# v += a * dt （積分：加速度 ⇒ 速度），速度を計算
    android.y += android.velocity * DT# y += v * dt (積分：速度 ⇒ 位置)，次の位置を計算
    android.time += DT# 経過時間

# ボタン処理
def button():
    global state
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()
        if event.type == KEYDOWN:# 終了
            if event.key == K_ESCAPE:
                pygame.quit(); sys.exit()
            if event.key == K_2:
                state = 2
            if event.key == K_SPACE or event.key == K_1:# 計算開始
                state = 1

def draw_graph(surface,data):
    surface.fill((0,0,0))# 画面初期化
    surface.blit(pygame.image.load("./figure.png"), (20,20))
    pygame.display.update()
    
def _rouletteSelection(self):# ルーレット選択
        pool_next = []
        total = 0
        for pool_i in self.pool:
            total += pool_i.getFittness()
        
        while (len(pool_next) < self.N):
            sum_fittness = 0
            p = random.random()
            for pool_i in self.pool:
                sum_fittness += pool_i.getFittness()
                if p <= sum_fittness/total:
                    pool_next.append(copy.deepcopy(pool_i))
                    break
        self.pool = pool_next[:]

def main():
    global jump # ジャンプできるかできないかTrue or False
    global state # ゲームの状態:{開始前:0,実行中:1}
    global tmp_t
    global trial
    global jump2
    trial = 0# 試行回数
    jump = True
    jump2 = True
    my_func.create_jumping_android(14)#画像生成
    my_func.create_crouching_android(14)
    my_func.create_falling_android(14)
    width_stage = 1000; height_stage = 600# area設定
    pygame.init()
    pygame.display.set_mode((width_stage, height_stage)) # 画面設定
    pygame.display.set_caption("トランポリン") #タイトル
    surface = pygame.display.get_surface()
    surface.fill((0,0,0)) # 画面初期化
    state = 0# 初期状態
    data = []
    ground = Ground(115, 450, 10, 100, 'ground', 0)# ground
    trial = 0
    N = 1000
    AFD=[]
    for i in range(N):
        AFD.append(random.uniform(0,6))
    #AFD = [random.uniform(0,10) for i in range(N)]
    while(True):
        y_max = -10000
        android = Android(150, 300, 40, 40, 'android', 1)# ドロイド君生成，位置(x,y)=(150, 100),大きさ(40*40)
        y_max_list=[]
        for Apply_force_down_t in AFD:
            while(True):
                button()# ボタン処理
                if state == 0:
                    first_message(surface, "Hit space Key", 150, (255,0,0))
                if state == 1 or 2:
                    calculation(android, ground, Apply_force_down_t)# 物理計算
                if state == 1:
                    #android.print_details()# デバッグ
                    draw(surface, ground, android)# 描画処理
                if android.n_jump > 10 and jump2 and android.velocity > 0:
                    tmp_y = -(android.y-ground.y)
                    if y_max < tmp_y:
                       y_max = tmp_y
                    break
            y_max_list.append(y_max)
        #print(y_max)
        # y_max
        trial += 1#試行回数
        data.append(sum(y_max_list)/len(y_max_list))
        if state == 2 and trial%10==0:
            plt.figure()
            plt.plot(data)
            plt.xlabel("N")
            plt.ylabel("Height")
            plt.title("GA")
            plt.savefig('figure.png')
            plt.close()
            draw_graph(surface,data)
        #print(AFD[1],y_max_list[1])
        pool_next = []
        mym = min(y_max_list)
        y_max_list = [math.exp(1*(i-mym)) for i in y_max_list]
        total = sum(y_max_list)# - min(y_max_list)*len(y_max_list)
        while (len(pool_next) < N):
            sum_fittness = 0
            p = random.random()
            i = 0
            for pool_i in y_max_list:
                sum_fittness += pool_i#-min(y_max_list)
                if p <= sum_fittness / total:
                    pool_next.append(AFD[i])
                    break
                i += 1
        """
        pool_next = []
        next_list=[i for i in range(N)]
        while len(pool_next) < N:
            #offspring1=copy.deepcopy(self.pool[random.choices(next_list,weights=self.Glist)])
            #pool_next.append(self.pool[random.choices(next_list,weights=self.Glist)])
            a=random.choices(next_list,weights=AFD)
            #print(a)
            #print(self.pool[a[0]])
            offspring1=copy.deepcopy(AFD[a[0]])
            #pass
            pool_next.append(offspring1)
        """
        """
        pool_next = []
        while len(pool_next) < N:
            offspring1 = copy.deepcopy(AFD[random.randrange(N)])
            offspring2 = copy.deepcopy(AFD[random.randrange(N)])
            if offspring1 < offspring2:
                pool_next.append(offspring1)
            else:
                pool_next.append(offspring2)
        """
        AFD = pool_next
if __name__ == "__main__":
    main()