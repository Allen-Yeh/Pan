# import pickle
# import current
# import field
# import material
# import mesh
# import pattern
# import rwg
# import numpy as np
# from plotter import *



# freq = 75.0
# # structure=mesh.Mesh('dipole', 'plate', 0.05, 2, 1, 10)

# (print('\nrwg1'))
# rwg.rwg1(structure)

# (print('\nrwg2'))
# rwg.rwg2(structure)

# (print('\nrwg3'))
# mat_prop = material.Material(epsilon_r = 1, mu_r = 1)
# rwg.rwg3(structure, mat_prop)

# (print('\nimpmat'))
# Z = rwg.impmat(structure, freq)

# (print('\nrwg4'))
# Vx = rwg.rwg4(structure, freq, incidence=rwg.negEz, pol=rwg.posEy)

# Ix = np.linalg.solve(Z, Vx)

# (print('\nrwg5'))
# Jm = rwg.rwg5(structure, Ix)

# densities = []
# for each in Jm:
#     densities.append( (abs(each[0])**2 + abs(each[1])**2)**0.5 )
# structure.densities = densities

# Isource = current.Current(freq)
# Isource.Im = [complex(each[0]) for each in np.linalg.solve(Z, Vx)]

# (print('\nField and Measure Pattern.'))
# a = field.Field(structure, Isource)
# p = pattern.Pattern(a, step = 5)
# p.xy, p.yz, p.zx = p.cut2D()

# with open("./results/dipole_strct.pkl", 'wb') as file_strct:
#     pickle.dump(structure, file_strct)

# with open("./results/dipole_pattern.pkl", 'wb') as file_strct:
#     pickle.dump(p, file_strct)


import pickle
import current
import field
import material
import mesh
import pattern
import rwg
import numpy as np
from plotter import *

# 定義參數
width = 1
length = 2
nx = 1
ny = 10

#定義複製項
num_x_copies = 3
x_spacing = 3
num_y_copies = 3
y_spacing =3

# # 使用 Mesh 類別生成網格
structure = mesh.Mesh('dipole', 'plate', width, length, nx, ny,num_x_copies, x_spacing, num_y_copies, y_spacing)
structure._replicate_plate([width, length, nx, ny, num_x_copies, x_spacing, num_y_copies, y_spacing])

# 設置 `densities` 屬性。這裡以預設值 1.0 作為示例，可以根據具體需求調整
structure.densities = [1.0] * structure.triangles_total

# 將結構保存到文件中
with open("./results/dipole_strct.pkl", 'wb') as file_strct:
    pickle.dump(structure, file_strct)
