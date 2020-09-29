from PIL import Image as Im #Работа с графическими изображениями
import tkinter #Работа с GUI
import numpy as np #Работа с массивами
import matplotlib
import matplotlib.pyplot as plt #Вывод на экран
import random


root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
pic_size = min(int(width/2), int(height/2))
print ("Pic size: (%s,%s)" % (pic_size, pic_size))

def show_image(image):
    # plt.imshow(image, cmap="gray")
    plt.imshow(image, cmap="gray", interpolation="none")
    plt.show()

def build_catmul_rom(vertexes, steps):
    pass

def build_ermit_spline(image, vertexes, derivatives, steps):
    for i in range(len(vertexes) - 1):
        A = np.array([[vertexes[i][0]**3,vertexes[i][0] ** 2, vertexes[i][0],1],
                     [vertexes[i+1][0]**3,vertexes[i+1][0] **2,vertexes[i+1][0],1],
                     [(3*vertexes[i][0])**2,2*vertexes[i][0],1,0],
                     [(3*vertexes[i+1][0])**2,2*vertexes[i+1][0],1,0]])
        print(A)
        A_1 = np.linalg.inv(A)
        B = np.array([[vertexes[i][1]],[vertexes[i+1][1]],[derivatives[i]],[derivatives[i+1]]])
        K = A_1.dot(B)
        d = abs(vertexes[i][0] - vertexes[i+1][0])/steps
        for j in range(steps):
            y1 = K[0][0] * ((vertexes[i][0] + d*j)**3) + K[1][0] * ((vertexes[i][0] + d*j)**2) + K[2][0] * (vertexes[i][0] + d*j) + K[3][0]
            y2 = K[0][0] * ((vertexes[i][0] + d*(j + 1))**3) + K[1][0] * ((vertexes[i][0] + d*(j + 1))**2) + K[2][0] * (vertexes[i][0] + d*(j + 1)) + K[3][0]
            draw_line_bad_float(image, int(round((vertexes[i][0] + d*j)*100)), int(y1*100), int(round((vertexes[i][0] + d*(j + 1))*100)), int(round(y2 *100 )), (255,255,255))

def prepare_image():
    img = np.zeros(shape=(pic_size+1,pic_size+1, 3)).astype(np.uint8)
    return img

def vertexes_renderer(img, vertexes, color):
    for vertex in vertexes:
        img[tuple(vertex[:2])]=color
    return img

def draw_line_bad_float(img, x0, y0, x1, y1, color):
    steep = False
    #если ширина меньше высоты
    if (abs(x0 - x1) < abs(y0 - y1)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    #если первая координата больше второй
    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    for x in range(x0, x1+1):
        if x1==x0:
            t = 0
        else:
            t = (x-x0) / (x1-x0)
        y = int(round(y0 * (1.-t) + y1 * t))
        #поменяли коорды, при отрисовке меняем обратно
        if (steep):
            img[x, y]=color
        else:
            img[y, x] = color

if __name__=="__main__":
    print(width, height)
