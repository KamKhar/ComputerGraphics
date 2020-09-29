import matplotlib.pyplot as plt
import numpy as np
import math
import core
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
    #lst_x = shift(lst_x)
    #lst_y = shift(lst_y)
    m = max(max(lst_y) - min(lst_y), max(lst_x)-min(lst_x))
    k = (im_size - 1) / m

    lst_x = [(x * k) for x in lst_x]
    lst_y = [(x * k) for x in lst_y]
    lst_z = [((x) * k)+250 for x in lst_z]
    #lst_z = shift(lst_z)
    #lst_x = cent(lst_x, 512)
    return lst_x, lst_y, lst_z

def draw_ventexes(deg_rot,lst_x,lst_y,lst_z,lst_f1,lst_f2,lst_f3,lst_t1,lst_t2,lst_t3,lst_n1,lst_n2,lst_n3,lst_vn1,lst_vn2,lst_vn3,lst_u,lst_v,img_np,im_size,img):
    L = np.array([0, 0, -1])
    V = np.array(([0,0,-1]))
    lst_x, lst_y, lst_z = scale(lst_x,lst_y,lst_z,im_size)

    lst_x, lst_y, lst_z, lst_vn1, lst_vn2, lst_vn3 = Local_to_Global(lst_x,lst_y,lst_z,lst_vn1,lst_vn2,lst_vn3)

    lst_x, lst_y, lst_z, lst_vn1, lst_vn2, lst_vn3 = Cam_rotat(deg_rot,lst_x,lst_y,lst_z,lst_vn1,lst_vn2,lst_vn3,L)
    img.fill(0)

    lst_x, lst_y, lst_z, lst_vn1, lst_vn2, lst_vn3,w,h,b = Persp(lst_x, lst_y, lst_z,lst_vn1,lst_vn2,lst_vn3)

    lst_x,lst_y,lst_z = Viewport(lst_x,lst_y,lst_z,512,512,b)
    z = np.ones((512,512)) * 512000
    cos_deg = find_cos(lst_x, lst_y, lst_z, lst_f1, lst_f2, lst_f3, L)
    img = color_pic(z, lst_x, lst_y,lst_z, lst_f1, lst_f2, lst_f3 ,lst_t1,lst_t2,lst_t3,lst_n1,lst_n2,lst_n3,lst_vn1,lst_vn2,lst_vn3,lst_u,lst_v, cos_deg,img,img_np,L,V)
    img = np.rot90(img, 1, axes=(0, 1))
    return img

def Ortograth(lst_x,lst_y,lst_z):
    l, r, b, t, f, n = min(lst_x), max(lst_x), min(lst_y), max(lst_y), min(lst_z), max(lst_z)
    A = np.array([lst_x, lst_y, lst_z, np.ones(len(lst_z))])
    print(n)
    M_ort = np.array([[(2*n) / (r - l), 0, 0, -(r + l) / (r - l)],
                     [0, (2*n) / (t - b), 0, -(t + b) / (t - b)],
                     [0, 0, -(f + n) / (f - n), (2*f*n) / (f - n)],
                     [0, 0, -1, 0]])

    A = M_ort.dot(A)
    print(A[3])
    lst_x = A[0]/A[3]
    lst_y = A[1]/A[3]
    lst_z = A[2]/A[3]
    print("d")
    return lst_x, lst_y, lst_z

def Viewport1(lst_x,lst_y,w,h):
    A = np.array([lst_x, lst_y,np.ones(len(lst_x))])
    M_vp = np.array([[w/2,0,w/2],[0,h/2,h/2],[0,0,0]])
    A = M_vp.dot(A)
    lst_x = A[0]
    lst_y = A[1]
    lst_x = [int(round(x)) for x in lst_x]
    lst_y = [int(round(x)) for x in lst_y]
    lst_x = cent(lst_x, 512)
    return lst_x, lst_y
