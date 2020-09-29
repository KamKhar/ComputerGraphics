import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import core
import visualize
#класс игры
class Game:

    def __init__(self, pic_size=512):
        # сохранили параметр как поле класса
        self.pic_size=pic_size
        # проверяет нужно ли завершить игру
        self.finish = False
        # готовит окна
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("Game")
        # TODO считать вершины и грани. Адаптировать размер вершин


        pass

        # Обработчик на клик мышкой-выстрел
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        # подготовка изображения-массива
        self.img = np.zeros((pic_size,pic_size,3), dtype=np.uint8)
        self.lst_x = []
        self.lst_y = []
        self.lst_f1 = []
        self.lst_f2 = []
        self.lst_f3 = []

        core.read_vertexes('small_teapot.obj', self.lst_x, self.lst_y, self.lst_f1, self.lst_f2, self.lst_f3)
        print(self.lst_f2)
        self.lst_x, self.lst_y = visualize.scale(self.lst_x, self.lst_y, pic_size)
        self.xy1 = np.array([self.lst_x, self.lst_y]).transpose()
        self.xy1 = core.vertexes_to_projective(self.xy1)
        self.xy = self.xy1
        #print(self.xy)
        self.ugl = 0
        self.tap = 0
        self.delugl = 0
        # визуализация с анимацией
        self.im = plt.imshow(self.img, animated=True)
        # запуск анимации
        # self.fig - окно для анимации
        # self.update - функция отрисовки каждого кадра
        # self.init_target - функция, которая отработает перед запуском анимациии
        # self.end_game - функция-обман для matplotlib. Matplotlib требует точного количества кадров для завершения анимации. Мы же сделаем бесконечный генератор.
        # interval - количество миллисекунд, после которых снова вызывается функция self.update
        self.ani = FuncAnimation(self.fig, self.update, init_func=self.init_target, frames=self.end_game, blit=True, interval=15)
        plt.show()

    #остановит игру
    def end_game(self):
        i = 0
        while not self.finish:
            i += 1
            yield i
    #функция инициализациии полета
    def init_target(self, x0=0, y0=None, alpha=None, v0=None):
        """
        Эмулирует полёт под углом к горизонту с ускорением свободного падения
        :param x0: стартовая координата x тела
        :param y0: стартовая координата y тела
        :param alpha: угол в градусах по отношегнию к горизонту
        :param v0: начальная скорость
        :return:
        """
        # Обнулили поле
        self.img=np.zeros((self.pic_size,self.pic_size,3), dtype=np.uint8)
        # Если в функцию не передали такой параметр, генерируем случаную координату y
        if y0 is None:
            y0 = np.random.randint(0, self.pic_size)
        # то же самое с углом
        if alpha is None:
            alpha = np.deg2rad(np.random.randint(-50, -20))
        # и со скоростью
        if v0 is None:
            v0 = np.random.randint(20, 50)
        # фиксируем начальное время - оно понадобится для вычисленния новых координат
        self.t = time.time()
        self.v0 = v0
        self.x0 = x0
        self.y0 = y0
        self.alpha = alpha
        # неземное ускорение свободного падения
        self.g = 3 * 9.8
        # начальные проекции скоростей
        self.vx = self.v0 * np.cos(self.alpha)
        self.vy = self.v0 * np.sin(self.alpha)

        return self.im,

    # функция отрисовки
    def update(self, par):

        # посмотрели сколько прошло времени с момента запуска снаряда
        cur_t = time.time() - self.t
        # пересчитали положение снаряда
        cur_x = self.x0 + self.v0 * cur_t * np.cos(self.alpha)
        cur_y = self.y0 + self.v0 * cur_t * np.sin(self.alpha) - self.g * cur_t * cur_t / 2
        #T = np.array([[1, 0, cur_x], [0, 1, cur_y], [0, 0, 1]]) - матрица перемещения
        if (self.delugl>0):
            self.delugl-=0.1
        #assert isinstance(self.xy, object)
        #self.xy = T.dot(self.xy)
        # если вышли за вертикальные пределы изображения или каким-то образом влево - проиграли
        # TODO закончить условие проигрыша
        if cur_x < 0 or cur_y < 0 or cur_y >= self.pic_size or cur_x >= self.pic_size:
            self.tap = 0
            self.delugl = 0
            self.ugl = 0
            self.xy = self.xy1
            self.init_target()
            print(self.xy)
            # self.finish=True
            return self.im,
        # # если просто вышли за пределы правой части экрана - запускам новый снаряд
        # if cur_x >= self.pic_size:
        #     self.init_target()
        #     return self.im,
        self.last_x=int(cur_x)
        self.last_y=int(cur_y)
        # TODO отрисовка чайника, летящего по параболической траектории и прочие плюшки (о них ниже)

        pass
        #рисуем снаряд
        self.img = np.zeros((self.pic_size, self.pic_size, 3), dtype=np.uint8)

        self.ugl += self.delugl
        #V1 = np.array([1,0,0],[0, 1 ,0],[-self.xy[5][0],-self.xy[5][1],1])
        #V2 = np.array([1,0,0],[0, 1 ,0],[self.xy[5][0],self.xy[5][1],1])
        R = np.array([[np.cos(np.radians(self.ugl)),-np.sin(np.radians(self.ugl)),0],
                      [np.sin(np.radians(self.ugl)),np.cos(np.radians(self.ugl)),0],
                     [0,0,1]])
        #V1 = V1.dot(R).astype(np.int64)
        #V1 = V1.dot(V2).astype(np.int64)
        self.xy = self.xy1.dot(R).astype(np.int64)

        if (self.tap >= 2):
            T = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]])
            self.xy = self.xy.dot(T).astype(np.int64)
        #print(self.xy)
        self.img = visualize.draw_ventexes(self.img,self.xy,self.lst_f1,self.lst_f2,self.lst_f3,self.last_x,self.last_y)
        #self.img[self.last_x, self.last_y] = (255, 255, 255)
        # запомнили скорости текущие
        self.vx = self.v0 * np.cos(self.alpha)
        self.vy = self.v0 * np.sin(self.alpha) - self.g * cur_t

        #обновили буфер отрисовки
        self.im.set_array(np.rot90(self.img))
        return self.im,

    # функция выстрела
    def onclick(self, event):
        # задали размер хитбокса
        heat_box = 20
        # вывели дебаг информацию
        print(self.last_x, self.last_y, event.xdata, event.ydata, self.vx, self.vy)
        # Если кликнули в место, где сейчас летит снаряд
        if self.last_x - heat_box < event.xdata and event.xdata < self.last_x + heat_box and \
                self.pic_size-self.last_y - heat_box < event.ydata and event.ydata < self.pic_size-self.last_y + heat_box:
            # придать ему доп скорость и подкинуть от текущего положения
            #TODO также заставить чайник вращаться, чайник должен вращаться быстро, а спустя некторое время замедлять вращение и вовсе его прекращать
            #TODO после второго попадания по тому же чайнику, увеличить его размер в два раза, сохранив текущую ориентацию вращения
            self.delugl += 15
            self.tap += 1
            self.init_target(self.last_x, self.last_y, np.deg2rad(45), self.v0 + np.abs(self.vx))


gg=Game()
