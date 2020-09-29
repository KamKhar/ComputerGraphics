import matplotlib.pyplot as plt
import numpy as np
import math

def shift(lst):
    min = max(lst)
    for i in lst:
        if min > i:
            min = i
    #min *= -1
    lst = [x - min for x in lst]
    return lst

def scale(lst_x,lst_y,im_size):
    lst_x = shift(lst_x)
    lst_y = shift(lst_y)

    m = max(max(lst_y), max(lst_x))
    k =100 / m
    lst_x = [int(round(x * k)) for x in lst_x]
    lst_y = [int(round(x * k)) for x in lst_y]

    return lst_x,lst_y

def draw_ventexes(img,arr,lst_f1,lst_f2,lst_f3,x,y):
    #a = np.zeros((im_size, im_size, 3))
    x -= 30
    y -=30
    for i in range(len(lst_f1)):
        img = draw_liner_good(arr[lst_f1[i]][0] + x, arr[lst_f1[i]][1] + y, arr[lst_f2[i]][0] + x, arr[lst_f2[i]][1] + y, img)
        img = draw_liner_good(arr[lst_f2[i]][0] + x, arr[lst_f2[i]][1] + y, arr[lst_f3[i]][0] + x, arr[lst_f3[i]][1] + y, img)
        img = draw_liner_good(arr[lst_f1[i]][0] + x, arr[lst_f1[i]][1] + y, arr[lst_f3[i]][0] + x, arr[lst_f3[i]][1] + y, img)

    return img
    #a = np.rot90(a, 1, axes=(0, 1))
    #plt.imshow(a)

def draw_liner_good(x0,y0,x1,y1,img):
    steep = False
    if math.fabs(x0-x1) < math.fabs(y0-y1):
        steep = True
        x0,y0 = y0,x0
        x1,y1 = y1,x1
    if x1 < x0:
        x0,x1 = x1,x0
        y0,y1 = y1,y0
    k = abs(y1 - y0)
    error = 0
    y = y0

    for x in range(x0,x1+1):
        if (x > 0 and y > 0 and x < 512 and y < 512):
            if (steep):
                img[y, x] = (255,255,255)
            else:
                img[x, y] = (255,255,255)
        error += k
        if ((error << 1) > x1 - x0):
            y += np.sign(y1 - y0)
            error -= x1 - x0


    return img
