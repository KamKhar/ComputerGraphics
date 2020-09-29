import matplotlib.pyplot as plt
def read_vertexes(file_name,lst_x,lst_y,lst_f1,lst_f2,lst_f3):
    f = open(file_name)
    for line in f.readlines():
        lst = line.split()
        if lst != [] and lst[0] == 'v':
            lst_x.append(float(lst[1]))
            lst_y.append(float(lst[2]))
        elif lst != [] and lst[0] == 'f':
            lst_f1.append(int(lst[1]) - 1)
            lst_f2.append(int(lst[2]) - 1)
            lst_f3.append(int(lst[3]) - 1)
    f.close()


