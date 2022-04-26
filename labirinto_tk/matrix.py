

class Matrix:
    def __init__(self, rows=0, columns=0, _list=None):
        self.size = str(rows)+'x'+str(columns)
        self.rows = rows
        self.cols = columns
        if _list is not None:
            self._list = _list
        else:
            self._list = []
            for r in range(rows):
                col = []
                for c in range(columns):
                    col.append(0)
                self._list.append(col)
            
    def __getitem__(self, row):
        return self._list[row]

    def __setitem__(self, row, new_row):
        self._list[row] = new_row

    def print(self):
        for i in self:
            print(i)

    def set(self, new_list_or_const):
        try:
            for r in range(self.rows):
                for c in range(self.cols):
                    self[r][c] = new_list_or_const[r][c]
        except TypeError:
            for r in range(self.rows):
                for c in range(self.cols):
                    self[r][c] = new_list_or_const

    def set_row(self, row, new_list_or_const):
        try:
            self[row] = list(new_list_or_const)
        except TypeError:
            for c in range(self.cols):
                self[row][c] = new_list_or_const

    def set_col(self, col, new_list_or_const):
        try:
            for r in range(self.rows):
                self[r][col] = new_list_or_const[r]
        except TypeError:
            for r in range(self.rows):
                self[r][col] = new_list_or_const

    def __eq__(self, other):
        for r in range(self.rows):
            for c in range(self.cols):
                if self[r][c] != other[r][c]:
                    return False
        return True

    def __add__(self, other):
        new_matr = Matrix(self.rows, self.cols)
        for r in range(self.rows):
            for c in range(self.cols):
                new_matr[r][c] = self[r][c]+other[r][c]
        return new_matr

    def __mul__(self, other_or_const):
        try:
            new_matr = Matrix(self.rows, other_or_const.cols)
            for r in range(self.rows):
                for c in range(other_or_const.cols):
                    for n in range(self.cols):
                        new_matr[r][c] += self[r][n]*other_or_const[n][c]
            return new_matr
        except AttributeError:
            new_matr = Matrix(self.rows, self.cols)
            for r in range(self.rows):
                new_matr[r] = [i*other_or_const for i in self[r]]
            return new_matr

    def __sub__(self, other):
        new_matr = self+other*-1
        return new_matr

    def __pow__(self, power):
        if power == 0:
            new_matr = matr_E(self.rows)
            return new_matr
        new_matr = self
        for i in range(power-1):
            new_matr *= self
        return new_matr

    def transpose(self):
        new_matr = Matrix(self.cols, self.rows)
        for c in range(self.cols):
            for r in range(self.rows):
                new_matr[c][r] = self[r][c]
        return new_matr

    def row(self, row):
        return self[row]

    def col(self, col):
        return self.transpose()[col]

    def complement(self, x, y):       
        n = self.rows
        if n != self.cols:
            raise TypeError('Not inversible Matrix!')
        dop = []
        for i in range(n):
            if i != x:
                dop_str = []
                for j in range(n):
                    if j != y:
                        dop_str.append(self[i][j])
                dop.append(dop_str)
        return Matrix(n-1, n-1, dop)

    def det(self):  # finds determinant by recursion
        n = self.rows
        if n >= 2:
            deter = 0
            for i in range(n):
                deter += ((-1)**i) * self[0][i] * (self.complement(0, i)).det()
        else:
            deter = self[0][0]
        return deter

    def inverse(self):  # finds inverse matrix
        n = self.rows
        co_matr = [[0]*n for i in range(n)]  # empty matrix for inversion
        det_m = self.det()
        if det_m == 0:
            raise ZeroDivisionError('Not inversible matrix!')
        for i in range(n):
            for j in range(n):
                co_matr[j][i] = ((-1)**(i+j))*(self.complement(i, j)).det() / det_m
        return Matrix(n, n, co_matr)


def matr_E(n):
    new_matr = Matrix(n, n)
    for i in range(n):
        new_matr[i][i] = 1
    return new_matr


if __name__ == '__main__':
    print('--- setting a matrix and its size ---')
    A = Matrix(4, 3)
    A.print()
    print('--- setting its values ---')
    A[0][1] = 5
    A.set_row(1, [1, 2, 3])
    A.print()
    print('--- changing rows ---')
    A[0], A[1] = A[1], A[0]
    A.print()
    print('--- changing elements ---')
    A[0][2], A[0][0] = A[0][0], A[0][2]
    A.print()
    print('--- example of matrix operations ---')
    A = Matrix(2, 2, [[1, 2], [2, 3]])
    B = Matrix(2, 2, [[-1, -2], [2, 1]])
    print('A =')
    A.print()
    print('B =')
    B.print()
    print('\nA+B =')
    (A+B).print()
    print('\n3A*2B =')
    ((A*3)*(B*2)).print()  # note that to multiply matrix by a constant you have to write A*c not c*A