def Local_to_Global(lst_x,lst_y,lst_z,lst_vn1,lst_vn2,lst_vn3):
    A = np.array([lst_x, lst_y, lst_z, np.ones(len(lst_z))])
    M_ltg = np.eye(4)
    M_nor = np.array([lst_vn1, lst_vn2, lst_vn3, np.ones(len(lst_vn3))])
    M_nor = ((np.linalg.inv(M_ltg).transpose())).dot(M_nor)
    lst_vn1 = M_nor[0]
    lst_vn2 = M_nor[1]
    lst_vn3 = M_nor[2]
    A = M_ltg.dot(A)
    lst_x = A[0]
    lst_y = A[1]
    lst_z = A[2]
    return lst_x,lst_y,lst_z,lst_vn1,lst_vn2,lst_vn3

def Cam_rotat(deg_rot,lst_x,lst_y,lst_z,lst_vn1,lst_vn2,lst_vn3,L):

    P = np.array([[1, 0, 0, -(max(lst_x) + min(lst_x)) / 2],
                  [0, 1, 0, -(max(lst_y) + min(lst_y)) / 2],
                  [0, 0, 1, -(max(lst_z) + min(lst_z)) / 2],
                  [0, 0, 0, 1]])

    R = np.array([[np.cos(np.radians(deg_rot)), 0, -np.sin(np.radians(deg_rot)), 0],
                  [0, 1, 0, 0],
                  [np.sin(np.radians(deg_rot)), 0, np.cos(np.radians(deg_rot)), 0],
                  [0, 0, 0, 1]])

    P1 = np.array([[1, 0, 0, (max(lst_x) + min(lst_x)) / 2],
                   [0, 1, 0, (max(lst_y) + min(lst_y)) / 2],
                   [0, 0, 1, (max(lst_z) + min(lst_z)) / 2],
                   [0, 0, 0, 1]])
    #L1 = np.array([L[0],L[1],L[2],1])
    A = np.array([lst_x, lst_y, lst_z, np.ones(len(lst_z))])
    A = P1.dot(R.dot(P.dot(A)))
    M_nor = np.array([lst_vn1, lst_vn2, lst_vn3, np.ones(len(lst_vn3))])
    M_nor = ((np.linalg.inv(R).transpose())).dot(M_nor)
    lst_vn1 = M_nor[0]
    lst_vn2 = M_nor[1]
    lst_vn3 = M_nor[2]
    #L1 = P1.dot(R.dot(P.dot(L1)))
    lst_x = A[0]
    lst_y = A[1]
    lst_z = A[2]
    #L[0] = L1[0]
    #L[1] = L1[1]
    #L[2] = L1[2]
    lst_x = [int(round(x)) for x in lst_x]
    lst_y = [int(round(x)) for x in lst_y]
   # lst_y = shift(lst_y)
    #lst_z = shift(lst_z)
    lst_z = [int(round(x )) for x in lst_z]
    #lst_x = cent(lst_x, 512)
    return lst_x, lst_y, lst_z, lst_vn1, lst_vn2, lst_vn3

def Persp(lst_x,lst_y,lst_z,lst_vn1,lst_vn2,lst_vn3):
    l, r, b, t, f, n = -256, 256, -256,256, 570, 70
    A = np.array([lst_x, lst_y, lst_z, np.ones(len(lst_z))])
    M_ort = np.array([[2 * n / (r - l), 0, (r + l) / (r - l), 0],
                     [0, 2 * n / (t - b), (t + b) / (t - b), 0],
                     [0, 0, (f + n) / (f - n), -2 * f * n / (f - n)],
                     [0, 0, 1, 0]], dtype=np.float64)
    #M_nor = np.array([lst_vn1, lst_vn2, lst_vn3, np.ones(len(lst_vn3))])
    #M_nor = ((np.linalg.inv(M_ort).transpose())).dot(M_nor)
    #lst_vn1 = M_nor[0]
    #lst_vn2 = M_nor[1]
    #lst_vn3 = M_nor[2]
    A = M_ort.dot(A)
    lst_x = A[0]/A[3]
    lst_y = A[1]/A[3]
    lst_z = A[2]/A[3]
    return lst_x, lst_y, lst_z,lst_vn1,lst_vn2,lst_vn3,r-l,t-b,f-n

