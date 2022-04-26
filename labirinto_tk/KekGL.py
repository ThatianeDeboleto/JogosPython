"""
KekGL is like OtherGLs but Kek.

Note that in KekGl row-major matrix order is used.
"""

from matrix import *
from math import cos, sin


class Prim:
    """ Class to define operations with primitives
    Coordinates of their points stored as a concatenated rows of homogeneous coordinates
    """
    def __init__(self, crds, color='black', outline='black', width=1):
        self.color = color
        self.outline = outline
        self.width = width
        self.num_of_vertices = len(crds)
        self.w_crds = Matrix(len(crds), 4)
        for i in range(len(crds)):
            self.w_crds.set_row(i, list(crds[i])+[1])
        self.c_crds = None
        self.p_crds = None
        self.ndc_crds = None
        self.s_crds = None

    # Setting position and direction of the primitive in the world
    def toWorld(self, matrix):
        self.w_crds *= matrix

    # Setting position and direction relative to the camera (input matrix should be inverse camera matrix)
    def toCamera(self, matrix):
        self.c_crds = self.w_crds*matrix

    # Getting projected coordinates using projection matrix
    def toProjection(self, matrix):
        self.p_crds = self._rear_clipping_algorithm(5)*matrix

    # NDC is normalized device coordinates
    def toNDC(self):
        self.ndc_crds = self.p_crds*1
        for i in range(self.p_crds.rows):
            self.ndc_crds.set_row(i, [a/self.p_crds[i][3] for a in self.p_crds[i]])

    def toScreen(self, width, height):
        self.s_crds = Matrix(self.p_crds.rows, 2)
        for i in range(self.ndc_crds.rows):
            self.s_crds.set_row(i, [width/2*(self.ndc_crds[i][0]+1), height/2*(self.ndc_crds[i][1]+1)])

    @staticmethod
    # finds intersection of line p1p2 with plane z+dz=0
    def _intersec(p1, p2, dz):
        t = -(p1[2]+dz)/(p2[2]-p1[2])
        return [p1[0]+(p2[0]-p1[0])*t, p1[1]+(p2[1]-p1[1])*t, -dz, 1]

    def _rear_clipping_algorithm(self, dz):
        """ Clips polygons with plane z+dz=0 (dz>0) and returns new polygon's matrix

        It checks every two points starting from the visible one. Depending on the sign
        of their z-coordinate a new point added or not to the new list of coordinates.
        Clipping points have z = -dx coordinate to project correctly.
        Too big or too small values of dz can produce glitches. dz = 1 seems to be fine."""
        crds_list = []
        p_prev = None

        for i in range(self.c_crds.rows):
            if self.c_crds[i][2] < -dz:
                try:
                    p_curr = [*self.c_crds[i+1]]
                    i_curr = i+1
                except IndexError:
                    p_curr = [*self.c_crds[0]]
                    i_curr = 0
                p_prev = [*self.c_crds[i]]
                prev = 1
                break

        if p_prev is None:
            return Matrix(2, 4, [[10, 0, 1, 1], [10, 0, 1, 1]])  # returns invisible polygon

        counter = 0
        while counter != self.c_crds.rows:
            if p_curr[2] < -dz:
                curr = 1
            elif p_curr[2] == -dz:
                curr = 0
            else:
                curr = -1

            while True:
                if curr == -1 and prev == 1:
                    crds_list += [self._intersec(p_curr, p_prev, dz)]
                    break
                if curr == 0 and prev == 1:
                    crds_list += [self._intersec(p_curr, p_prev, dz)]
                    break
                if curr == 1 and prev == 1:
                    crds_list += [p_curr]
                    break
                if curr == -1 and prev == -1:
                    break
                if curr == 0 and prev == -1:
                    break
                if curr == 1 and prev == -1:
                    crds_list += [self._intersec(p_curr, p_prev, dz)]
                    crds_list += [p_curr]
                    break
                if curr == -1 and prev == 0:
                    break
                if curr == 0 and prev == 0:
                    break
                if curr == 1 and prev == 0:
                    crds_list += [self._intersec(p_curr, p_prev, dz)]
                    crds_list += [p_curr]
                    break

            p_prev = p_curr
            prev = curr
            i_curr += 1
            counter += 1
            try:
                p_curr = [*self.c_crds[i_curr]]
            except IndexError:
                p_curr = [*self.c_crds[0]]
                i_curr = 0

        return Matrix(len(crds_list), 4, crds_list)

    def isInFront(self):
        for i in range(self.num_of_vertices):
            if self.c_crds[i][2] >= 0:
                return False

        return True

    # should be inited after self.toNDC()
    def isFullyVisible(self):
        if self.isInFront():
            for i in range(self.num_of_vertices):
                if abs(self.ndc_crds[i][0]) >= 1 or abs(self.ndc_crds[i][1]) >= 1:
                    return False
            return True
        else:
            return False


