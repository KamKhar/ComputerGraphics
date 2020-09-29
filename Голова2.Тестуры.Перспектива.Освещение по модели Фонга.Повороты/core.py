import PIL.Image as pi
import numpy as np
def read_vertexes(file_name,lst_x,lst_y,lst_z,lst_f1,lst_f2,lst_f3,lst_t1,lst_t2,lst_t3,lst_n1,lst_n2,lst_n3,lst_vn1,lst_vn2,lst_vn3,lst_u,lst_v):
    f = open(file_name)
    for line in f.readlines():
        lst = line.split()

        if lst != [] and lst[0] == 'v':
            lst_x.append(float(lst[1]))
            lst_y.append(float(lst[2]))
            lst_z.append(float(lst[3]))
        elif lst != [] and lst[0] == 'f':
            lst_1=lst[1].split('/')
            lst_f1.append(int(lst_1[0]) - 1)
            lst_t1.append(int(lst_1[1]) - 1)
            lst_n1.append(int(lst_1[2]) - 1)
            lst_2 = lst[2].split('/')
            lst_f2.append(int(lst_2[0]) - 1)
            lst_t2.append(int(lst_2[1]) - 1)
            lst_n2.append(int(lst_2[2]) - 1)
            lst_3 = lst[3].split('/')
            lst_f3.append(int(lst_3[0]) - 1)
            lst_t3.append(int(lst_3[1]) - 1)
            lst_n3.append(int(lst_3[2]) - 1)
        elif lst != [] and lst[0] == 'vt':
            lst_u.append(float(lst[1]))
            lst_v.append(float(lst[2]))
        elif lst != [] and lst[0] == 'vn':
            lst_vn1.append(float(lst[1]))
            lst_vn2.append(float(lst[2]))
            lst_vn3.append(float(lst[3]))
    img = pi.open('african_head_diffuse.tga')
    img_np = np.array(img)
    img_np = np.rot90(img_np, 1, axes=(0, 1))
    img_np = np.rot90(img_np, 1, axes=(0, 1))

    img_np = np.rot90(img_np, 1, axes=(0, 1))
    f.close()
    return img_np


