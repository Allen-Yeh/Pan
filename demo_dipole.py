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
width = 0.15
length = 0.15
nx = 15
ny = 15

# 定義複製項 , num_x_copies=1 , num_y_copies=1 , 就是1x1天線
num_x_copies = 5
x_spacing = 0.2
num_y_copies = 5
y_spacing = 0.2

# 防呆檢查
def validate_params(num_x_copies, num_y_copies, x_spacing, y_spacing, width, length):
    if not isinstance(num_x_copies, int) or not isinstance(num_y_copies, int) or num_x_copies < 1 or num_y_copies < 1:
        raise ValueError("num_x_copies 和 num_y_copies 必須是大於等於1的正整數。")
    if x_spacing <= width:
        raise ValueError("x_spacing 必須大於width。")
    if y_spacing <= length:
        raise ValueError("y_spacing 必須大於length。")

# 執行防呆檢查
validate_params(num_x_copies, num_y_copies, x_spacing, y_spacing, width, length)

freq = 900
# 使用 Mesh 類別生成網格
structure = mesh.Mesh('dipole', 'plate', width, length, nx, ny, num_x_copies, x_spacing, num_y_copies, y_spacing)
structure._replicate_plate([width, length, nx, ny, num_x_copies, x_spacing, num_y_copies, y_spacing])

print('\nrwg1')
rwg.rwg1(structure)

print('\nrwg2')
rwg.rwg2(structure)

print('\nrwg3')
mat_prop = material.Material(epsilon_r=1, mu_r=1)
rwg.rwg3(structure, mat_prop)

print('\nimpmat')
Z = rwg.impmat(structure, freq)

print('\nrwg4')
Vx = rwg.rwg4(structure, freq, incidence=rwg.negEz, pol=rwg.posEy)

Ix = np.linalg.solve(Z, Vx)

print('\nrwg5')
Jm = rwg.rwg5(structure, Ix)

densities = []
for each in Jm:
    densities.append((abs(each[0]) ** 2 + abs(each[1]) ** 2) ** 0.5)
structure.densities = densities

Isource = current.Current(freq)
Isource.Im = [complex(each[0]) for each in np.linalg.solve(Z, Vx)]

print('\nField and Measure Pattern.')
a = field.Field(structure, Isource)
p = pattern.Pattern(a, step=5)
p.xy, p.yz, p.zx = p.cut2D()

with open("./results/dipole_strct.pkl", 'wb') as file_strct:
    pickle.dump(structure, file_strct)

with open("./results/dipole_pattern.pkl", 'wb') as file_strct:
    pickle.dump(p, file_strct)