class Object:
    """ Class that makes primitives from a model
    Operations with Object are the same as for Prim
    """
    def __init__(self, model):
        self.prims = []
        for poly in model:
            self.prims += [Prim(crds=poly['crds'], color=poly['color'],
                                outline=poly['outline'], width=poly['width'])]
        self.center = [0]*4

    def toWorld(self, matrix):
        for prim in self.prims:
            prim.toWorld(matrix)

    def toCamera(self, matrix):
        for prim in self.prims:
            prim.toCamera(matrix)

    def toProjection(self, matrix):
        for prim in self.prims:
            prim.toProjection(matrix)

    def toNDC(self):
        for prim in self.prims:
            prim.toNDC()

    def toScreen(self, width, height):
        for prim in self.prims:
            prim.toScreen(width, height)

    def isInFront(self):
        for prim in self.prims:
            if not prim.isInFront():
                return False

        return True

    def isVisible(self):
        for prim in self.prims:
            if not prim.isVisible():
                return False

        return True


class Player:
    def __init__(self):
        self.matrix = matr_E(4)
        self.speed = 1
        self.isMoving = False
        self.deviation_angle = 0.0

    def move(self, matrix):
        r = self.matrix[3]
        self.matrix = matrix*self.matrix
        self.matrix[3] = r

    def move_along_z(self, r, phi):
        self.matrix[3][0] += (self.matrix[1][0]*sin(phi) - self.matrix[2][0]*cos(phi))*r
        self.matrix[3][1] += (self.matrix[1][1]*sin(phi) - self.matrix[2][1]*cos(phi))*r
        self.matrix[3][2] += (self.matrix[1][2]*sin(phi) - self.matrix[2][2]*cos(phi))*r

    def move_along_x(self, r):
        self.matrix[3][0] += self.matrix[0][0]*r
        self.matrix[3][1] += self.matrix[0][1]*r
        self.matrix[3][2] += self.matrix[0][2]*r

    def move_along_y(self, r):
        self.matrix[3][0] += self.matrix[1][0]*r
        self.matrix[3][1] += self.matrix[1][1]*r
        self.matrix[3][2] += self.matrix[1][2]*r


