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
K = 5        # ばね定数 [n/m]
 
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
 
class Ceiling:
    def __init__(self):
        self.pos1 = Vec2(0, 30)
        self.pos2 = Vec2(WINDOW_W, 35)
        self.color = 12 # blue
 
class Spring:
    def __init__(self):
        self.pos1 = Vec2(0, 0)
        self.pos2 = Vec2(0, 0)
        self.color = 12 # blue
 
    def update(self, x1, y1, x2, y2, color):
        self.pos1.x = x1
        self.pos1.y = y1
        self.pos2.x = x2
        self.pos2.y = y2
        self.color = color
 
class App:
    def __init__(self):
        self.IMG_ID0_X = 60
        self.IMG_ID0_Y = 65
        self.IMG_ID0 = 0
        self.IMG_ID1 = 1
        # self.IMG_ID2 = 2
 
        pyxel.init(WINDOW_W, WINDOW_H, fps = FPS, caption="Hello Pyxel")
        pyxel.image(self.IMG_ID0).load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.image(self.IMG_ID1).load(0, 0, "assets/cat_16x16.png")
 
        pyxel.mouse(True)
 
        # make instance
        self.Cats = []
        self.Springs = []
        self.ceiling = Ceiling()
 
        pyxel.run(self.update, self.draw)
 
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
 
        # ====== ctrl cat ======
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            new_cat = cat(self.IMG_ID1)
            new_cat.update(pyxel.mouse_x, pyxel.mouse_y, new_cat.vec)
            self.Cats.append(new_cat)
 
            new_spring = Spring()
            self.Springs.append(new_spring)
 
        cat_count = len(self.Cats)
        for i in range(cat_count):
            if self.Cats[i].pos.y < WINDOW_H:
                # ばね変位：x（猫のｙ座標 - 天井のｙ座標）
                x = self.Cats[i].pos.y - self.ceiling.pos2.y
                # f = m * g - k * x（重力 - 復元力）
                f = self.Cats[i].weight * G - K * x
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
 
                # Spring update
                self.Springs[i].update(self.Cats[i].pos.x + CAT_W / 2, 
                                        self.ceiling.pos2.y, 
                                        self.Cats[i].pos.x + CAT_W / 2, 
                                        self.Cats[i].pos.y,
                                        pyxel.frame_count % 16)
 
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
 
        # ======= draw springs ========
        for springs in self.Springs:
            pyxel.line(springs.pos1.x, springs.pos1.y, 
                       springs.pos2.x, springs.pos2.y, 
                       springs.color)
 
        # ======= draw ceiling ========
        pyxel.rect(self.ceiling.pos1.x, self.ceiling.pos1.y, 
                    self.ceiling.pos2.x, self.ceiling.pos2.y, 
                    self.ceiling.color)
 
App()