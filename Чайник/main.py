import visualize
import matplotlib.pyplot as plt
import core

lst_x = []
lst_y = []
lst_f1 = []
lst_f2 = []
lst_f3 = []
core.read_vertexes('task1.obj',lst_x,lst_y,lst_f1,lst_f2,lst_f3)
visualize.draw_ventexes(lst_x,lst_y,lst_f1,lst_f2,lst_f3,512)
plt.show()