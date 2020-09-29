import visualize
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import core
import copy
class Face:
    def __init__(self, pic_size=512):
        self.pic_size=pic_size
        self.finish = False
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("Face")
        self.deg = 0
        self.del_deg = 15
        # Обработчик на клик мышкой-выстрел
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        # подготовка изображения-массива
        self.img = np.zeros((pic_size,pic_size,3), dtype=np.uint8)
        self.lst_x = []
        self.lst_y = []
        self.lst_z = []
        self.lst_f1 = []
        self.lst_f2 = []
        self.lst_f3 = []
        core.read_vertexes('face.obj', self.lst_x, self.lst_y, self.lst_z, self.lst_f1, self.lst_f2, self.lst_f3)
        # визуализация с анимацией
        self.im = plt.imshow(self.img, animated=True)
        self.ani = FuncAnimation(self.fig, self.update, init_func=self.init_anim, frames=self.end_face, blit=True, interval=15)
        plt.show()

    def onclick(self, event):
        self.finish = True

    def end_face(self):
        ii = 0
        while not self.finish:
            ii += 1
            yield ii

    def init_anim(self):
        pass
        return self.im,

    def update(self, par):
        self.img = visualize.draw_ventexes(self.deg,self.lst_x, self.lst_y,self.lst_z, self.lst_f1, self.lst_f2, self.lst_f3, 512, self.img)
        if abs(self.deg) == 360:
            self.deg = 0
            self.del_deg *= -1
        self.deg -= self.del_deg
        #обновили буфер отрисовки
        self.im.set_array(self.img)
        return self.im,


face=Face()