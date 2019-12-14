# -*- coding: utf-8 -*-

import sys
import pygame
#import random
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE,K_SPACE, K_r
import android_3type_pic as my_func


# ===== Physical parameters =====
FPS = 30     # フレームレート [f/s]
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
        self.weight = 10# 重さ　
        self.velocity = 0# 速度
        self.start_position = y
        my_func.create_jumping_android(14)#画像生成
        my_func.create_crouching_android(14)
        my_func.create_falling_android(14)
        self.image = [pygame.image.load("./jumping_android1.png"),
                      pygame.image.load("./crouching_android1.png"),#しゃがんでいるとき用1
                      pygame.image.load("./falling_android1.png")]#落ちるとき用2
    
    def draw(self, surface, x):
        if x > 0:
            form = 1
        else:
            if self.velocity > 0:
                form = 2
            else: 
                form = 0
        
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

# 描画
def draw(surface, ground, android):
    surface.fill((0,0,0))# 画面初期化
    pygame.time.delay(5)
    x = android.y + android.size_vertical - ground.y        
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
    # オブジェクト表示
    #for p in obgect_list:
    android.draw(surface, x)
    ground.draw(surface)
    # スタート位置
    pygame.draw.line(surface, (255, 255, 255), 
                     (115,android.start_position),
                     (215,android.start_position), 1)
    # 頭の位置
    pygame.draw.line(surface, (255, 255, 255), (115,android.y), (215,android.y), 1)
    pygame.display.update()

def calculation(android, ground):
    f = android.weight * G # 重力
    x = android.y + android.size_vertical - ground.y# トランポリンの表面との距離
    # トランポリンに衝突したとき
    if x > 0:
        f += -K * x
        #f += -C * android.velocity# 減衰
    
    # 動きの計算
    alpha = f / android.weight# a = f / m （ニュートンの運動方程式），加速度を求める
    android.velocity += alpha * DT# v += a * dt （積分：加速度 ⇒ 速度），速度を計算
    android.y += android.velocity * DT# y += v * dt (積分：速度 ⇒ 位置)，次の位置を計算
    android.time += DT# 経過時間

def button():
    global state
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()
            
        if event.type == KEYDOWN:# 終了
            if event.key == K_ESCAPE:
                pygame.quit(); sys.exit()
            if event.key == K_SPACE:# 計算開始
                state = 1

def main():
    global state # ゲームの状態:{開始前:0,実行中:1}
    width_stage = 300; height_stage = 600# area設定
    pygame.init()
    pygame.display.set_mode((width_stage, height_stage)) # 画面設定
    pygame.display.set_caption("トランポリン") #タイトル
    surface = pygame.display.get_surface()
    surface.fill((0,0,0)) # 画面初期化
    
    state = 0# 初期状態
    android = Android(150, 100, 40, 40, 'android', 1)# ドロイド君生成，位置(x,y)=(150, 100),大きさ(40*40)
    ground = Ground(115, 450, 10, 100, 'ground', 0)# ground
    
    while(True):
        button()# ボタン処理
        if state == 0:
            first_message(surface, "Hit space Key", 150, (255,0,0))
        
        if state == 1:
            calculation(android, ground)# 物理計算
            android.print_details()# デバッグ
            draw(surface, ground, android)# 描画処理
        
if __name__ == "__main__":
    main()