class World:
    def __init__(self, player, *objects_static):
        self.objects = objects_static
        self.player = player
        self._BSP_root = None
        self.screen_width = 800
        self.screen_height = 600
        self.projection_matrix = None
        self.camera_matrix = matr_E(4)
        self.prims_static = None

    def set_screen_resolution(self, width, height):
        self.screen_width = width
        self.screen_height = height

    def BSP_create(self, root_prim=0):
        # making a list of prims to sort them for drawing
        self.prims_static = []
        for obj in self.objects:
            if isinstance(obj, Prim):
                self.prims_static += [obj]
            if isinstance(obj, Object):
                self.prims_static += [*obj.prims]

        self._BSP_root = _Node(self.prims_static[root_prim])
        for prim in self.prims_static:
            if prim is not self.prims_static[root_prim]:
                self._BSP_root.insert(prim)

    # def BSP_load(self, file):
    #     self._BSP_root = ...

    def update(self):
        self.prims_static = self._BSP_root.get_prims((self.camera_matrix[3][0],
                                                     self.camera_matrix[3][1], self.camera_matrix[3][2]))

        self.camera_matrix = self.player.matrix
        camera_matrix = self.camera_matrix.inverse()

        for prim in self.prims_static:
            prim.toCamera(camera_matrix)
            prim.toProjection(self.projection_matrix)
            prim.toNDC()
            prim.toScreen(self.screen_width, self.screen_height)

    def canv_draw(self, prim):
        pass

    def draw(self):
        for prim in self.prims_static:
            self.canv_draw(prim)

    def get_allowed_directions(self):
        i = 0
        allowed_directions = []
        #print(self.prims_static[1])
        i = 0
        x0, y0, z0 = self.player.matrix[3][0], self.player.matrix[3][1], self.player.matrix[3][2]
        for prim in self.prims_static:
            i += 1
            x1, y1, z1 = prim.w_crds[0][0], prim.w_crds[0][1], prim.w_crds[0][2]    # for each plane get tree points
            x2, y2, z2 = prim.w_crds[1][0], prim.w_crds[1][1], prim.w_crds[1][2]
            x3, y3, z3 = prim.w_crds[2][0], prim.w_crds[2][1], prim.w_crds[2][2]

            A = (y2-y1)*(z3-z1)-(y3-y1)*(z2-z1)                                     # find coefficients for the plane equation
            B = (x3-x1)*(z2-z1)-(x2-x1)*(z3-z1)
            C = (x2-x1)*(y3-y1)-(x3-x1)*(y2-y1)
            D = -A*x1-B*y1-C*z1
            
            len_norm = abs((A**2 + B**2 + C**2))**0.5                               # length of normal
            dist = abs((A*x0 + B*y0 + C*z0 + D))/(len_norm)                         # distance to the plane
            

            if A*x0 + B*y0 + C*z0 + D > 0:
                k = 1
            else:
                k = -1
            intersection = False
            #print(dist, intersection)
            x_col, y_col, z_col = x0 + A * (dist/len_norm)*(-k), y0 + B * (dist/len_norm)*(-k), z0 + C * (dist/len_norm)*(-k)   # coordinates of the projection point
            
            if (x_col >= min([prim.w_crds[0][0], prim.w_crds[1][0], prim.w_crds[2][0], prim.w_crds[3][0]]) and x_col <= max([prim.w_crds[0][0], prim.w_crds[1][0], prim.w_crds[2][0], prim.w_crds[3][0]])) and (y_col >= min([prim.w_crds[0][1], prim.w_crds[1][1], prim.w_crds[2][1], prim.w_crds[3][1]]) and y_col <= max([prim.w_crds[0][1], prim.w_crds[1][1], prim.w_crds[2][1], prim.w_crds[3][1]])) and (z_col >= min([prim.w_crds[0][2], prim.w_crds[1][2], prim.w_crds[2][2], prim.w_crds[3][2]]) and z_col <= max([prim.w_crds[0][2], prim.w_crds[1][2], prim.w_crds[2][2], prim.w_crds[3][2]])):
                intersection = True                                                 # interseption check
            
            if dist < 2*self.player.speed*4 and intersection == True:               # add restriction to moving
                allowed_directions.append([A*k,B*k,C*k])
            
        return allowed_directions
 



class Main:
    def __init__(self, world):
        pass

    def update(self):
        pass


