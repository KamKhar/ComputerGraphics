import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import copy
import datetime
class Digits:

    digits=\
    np.array([
        # zero
        [[159.0, 84.0, 123.0, 158.0, 131.0, 258.0],
        [139.0, 358.0, 167.0, 445.0, 256.0, 446.0],
        [345.0, 447.0, 369.0, 349.0, 369.0, 275.0],
        [369.0, 201.0, 365.0, 81.0, 231.0, 75.0]],
        # one
        [[226.0, 99.0, 230.0, 58.0, 243.0, 43.0],
        [256.0, 28.0, 252.0, 100.0, 253.0, 167.0],
        [254.0, 234.0, 254.0, 194.0, 255.0, 303.0],
        [256.0, 412.0, 254.0, 361.0, 255.0, 424.0]],
        # two
        [[152.0, 55.0, 208.0, 26.0, 271.0, 50.0],
        [334.0, 74.0, 360.0, 159.0, 336.0, 241.0],
        [312.0, 323.0, 136.0, 454.0, 120.0, 405.0],
        [104.0, 356.0, 327.0, 393.0, 373.0, 414.0]],
        # three
        [[113.0, 14.0, 267.0, 17.0, 311.0, 107.0],
        [355.0, 197.0, 190.0, 285.0, 182.0, 250.0],
        [174.0, 215.0, 396.0, 273.0, 338.0, 388.0],
        [280.0, 503.0, 110.0, 445.0, 93.0, 391.0]],
        # four
        [[249.0, 230.0, 192.0, 234.0, 131.0, 239.0],
        [70.0, 244.0, 142.0, 138.0, 192.0, 84.0],
        [242.0, 30.0, 283.0, -30.0, 260.0, 108.0],
        [237.0, 246.0, 246.0, 435.0, 247.0, 438.0]],
        # five
        [[226.0, 42.0, 153.0, 44.0, 144.0, 61.0],
        [135.0, 78.0, 145.0, 203.0, 152.0, 223.0],
        [159.0, 243.0, 351.0, 165.0, 361.0, 302.0],
        [371.0, 439.0, 262.0, 452.0, 147.0, 409.0]],
        # six
        [[191.0, 104.0, 160.0, 224.0, 149.0, 296.0],
        [138.0, 368.0, 163.0, 451.0, 242.0, 458.0],
        [321.0, 465.0, 367.0, 402.0, 348.0, 321.0],
        [329.0, 240.0, 220.0, 243.0, 168.0, 285.0]],
        # seven
        [[168.0, 34.0, 245.0, 42.0, 312.0, 38.0],
        [379.0, 34.0, 305.0, 145.0, 294.0, 166.0],
        [283.0, 187.0, 243.0, 267.0, 231.0, 295.0],
        [219.0, 323.0, 200.0, 388.0, 198.0, 452.0]],
        # eight
        [[336.0, 184.0, 353.0, 52.0, 240.0, 43.0],
        [127.0, 34.0, 143.0, 215.0, 225.0, 247.0],
        [307.0, 279.0, 403.0, 427.0, 248.0, 432.0],
        [93.0, 437.0, 124.0, 304.0, 217.0, 255.0]],
        # nine
        [[323.0, 6.0, 171.0, 33.0, 151.0, 85.0],
        [131.0, 137.0, 161.0, 184.0, 219.0, 190.0],
        [277.0, 196.0, 346.0, 149.0, 322.0, 122.0],
        [298.0, 95.0, 297.0, 365.0, 297.0, 448.0]]

    ])
    end_points=\
    np.array([
        # zero
        [254, 47],
        # one
        [138, 180],
        # two
        [104, 111],
        # three
        [96, 132],
        # four
        [374, 244],
        # five
        [340, 52],
        # six
        [301, 26],
        # seven
        [108, 52],
        # eight
        [243,242],
        # nine
        [322, 105]
    ]).astype(float)
    def __init__(self):
        pass
    def get_coords(self, digit):
        return self.digits[digit]

