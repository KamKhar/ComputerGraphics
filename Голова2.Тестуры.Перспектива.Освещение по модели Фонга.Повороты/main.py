import visualize
import matplotlib.pyplot as plt
import numpy as np
import core

img = np.zeros((512,512,3), dtype=np.uint8)
lst_x = []
lst_y = []
lst_z = []
lst_f1 = []
lst_f2 = []
lst_f3 = []
lst_u = []
lst_v = []
lst_t1 = []
lst_t2 = []
lst_t3 = []
lst_n1 = []
lst_n2 = []
lst_n3 = []
lst_vn1 = []
lst_vn2 = []
lst_vn3 = []
img_np = core.read_vertexes('face.obj',lst_x,lst_y,lst_z,lst_f1,lst_f2,lst_f3,lst_t1,lst_t2,lst_t3,lst_n1,lst_n2,lst_n3,lst_vn1,lst_vn2,lst_vn3,lst_u,lst_v)
img = visualize.draw_ventexes(180,lst_x,lst_y,lst_z,lst_f1,lst_f2,lst_f3,lst_t1,lst_t2,lst_t3,lst_n1,lst_n2,lst_n3,lst_vn1,lst_vn2,lst_vn3,lst_u,lst_v,img_np, 512, img)
plt.imshow(img)
plt.show()