def Viewport(lst_x,lst_y,lst_z,w,h,b):
    A = np.array([lst_x, lst_y,np.ones(len(lst_x))])
   # M_vp = np.array([[w/2,0,w/2],[0,h/2,h/2],[0,0,0]])
   # A = M_vp.dot(A)
   # lst_x = A[0]
    #lst_y = A[1]
    print(lst_x)
    for i in range(len(lst_z)):
        lst_x[i] = lst_x[i]*w/2 + w/2
        lst_y[i] = lst_y[i]*h/2 + h/2
        lst_z[i] = lst_z[i]*b/2 + b/2
    lst_x = [int(round(x)) for x in lst_x]
    print(lst_x)
    lst_y = [int(round(x)) for x in lst_y]
    lst_x = cent(lst_x, 512)
    return lst_x, lst_y,lst_z

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

def find_cos2point(x,y,z,L):
    N = np.array([x,y,z])
    len_N = math.sqrt(N[0] * N[0] + N[1] * N[1] + N[2] * N[2])
    len_L = math.sqrt(L[0] * L[0] + L[1] * L[1] + L[2] * L[2])
    cos = (L[0]/len_L * (N[0] / len_N)) + (L[1]/len_L * (N[1] / len_N)) + (L[2]/len_L * (N[2] / len_N))
    return cos