class Clock:

    def __init__(self, frames_to_change=10):
        self.frames_to_change=frames_to_change
        self.finish=False
        self.Digits=Digits()
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("Clock")
        self.img = np.zeros((512,1920,3), dtype=np.uint8)
        self.blank = np.zeros((512,1920,3), dtype=np.uint8)
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.im = plt.imshow(self.img, animated=True)
        self.now = datetime.datetime.now()
        self.ani = FuncAnimation(self.fig, self.plot_digit, init_func=self.init_anim, frames=self.end_clock, blit=True, interval=5)
        plt.show()
        pass

    def end_clock(self):
        ii = 0
        while not self.finish:
            ii += 1
            yield ii

    def init_anim(self):
        #текущая цифра
        self.now = datetime.datetime.now()
        self.img = np.zeros((512, 1920, 3), dtype=np.uint8)
        self.cur_digith1 = int(self.now.hour / 10)
        self.cur_digith2 = self.now.hour % 10
        self.cur_digitm1 = int(self.now.minute /10)
        self.cur_digitm2 = self.now.minute % 10
        self.cur_digits1 = int(self.now.second / 10)
        self.cur_digits2 = self.now.second % 10
        #print(self.cur_digit)
        #текущий фрейм в превращении
        self.cur_steph1 = 0
        self.cur_steph2 = 0
        self.cur_stepm1 = 0
        self.cur_stepm2 = 0
        self.cur_steps1 = 0
        self.cur_steps2 = 0
        #текущие точки
        self.current_besier_points = [self.Digits.get_coords(self.cur_digith1).copy(),
                                      self.Digits.get_coords(self.cur_digith2).copy(),
                                      self.Digits.get_coords(self.cur_digitm1).copy(),
                                      self.Digits.get_coords(self.cur_digitm2).copy(),
                                      self.Digits.get_coords(self.cur_digits1).copy(),
                                      self.Digits.get_coords(self.cur_digits2).copy()]

        self.current_end_point = [self.Digits.end_points[self.cur_digith1].copy(),
                                  self.Digits.end_points[self.cur_digith2].copy(),
                                  self.Digits.end_points[self.cur_digitm1].copy(),
                                  self.Digits.end_points[self.cur_digitm2].copy(),
                                  self.Digits.end_points[self.cur_digits1].copy(),
                                  self.Digits.end_points[self.cur_digits2].copy()]
        #текущие сдвиги по точкам
        self.current_shift_per_step_vertexes=[(self.Digits.digits[self.cur_digith1+1 if self.cur_digith1<2 else 0]-self.Digits.digits[self.cur_digith1])/self.frames_to_change,
                                              (self.Digits.digits[self.cur_digith2 + 1 if ((self.cur_digith2 < 9 and self.cur_digith1!=2) or (self.cur_digith2 < 3 and self.cur_digith1==2)) else 0] -
                                               self.Digits.digits[self.cur_digith2]) / self.frames_to_change,
                                              (self.Digits.digits[self.cur_digitm1 + 1 if self.cur_digitm1 < 5 else 0] -
                                               self.Digits.digits[self.cur_digitm1]) / self.frames_to_change,
                                              (self.Digits.digits[self.cur_digitm2 + 1 if self.cur_digitm2 < 9 else 0] -
                                               self.Digits.digits[self.cur_digitm2]) / self.frames_to_change,
                                              (self.Digits.digits[self.cur_digits1 + 1 if self.cur_digits1 < 5 else 0] -
                                               self.Digits.digits[self.cur_digits1]) / self.frames_to_change,
                                              (self.Digits.digits[self.cur_digits2 + 1 if self.cur_digits2 < 9 else 0] -
                                               self.Digits.digits[self.cur_digits2]) / self.frames_to_change]

        self.current_shift_per_step_end_point=[(self.Digits.end_points[self.cur_digith1+1 if self.cur_digith1<2 else 0]-self.Digits.end_points[self.cur_digith1])/self.frames_to_change,
                                               (self.Digits.end_points[
                                                    self.cur_digith2 + 1 if self.cur_digith2 < 9 else 0] -
                                                self.Digits.end_points[self.cur_digith2]) / self.frames_to_change,
                                               (self.Digits.end_points[
                                                    self.cur_digitm1 + 1 if self.cur_digitm1 < 5 else 0] -
                                                self.Digits.end_points[self.cur_digitm1]) / self.frames_to_change,
                                               (self.Digits.end_points[
                                                    self.cur_digitm2 + 1 if self.cur_digitm2 < 9 else 0] -
                                                self.Digits.end_points[self.cur_digitm2]) / self.frames_to_change,
                                               (self.Digits.end_points[
                                                    self.cur_digits1 + 1 if self.cur_digits1 < 5 else 0] -
                                                self.Digits.end_points[self.cur_digits1]) / self.frames_to_change,
                                               (self.Digits.end_points[
                                                    self.cur_digits2 + 1 if self.cur_digits2 < 9 else 0] -
                                                self.Digits.end_points[self.cur_digits2]) / self.frames_to_change]


        return self.im,

    def onclick(self, event):
        self.finish=True

    def casteljau(self, ar_x, ar_y, acc):
        a_x = []
        a_y = []
        for t in np.arange(0.0, 1.0, acc):
            x, y = self.casteljau_rec(ar_x, ar_y, t / (1 - t))
            a_x.append(x)
            a_y.append(y)
        a_x.append(ar_x[len(ar_x) - 1])
        a_y.append(ar_y[len(ar_y) - 1])
        return a_x,a_y

    def casteljau_rec(self,ar_x, ar_y, t):
        if (len(ar_x) == 2):
            return ((ar_x[0] + t * ar_x[1]) / (1 + t), (ar_y[0] + t * ar_y[1]) / (1 + t))
        else:
            x = []
            y = []
            for i in range(len(ar_x) - 1):
                x.append((ar_x[i] + t * ar_x[i + 1]) / (1 + t))
                y.append((ar_y[i] + t * ar_y[i + 1]) / (1 + t))
            return self.casteljau_rec(x, y, t)

    def draw_line(self, x0, y0, x1, y1):
        steep = False
        if abs(x0 - x1) < abs(y0 - y1):
            steep = True
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x1 < x0:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        k = abs(y1 - y0)
        error = 0
        y = y0

        for x in range(x0, x1 + 1):
            if (steep):
                self.img[y, x] = (255,255,255)
            else:
                self.img[x, y] = (255,255,255)
            error += k
            if ((error << 1) > x1 - x0):
                y += np.sign(y1 - y0)
                error -= x1 - x0
    def change_dig(self,num,c):
        for j in range(4):
            a_x = []
            a_y = []
            if (j != 3):
                ar_y = [self.current_besier_points[num] [3 - j][4]+c , self.current_besier_points[num] [3 - j][2]+c , self.current_besier_points[num] [3 - j][0]+c , self.current_besier_points[num] [2 - j][4]+c ]
                ar_x = [self.current_besier_points[num] [3 - j][5], self.current_besier_points[num] [3 - j][3], self.current_besier_points[num] [3 - j][1] , self.current_besier_points[num] [2 - j][5]]
            else:
                ar_x = [self.current_besier_points[num] [0][5] , self.current_besier_points [num][0][3], self.current_besier_points [num][0][1] , self.current_end_point[num][1]]
                ar_y = [self.current_besier_points[num] [0][4]+c, self.current_besier_points [num][0][2]+c,self.current_besier_points [num][0][0]+c, self.current_end_point[num][0]+c]

            a_x, a_y = self.casteljau(ar_x, ar_y, 0.1)
            for i in range(len(a_x) - 1):
                self.draw_line( int(a_x[i]), int(a_y[i]), int(a_x[i + 1]), int(a_y[i + 1]))

    def plot_digit(self, par):
        # Если нарисовали все фреймы - инициализация новой цифры
        # Иначе - запустить построение кривой безье на основе данных current_besier_points и current_end_point
        # с заданной точностью acc. Связать все полученные точки последовательно через брезенхема и нарисовать.
        # Произвести сдвиг current_besier_points и current_end_point на shift
        self.change_dig(0,-70)
        self.change_dig(1, 200)
        self.change_dig(2, 550)
        self.change_dig(3, 820)
        self.change_dig(4, 1170)
        self.change_dig(5, 1440)

        self.now = datetime.datetime.now()
        self.im.set_array(self.img)
        if(int(self.now.hour / 10) != self.cur_digith1):
            self.current_besier_points[0] += self.current_shift_per_step_vertexes[0]
            self.current_end_point[0] +=self.current_shift_per_step_end_point[0]
            self.cur_steph1 += 1
        if (self.now.hour % 10 != self.cur_digith2):
            self.current_besier_points[1] += self.current_shift_per_step_vertexes[1]
            self.current_end_point[1] += self.current_shift_per_step_end_point[1]
            self.cur_steph2 += 1
        if (int(self.now.minute /10) != self.cur_digitm1):
            self.current_besier_points[2] += self.current_shift_per_step_vertexes[2]
            self.current_end_point[2] += self.current_shift_per_step_end_point[2]
            self.cur_stepm1 += 1
        if (self.now.minute %10 != self.cur_digitm2):
            self.current_besier_points[3] += self.current_shift_per_step_vertexes[3]
            self.current_end_point[3] += self.current_shift_per_step_end_point[3]
            self.cur_stepm2 += 1
        if (int(self.now.second / 10) != self.cur_digits1):
            self.current_besier_points[4] += self.current_shift_per_step_vertexes[4]
            self.current_end_point[4] += self.current_shift_per_step_end_point[4]
            self.cur_steps1 += 1
        if (self.now.second % 10 != self.cur_digits2):
            self.current_besier_points[5] += self.current_shift_per_step_vertexes[5]
            self.current_end_point[5] += self.current_shift_per_step_end_point[5]
            self.cur_steps2 += 1
        self.img = np.zeros((512, 1920, 3), dtype=np.uint8)
        if (self.cur_steph1 == 10 or self.cur_steph2 == 10 or self.cur_stepm1 == 10 or self.cur_stepm2 == 10 or self.cur_steps1 == 10 or self.cur_steps2 == 10):
            self.init_anim()
        return self.im,




clock=Clock()
# clock.plot_digit(1)


