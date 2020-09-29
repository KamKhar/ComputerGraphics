import matplotlib.pyplot as plt
import numpy as np
def read_vertexes(file_name,lst_x,lst_y,lst_f1,lst_f2,lst_f3):
    f = open(file_name)
    for line in f.readlines():
        lst = line.split()
        if lst != [] and lst[0] == 'v':
            lst_x.append(int(lst[1]))
            lst_y.append(int(lst[2]))
        elif lst != [] and lst[0] == 'f':
            lst_1=lst[1].split('/')
            lst_f1.append(int(lst_1[0]) - 1)
            lst_2 = lst[2].split('/')
            lst_f2.append(int(lst_2[0]) - 1)
            lst_3 = lst[3].split('/')
            lst_f3.append(int(lst_3[0]) - 1)
    f.close()
def vertexes_to_projective(vertexes):
    return np.concatenate([vertexes[:,:2].copy(),np.ones(vertexes.shape[0]).reshape(-1,1)],axis=1)