def color_pic(z,lst_x,lst_y,lst_z,lst_f1,lst_f2,lst_f3,lst_t1,lst_t2,lst_t3,lst_n1,lst_n2,lst_n3,lst_vn1,lst_vn2,lst_vn3,lst_u,lst_v,cos_deg,img,img_np,L,V):

    for i in range(len(lst_f1)):
        if (cos_deg[i] > 0):

            #img,z = draw_liner_good(z,lst_x[lst_f1[i]], lst_y[lst_f1[i]], lst_z[lst_f1[i]], lst_x[lst_f2[i]], lst_y[lst_f2[i]], lst_z[lst_f2[i]], img,color)
            #img,z = draw_liner_good(z,lst_x[lst_f2[i]], lst_y[lst_f2[i]], lst_z[lst_f2[i]], lst_x[lst_f3[i]], lst_y[lst_f3[i]], lst_z[lst_f3[i]], img,color)
            #img,z = draw_liner_good(z,lst_x[lst_f1[i]], lst_y[lst_f1[i]], lst_z[lst_f1[i]], lst_x[lst_f3[i]], lst_y[lst_f3[i]], lst_z[lst_f3[i]], img,color)

            for q in range(min([lst_x[lst_f1[i]], lst_x[lst_f2[i]], lst_x[lst_f3[i]]]),
                           max([lst_x[lst_f1[i]], lst_x[lst_f2[i]], lst_x[lst_f3[i]]])+ 1):
                for j in range(min([lst_y[lst_f1[i]], lst_y[lst_f2[i]], lst_y[lst_f3[i]]]),
                               max([lst_y[lst_f1[i]], lst_y[lst_f2[i]], lst_y[lst_f3[i]]]) + 1):
                    if (q < 512) and (j < 512) and (q > 0) and (j > 0):
                        c = ((j - lst_y[lst_f1[i]]) * (lst_x[lst_f2[i]] - lst_x[lst_f1[i]]) - \
                             (q - lst_x[lst_f1[i]]) * (lst_y[lst_f2[i]] - lst_y[lst_f1[i]])) / (
                                    (lst_y[lst_f3[i]] - lst_y[lst_f1[i]]) * (lst_x[lst_f2[i]] - lst_x[lst_f1[i]]) -
                                    (lst_x[lst_f3[i]] - lst_x[lst_f1[i]]) * (lst_y[lst_f2[i]] - lst_y[lst_f1[i]]))
                        b = ((j - lst_y[lst_f1[i]]) * (lst_x[lst_f3[i]] - lst_x[lst_f1[i]]) - \
                             (q - lst_x[lst_f1[i]]) * (lst_y[lst_f3[i]] - lst_y[lst_f1[i]])) / (
                                    (lst_y[lst_f2[i]] - lst_y[lst_f1[i]]) * (lst_x[lst_f3[i]] - lst_x[lst_f1[i]]) -
                                    (lst_x[lst_f2[i]] - lst_x[lst_f1[i]]) * (lst_y[lst_f3[i]] - lst_y[lst_f1[i]]))
                        a = ((j - lst_y[lst_f3[i]]) * (lst_x[lst_f2[i]] - lst_x[lst_f3[i]]) - \
                             (q - lst_x[lst_f3[i]]) * (lst_y[lst_f2[i]] - lst_y[lst_f3[i]])) / (
                                    (lst_y[lst_f1[i]] - lst_y[lst_f3[i]]) * (lst_x[lst_f2[i]] - lst_x[lst_f3[i]]) -
                                    (lst_x[lst_f1[i]] - lst_x[lst_f3[i]]) * (lst_y[lst_f2[i]] - lst_y[lst_f3[i]]))
                        if (((a >= 0 and b >= 0 and c >= 0) or (a <= 0 and b <= 0 and c <= 0)) ):

                            z1 = 1 / (a * (1 / lst_z[lst_f1[i]]) + b * (1 / lst_z[lst_f2[i]]) + c * (
                                    1 / lst_z[lst_f3[i]]))

                            if (z[q][j] > z1):
                                z[q][j] = z1
                                xx = a * lst_vn1[lst_n1[i]] + b * lst_vn1[lst_n2[i]] + c * lst_vn1[lst_n3[i]]
                                yy = a * lst_vn2[lst_n1[i]] + b * lst_vn2[lst_n2[i]] + c * lst_vn2[lst_n3[i]]
                                zz = a * lst_vn3[lst_n1[i]] + b * lst_vn3[lst_n2[i]] + c * lst_vn3[lst_n3[i]]
                                u = z1 * ((a*lst_u[lst_t1[i]]*(1 / lst_z[lst_f1[i]])) + (b * lst_u[lst_t2[i]]* (1 / lst_z[lst_f2[i]])) + (c * lst_u[lst_t3[i]]* (1 / lst_z[lst_f3[i]])))
                                v = z1 * ((a*lst_v[lst_t1[i]]*(1 / lst_z[lst_f1[i]])) + (b * lst_v[lst_t2[i]]* (1 / lst_z[lst_f2[i]])) + (c * lst_v[lst_t3[i]]* (1 / lst_z[lst_f3[i]])))
                                w,h = len(img_np),len(img_np[0])
                                u = int(round(u*w))
                                v = int(round(v*h))
                                N = np.array([xx,yy,zz])
                                cos = find_cos2point(xx,yy,zz,L)
                                #cos = cos_deg[i]
                                if (cos > 0):
                                    R = L - 2 * (L[0] * N[0] + L[1]*N[1] + L[2]*N[2])*N
                                    len_R = math.sqrt(R[0] * R[0] + R[1] * R[1] + R[2] * R[2])
                                    len_V = math.sqrt(V[0] * V[0] + V[1] * V[1] + V[2] * V[2])

                                    alf = 30
                                    cos_blick =  (R[0] / len_R * (V[0] / len_V)) + (R[1] / len_R * (V[1] / len_V)) + (
                                                        R[2] / len_R * (V[2] / len_V))
                                    if (cos_blick > 0):
                                        cos_blick = 0
                                    color = (min(int(round(img_np[u][v][0] * cos + 100*cos_blick**alf)),255), min(int(round(img_np[u][v][1] * cos + 100*cos_blick**alf)),255),
                                         min(int(round(img_np[u][v][2] * cos + 100*cos_blick**alf)),255))
                                    img[q][j] = color
    return img

def draw_liner_good(z,x0,y0,z0,x1,y1,z1,img,color):
    steep = False
    if math.fabs(x0-x1) < math.fabs(y0-y1):
        steep = True
        x0,y0 = y0,x0
        x1,y1 = y1,x1
    if x1 < x0:
        x0,x1 = x1,x0
        y0,y1 = y1,y0
        z0,z1 = z1,z0
    k = abs(y1 - y0)
    error = 0
    y = y0
    zz = z0
    for x in range(x0,x1+1):
        if (steep):
            img[y, x] = color
        else:
            img[x, y] = color
        error += k
        if ((error << 1) > x1 - x0):
            y += np.sign(y1 - y0)
            error -= x1 - x0

    return img,z

