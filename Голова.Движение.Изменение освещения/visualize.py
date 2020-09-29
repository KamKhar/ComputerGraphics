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

def cent(lst,pic_size):
    sh = int(round((pic_size - (max(lst) + min(lst)))/2))
    lst = [x + sh for x in lst]
    return lst

def scale (lst_x,lst_y,lst_z,im_size):
    lst_x = shift(lst_x)
    lst_y = shift(lst_y)
    lst_z = shift(lst_z)
    m = max(max(lst_y), max(lst_x), max(lst_z))
    k = (im_size - 1) / m
    lst_x = [int(round(x * k)) for x in lst_x]
    lst_y = [int(round(x * k)) for x in lst_y]
    lst_z = [int(round(x * k)) for x in lst_z]
    lst_x = cent(lst_x, 512)
    return lst_x, lst_y, lst_z

def draw_ventexes(deg_rot,lst_x,lst_y,lst_z,lst_f1,lst_f2,lst_f3,im_size,img):
    L = np.array([0, 0, 1])
    lst_x, lst_y, lst_z = scale(lst_x,lst_y,lst_z,im_size)
    if(deg_rot> 0):
        cos_deg = find_cos(lst_x, lst_y, lst_z, lst_f1, lst_f2, lst_f3, L)
    lst_x, lst_y, lst_z = rotat(deg_rot,lst_x,lst_y,lst_z)
    img.fill(0)
    if(deg_rot <= 0):
        cos_deg = find_cos(lst_x, lst_y, lst_z, lst_f1, lst_f2, lst_f3,L)
    for i in range(len(lst_f1)):
        if (cos_deg[i] > 0):
            color = (int(round(255 * cos_deg[i])),int(round(255 * cos_deg[i])),int(round(255 * cos_deg[i])))
            img = draw_liner_good(lst_x[lst_f1[i]], lst_y[lst_f1[i]], lst_x[lst_f2[i]], lst_y[lst_f2[i]], img,color)
            img = draw_liner_good(lst_x[lst_f2[i]], lst_y[lst_f2[i]], lst_x[lst_f3[i]], lst_y[lst_f3[i]], img,color)
            img = draw_liner_good(lst_x[lst_f1[i]], lst_y[lst_f1[i]], lst_x[lst_f3[i]], lst_y[lst_f3[i]], img,color)

            img = color_pic(i, lst_x, lst_y, lst_f1, lst_f2, lst_f3, color,img)

    img = np.rot90(img, 1, axes=(0, 1))
    return img

def rotat(deg_rot,lst_x,lst_y,lst_z):

    P = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [-256, 0, 0, 1]])

    R = np.array([[np.cos(np.radians(deg_rot)), 0, -np.sin(np.radians(deg_rot)), 0],
                  [0, 1, 0, 0],
                  [np.sin(np.radians(deg_rot)), 0, np.cos(np.radians(deg_rot)), 0],
                  [0, 0, 0, 1]])

    P1 = np.array([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [256, 0, 0, 1]])
    for i in range(len(lst_x)):
        A = np.array([lst_x[i], lst_y[i], lst_z[i], 1])
        A = A.dot(P)
        A = A.dot(R)
        A = A.dot(P1)
        lst_x[i] = A[0]
        lst_y[i] = A[1]
        lst_z[i] = A[2]

    lst_x = [int(round(x)) for x in lst_x]
    lst_y = [int(round(x)) for x in lst_y]
    lst_z = [int(round(x)) for x in lst_z]
    lst_x = cent(lst_x, 512)


    return lst_x,lst_y,lst_z

def find_cos(lst_x,lst_y,lst_z,lst_f1,lst_f2,lst_f3,L):

    cos_deg = []
    for i in range(len(lst_f1)):
        ab = np.array([lst_x[lst_f2[i]] - lst_x[lst_f1[i]],
                       lst_y[lst_f2[i]] - lst_y[lst_f1[i]],
                       lst_z[lst_f2[i]] - lst_z[lst_f1[i]]])
        ac = np.array([lst_x[lst_f3[i]] - lst_x[lst_f1[i]],
                       lst_y[lst_f3[i]] - lst_y[lst_f1[i]],
                       lst_z[lst_f3[i]] - lst_z[lst_f1[i]]])

        N = np.array([ab[1] * ac[2] - ab[2] * ac[1],
                      ab[2] * ac[0] - ab[0] * ac[2],
                      ab[0] * ac[1] - ab[1] * ac[0]])
        len_N = math.sqrt(N[0] * N[0] + N[1] * N[1] + N[2] * N[2])
        len_L = math.sqrt(L[0] * L[0] + L[1] * L[1] + L[2] * L[2])
        if(len_N != 0):
            cos_deg.append((L[0]/len_L * (N[0] / len_N)) + (L[1]/len_L * (N[1] / len_N)) + (L[2]/len_L * (N[2] / len_N)))
        else:
            cos_deg.append(0)
    return cos_deg

def color_pic(i,lst_x,lst_y,lst_f1,lst_f2,lst_f3,color,img):
    for q in range(min([lst_x[lst_f1[i]], lst_x[lst_f2[i]], lst_x[lst_f3[i]]]),
                   max([lst_x[lst_f1[i]], lst_x[lst_f2[i]], lst_x[lst_f3[i]]])):
        for j in range(min([lst_y[lst_f1[i]], lst_y[lst_f2[i]], lst_y[lst_f3[i]]]),
                       max([lst_y[lst_f1[i]], lst_y[lst_f2[i]], lst_y[lst_f3[i]]])):
            if (q < 512) and (j < 512) and (q > 0) and (j > 0):
                a = (lst_x[lst_f1[i]] - q) * (lst_y[lst_f2[i]] - lst_y[lst_f1[i]]) - \
                    (lst_x[lst_f2[i]] - lst_x[lst_f1[i]]) * (lst_y[lst_f1[i]] - j)
                b = (lst_x[lst_f2[i]] - q) * (lst_y[lst_f3[i]] - lst_y[lst_f2[i]]) - \
                    (lst_x[lst_f3[i]] - lst_x[lst_f2[i]]) * (lst_y[lst_f2[i]] - j)
                c = (lst_x[lst_f3[i]] - q) * (lst_y[lst_f1[i]] - lst_y[lst_f3[i]]) - \
                    (lst_x[lst_f1[i]] - lst_x[lst_f3[i]]) * (lst_y[lst_f3[i]] - j)
                if (((a > 0 and b > 0 and c > 0) or (a < 0 and b < 0 and c < 0))):
                    img[q][j] = color
    return img

def draw_liner_good(x0,y0,x1,y1,img,color):
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
        if (steep):
            img[y, x] = color
        else:
            img[x, y] = color
        error += k
        if ((error << 1) > x1 - x0):
            y += np.sign(y1 - y0)
            error -= x1 - x0

    return img