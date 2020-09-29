def read_vertexes(file_name,lst_x,lst_y,lst_z,lst_f1,lst_f2,lst_f3):
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
            lst_2 = lst[2].split('/')
            lst_f2.append(int(lst_2[0]) - 1)
            lst_3 = lst[3].split('/')
            lst_f3.append(int(lst_3[0]) - 1)
    f.close()


