import pyxel
# ====== Image parameters ======
WINDOW_H = 120
WINDOW_W = 160
CAT_H = 16
CAT_W = 16
 
# ===== Physical parameters =====
FPS = 30     # フレームレート [f/s]
DT = 1 / FPS # ステップ時間 [s]
G = 9.8      # 重力加速度 [kg.m/s^2]
K = 10       # ばね定数 [N/m]

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
 
class cat:
    def __init__(self, img_id):
        self.pos = Vec2(0, 0)
        self.vec = 0
        self.vel = 0
        self.weight = 1
        self.time = 0
        self.img_cat = img_id
 
    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx
 
class Ground:
    def __init__(self):
        self.pos1 = Vec2(30, WINDOW_H - 20)
        self.pos2 = Vec2(WINDOW_W - 30, WINDOW_H)
        self.color = 14 # pink
 
class App:
    def __init__(self):
        self.IMG_ID0_X = 60
        self.IMG_ID0_Y = 65
        self.IMG_ID0 = 0
        self.IMG_ID1 = 1
        # self.IMG_ID2 = 2
 
        pyxel.init(WINDOW_W, WINDOW_H, fps = FPS, caption="Hello Pyxel")
        pyxel.image(self.IMG_ID0).load(0, 0, "pyxel_logo_38x16.png")
        pyxel.image(self.IMG_ID1).load(0, 0, "cat_16x16.png")
 
        pyxel.mouse(True)
 
        # make instance
        self.Cats = []
        self.ground = Ground()
 
        # self.mouse_count = 0
 
        pyxel.run(self.update, self.draw)
 
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
 
        # ====== ctrl cat ======
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            new_cat = cat(self.IMG_ID1)
 
            new_cat.update(pyxel.mouse_x, pyxel.mouse_y, new_cat.vec)
            self.Cats.append(new_cat)
 
        cat_count = len(self.Cats)
        for i in range(cat_count):
            if self.Cats[i].pos.y < WINDOW_H:
                # f = m * g （自由落下）
                f = self.Cats[i].weight * G
 
                # トランポリンに衝突
                if ((self.ground.pos1.y <= self.Cats[i].pos.y + CAT_H)
                     and(self.ground.pos1.x <= self.Cats[i].pos.x + CAT_W)
                     and (self.Cats[i].pos.x <= self.ground.pos2.x)):
                    x = self.Cats[i].pos.y + CAT_H - self.ground.pos1.y
                    # f = m * g - k * x （重力 - 復元力）
                    f += -K * x
 
                # a = f / m （ニュートンの運動方程式）
                alpha = f / self.Cats[i].weight
                # v += a * dt （積分：加速度 ⇒ 速度）
                self.Cats[i].vel += alpha * DT
                # y += v * dt (積分：速度 ⇒ 位置)
                self.Cats[i].pos.y += self.Cats[i].vel * DT
                # 経過時間
                self.Cats[i].time += DT
 
                # debug
                print("Cat No.", i)
                print("v = ", self.Cats[i].vel)
                print("y = ", self.Cats[i].pos.y)
                print("f = ", f)
 
                # Cat update
                self.Cats[i].update(self.Cats[i].pos.x, 
                                    self.Cats[i].pos.y, 
                                    self.Cats[i].vec)
            else:
                del self.Cats[i]
                break
 
    def draw(self):
        pyxel.cls(0)
        pyxel.text(55, 40, "Are you Kururu?", pyxel.frame_count % 16)
        pyxel.blt(self.IMG_ID0_X, self.IMG_ID0_Y, self.IMG_ID0, 0, 0, 38, 16)
 
        # ======= draw cat ========
        for cats in self.Cats:
            pyxel.blt(cats.pos.x, cats.pos.y, cats.img_cat, 0, 0, CAT_W, CAT_H, 5)
 
        # ======= draw ground ========
        pyxel.rect(self.ground.pos1.x, self.ground.pos1.y, 
                    self.ground.pos2.x, self.ground.pos2.y, 
                    self.ground.color)
 
App()