class _Node:
    def __init__(self, prim):

        self.behind = None
        self.infront = None
        self.prims = [prim]
        self.equation = self.plane_equation()

    def plane_equation(self):
        prim = self.prims[0]
        x1, y1, z1 = prim.w_crds[0][0], prim.w_crds[0][1], prim.w_crds[0][2]
        x2, y2, z2 = prim.w_crds[1][0], prim.w_crds[1][1], prim.w_crds[1][2]
        x3, y3, z3 = prim.w_crds[2][0], prim.w_crds[2][1], prim.w_crds[2][2]

        A = (y2-y1)*(z3-z1)-(y3-y1)*(z2-z1)
        B = (x3-x1)*(z2-z1)-(x2-x1)*(z3-z1)
        C = (x2-x1)*(y3-y1)-(x3-x1)*(y2-y1)
        D = -A*x1-B*y1-C*z1
        # Ax+By+Cz+D=0
        return A, B, C, D

    def product(self, crd):
        A, B, C, D = self.equation
        return crd[0]*A+crd[1]*B+crd[2]*C+D

    def isInFront(self, prim):
        for crd in prim.w_crds:
            if self.product(crd) < -10**(-8):  # handling the floating point error
                return False
        return True

    def isBehind(self, prim):
        for crd in prim.w_crds:
            if self.product(crd) > 10**(-8):  # handling the floating point error
                return False
        return True

    def isIntersected(self, prim):
        return not (self.isInFront(prim) or self.isBehind(prim) or self.isBelonging(prim))

    def isBelonging(self, prim):
        for crd in prim.w_crds:
            if abs(self.product(crd)) > 10**(-8):  # handling the floating point error
                return False
        return True

    # finds intersection of line p1p2 with plane Ax+By+Cz+D=0
    def intersec(self, p1, p2):
        A, B, C, D = self.equation
        t = -(D+p1[0]*A+p1[1]*B+p1[2]*C)/((p2[0]-p1[0])*A+(p2[1]-p1[1])*B+(p2[2]-p1[2])*C)
        x = p1[0]+(p2[0]-p1[0])*t
        y = p1[1]+(p2[1]-p1[1])*t
        z = p1[2]+(p2[2]-p1[2])*t

        return [x, y, z, 1]

    def clip(self, prim):

        crds_list1 = []
        p_prev = None

        for i in range(prim.w_crds.rows):
            if self.product(prim.w_crds[i]) > 0:
                try:
                    p_curr = [*prim.w_crds[i+1]]
                    i_curr = i+1
                except IndexError:
                    p_curr = [*prim.w_crds[0]]
                    i_curr = 0
                p_prev = [*prim.w_crds[i]]
                prev = 1
                break

        counter = 0
        while counter != prim.w_crds.rows:
            if self.product(p_curr) > 0:
                curr = 1
            elif self.product(p_curr) == 0:
                curr = 0
            else:
                curr = -1

            while True:
                if curr == -1 and prev == 1:
                    crds_list1 += [self.intersec(p_curr, p_prev)]
                    break
                if curr == 0 and prev == 1:
                    crds_list1 += [self.intersec(p_curr, p_prev)]
                    break
                if curr == 1 and prev == 1:
                    crds_list1 += [p_curr]
                    break
                if curr == -1 and prev == -1:
                    break
                if curr == 0 and prev == -1:
                    break
                if curr == 1 and prev == -1:
                    crds_list1 += [self.intersec(p_curr, p_prev)]
                    crds_list1 += [p_curr]
                    break
                if curr == -1 and prev == 0:
                    break
                if curr == 0 and prev == 0:
                    break
                if curr == 1 and prev == 0:
                    crds_list1 += [self.intersec(p_curr, p_prev)]
                    crds_list1 += [p_curr]
                    break

            p_prev = p_curr
            prev = curr
            i_curr += 1
            counter += 1
            try:
                p_curr = [*prim.w_crds[i_curr]]
            except IndexError:
                p_curr = [*prim.w_crds[0]]
                i_curr = 0

        crds_list2 = []
        p_prev = None
        p_curr = None
        prev = None

        for i in range(prim.w_crds.rows):
            if self.product(prim.w_crds[i]) < 0:
                try:
                    p_curr = [*prim.w_crds[i+1]]
                    i_curr = i+1
                except IndexError:
                    p_curr = [*prim.w_crds[0]]
                    i_curr = 0
                p_prev = [*prim.w_crds[i]]
                prev = 1
                break

        counter = 0
        while counter != prim.w_crds.rows:
            if self.product(p_curr) < 0:
                curr = 1
            elif self.product(p_curr) == 0:
                curr = 0
            else:
                curr = -1

            while True:
                if curr == -1 and prev == 1:
                    crds_list2 += [self.intersec(p_curr, p_prev)]
                    break
                if curr == 0 and prev == 1:
                    crds_list2 += [self.intersec(p_curr, p_prev)]
                    break
                if curr == 1 and prev == 1:
                    crds_list2 += [p_curr]
                    break
                if curr == -1 and prev == -1:
                    break
                if curr == 0 and prev == -1:
                    break
                if curr == 1 and prev == -1:
                    crds_list2 += [self.intersec(p_curr, p_prev)]
                    crds_list2 += [p_curr]
                    break
                if curr == -1 and prev == 0:
                    break
                if curr == 0 and prev == 0:
                    break
                if curr == 1 and prev == 0:
                    crds_list2 += [self.intersec(p_curr, p_prev)]
                    crds_list2 += [p_curr]
                    break

            p_prev = p_curr
            prev = curr
            i_curr += 1
            counter += 1
            try:
                p_curr = [*prim.w_crds[i_curr]]
            except IndexError:
                p_curr = [*prim.w_crds[0]]
                i_curr = 0

        clipped_prim_in_front = Prim((), color=prim.color, width=prim.width, outline=prim.outline)
        clipped_prim_in_front.w_crds = Matrix(len(crds_list1), 4, crds_list1)

        clipped_prim_behind = Prim((), color=prim.color, width=prim.width, outline=prim.outline)
        clipped_prim_behind.w_crds = Matrix(len(crds_list2), 4, crds_list2)

        return clipped_prim_in_front, clipped_prim_behind

    def insert(self, prim):
        if self.isBelonging(prim):
            self.prims += [prim]
        elif self.isInFront(prim):
            if self.infront is None:
                self.infront = _Node(prim)
            else:
                self.infront.insert(prim)
        elif self.isBehind(prim):
            if self.behind is None:
                self.behind = _Node(prim)
            else:
                self.behind.insert(prim)
        elif self.isIntersected(prim):
            clipped_prim_in_front, clipped_prim_behind = self.clip(prim)
            if self.infront is None:
                self.infront = _Node(clipped_prim_in_front)
            else:
                self.infront.insert(clipped_prim_in_front)
            if self.behind is None:
                self.behind = _Node(clipped_prim_behind)
            else:
                self.behind.insert(clipped_prim_behind)

    def get_prims(self, view_crds):
        '''
        self.prims[i].w_crds[3][]
        for prim in self.prims:
            if (view_crds[0] - prim.w_crds[:,0])**2 + (view_crds[2] - prim.w_crds[:,2])**2) < R:
                prims += prim

        '''
        prims = []
        if self.infront is None and self.behind is None:
            prims += self.prims

        elif self.product(view_crds) > 0:
            if self.behind:
                prims += self.behind.get_prims(view_crds)
            prims += self.prims
            if self.infront:
                prims += self.infront.get_prims(view_crds)
        elif self.product(view_crds) < 0:
            if self.infront:
                prims += self.infront.get_prims(view_crds)
            prims += self.prims
            if self.behind:
                prims += self.behind.get_prims(view_crds)
        else:
            if self.infront:
                prims += self.infront.get_prims(view_crds)
            if self.behind:
                prims += self.behind.get_prims(view_crds)
        
        return prims



