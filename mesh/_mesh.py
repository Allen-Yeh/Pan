# import pydistmesh as dm
import dmsh as dm
from pyhull.delaunay import DelaunayTri
import numpy as np
from .poly import Poly
import warnings



class Mesh(object):
    """Mesh Generator          
    Inputs: initialize by object = Mesh("mesh name", string of mesh methods, list of parameters)

    String of mesh methods:
    a. _plate: patch type of antenna using pyhull
       argv = (W,L.Nx,Ny) and return (p,t)
       W: width
       L: length
       Nx, Ny: no. of sections in X and Y
       t: nx3 2-D list; n trianles; 3 vertices in node numbers
       p: nx2 2-D list; n nodes; 2 coordinates (X and Y)
       ( p will become nx2 list after adding Z-axis in /rwg/rwg1.py)
    note.1: the returned t is 3-dim, not including yet the triangle indicator

    b. _plate2: patch type of antenna using distmesh
       argv = (W, L, delta) and also return (p,t), same as abovementioned
       W: width
       L: length
       edge_size: the target edge size, which may not be exactly the same in the final triangularization, but close enough.

    c. _poly: arbitrary polygon
       argv = (poly_vertices, edge_size, bounding_box)
       poly_vertices: the returned vertices of the poly.Poly object
       edge_size: the target edge size, same as b.
       bounding_box: list of [xmin, ymin, xmax, ymax] to indicate the upper bound of the box
    """
    _fields = ['tri', 'points', 'triangles', 'area', 'center', 'center_', 'center_delta', 'center_g', 'edges_total', 'edge_length', 'edge_indicator', 'triangle_plus', 'triangle_minus', 'triangles_total', 'rho_plus', 'rho_minus', 'rho__plus', 'rho__minus', 'FactorA', 'FactorFi']


    def __init__(self, name='patch', geometry='plate', *argv):
        self.name = name
        self.geometry = geometry
        self.dlist = argv  ## dimension list
        self.tri = None

        # 初始化所有字段為空列表
        for each in Mesh._fields:
            setattr(self, each, [])

        # 初始化天線尺寸並設置網格
        exec('self._' + geometry + '(self.dlist)')


    def _plate(self, dlist, replicate=True):
        """Trianularize with pyhull Delaunay algorithm."""
        width = float(dlist[0])
        length = float(dlist[1])
        self.width = width  # 保存寬度
        self.length = length  # 保存長度
        half_w = width / 2
        half_l = length / 2
        nx = dlist[2]
        ny = dlist[3]
        delta = 0.0  # 1e-6
        x_coor = ()
        y_coor = ()

        self.x_extent = [-half_w, half_w]
        self.y_extent = [-half_l, half_l]
        self.maxdim = max([abs(each) for each in self.x_extent + self.y_extent])
        for m in range(nx + 1):
            for n in range(ny + 1):
                x_coor += (-width / 2.0 + m * 1.0 * width / nx,)
                y_coor += (-length / 2.0 + n * 1.0 * length / ny,)

        points = list(zip(x_coor, y_coor))
        tri = DelaunayTri(points)
        self.vertices = [[half_w, half_l], [half_w, -half_l], [-half_w, -half_l], [-half_w, half_l], [half_w, half_l]]
        self.triangles = tri.vertices
        self.points = tri.points
        self.triangles = [tuple(each) for each in self.triangles]
        self.triangles_total = len(self.triangles)

        if replicate:
            num_x_copies = int(dlist[4])
            x_spacing = float(dlist[5])
            num_y_copies = int(dlist[6])
            y_spacing = float(dlist[7])

            replicated_triangles = []
            replicated_points = list(self.points)
            num_original_points = len(self.points)

            for i in range(num_x_copies):
                for j in range(num_y_copies):
                    if i == 0 and j == 0:
                        continue

                    # 計算複製的偏移量
                    x_offset = i * x_spacing
                    y_offset = j * y_spacing

                    # 複製點並添加到點列表中
                    replicated_points.extend([(x + x_offset, y + y_offset) for x, y in self.points])

                    # 複製三角形，並更新其頂點索引
                    num_points = num_original_points * (i + j * num_x_copies)
                    for triangle in self.triangles:
                        replicated_triangle = [v + num_points for v in triangle]
                        replicated_triangles.append(replicated_triangle)

            # 更新 Mesh 物件的屬性
            self.triangles = replicated_triangles + self.triangles
            self.points = replicated_points
            self.triangles_total = len(self.triangles)



   

    # def _plate2(self, dlist):
    #     """Triangularize with MIT Per-Olof, Prof. Gilbert Strange's algorithm."""
    #     width = float(dlist[0])
    #     length = float(dlist[1])
    #     half_w = width / 2
    #     half_l = length / 2
    #     edge_size = dlist[2]
    #     self.x_extent = [-half_w, half_w]
    #     self.y_extent = [-half_l, half_l]
    #     self.maxdim = max([abs(each) for each in self.x_extent + self.y_extent])

    #     polygon = Poly([-half_w, -half_l])
    #     polygon.add_line2(width, 0, 1)
    #     polygon.add_line2(length, 90, 1)
    #     polygon.add_line2(width, 180, 1)
    #     polygon.add_line2(length, 270, 1)
    #     polygon.close()
    #     self.vertices = polygon.vertices
    #     pv = polygon.vertices
    #     f = lambda p: dm.dpoly(p,pv)
    #     pnt, tri = dm.distmesh2d(f, dm.huniform, edge_size, (-half_w, -half_l, half_w, half_l), pv)

    #     self.triangles = tri
    #     self.points = pnt
    #     self.triangles = [tuple(each) for each in self.triangles]
    #     self.triangles_total = len(self.triangles)


    # def _poly(self, dlist):
    #     """Triangularize arbitrary shape of polygon with MIT Per-Olof, Prof. Gilbert Strange's algorithm."""
    #     vertices = dlist[0]
    #     x, y = [each[0] for each in vertices], [each[1] for each in vertices]
    #     self.x_extent = [min(x), max(x)]
    #     self.y_extent = [min(y), max(y)]
    #     self.maxdim = max([abs(each) for each in self.x_extent + self.y_extent])

    #     edge_size = dlist[1]
    #     bbox = dlist[2]
    #     self.vertices = vertices
    #     pv = vertices
    #     f = lambda p: dm.dpoly(p,pv)
    #     pnt, tri = dm.distmesh2d(f, dm.huniform, edge_size, bbox, pv)

    #     self.triangles = tri
    #     self.points = pnt
    #     self.triangles = [tuple(each) for each in self.triangles]
    #     self.triangles_total = len(self.triangles)