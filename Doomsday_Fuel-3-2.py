from __future__ import division
from itertools import product
from fractions import Fraction
import copy

a = [[3, 0, 2], [2, 0, -2], [0, 1, 1]]
ad = 0
b = [[4, 6], [3, 8]]
bd = 14
c = [[6, 1, 1], [4, -2, 5], [2, 8, 7]]
cd = -306
d = [[6, 1, 1, 0], [4, -2, 5, 0], [2, 8, 7, 0], [0, 0, 1, 2]]
dd = -612

x = [[1, .66], [0, 1]]
y = [[.33, 0, 0], [0, .428, .571]]


# don't give this a non-square matrix
def determinant(m):
    mcopy = copy.deepcopy(m)
    if len(m) == 2:
        return mcopy[0][0] * mcopy[1][1] - mcopy[1][0] * mcopy[0][1]
    det = 0
    add_or_sub = 1
    for x in range(len(mcopy)):
        msub = non(x, 0, mcopy)
        det += add_or_sub * mcopy[0][x] * determinant(msub)
        add_or_sub *= -1
    return det


# Don't give this len 1 or 2 matrices
def non(i, j, m):
    sub = copy.deepcopy(m)
    del sub[j]
    for row in range(len(m) - 1):
        del sub[row][i]
    return sub


# Invert a square matrix
def invert(m):
    size = len(m)
    adj = matrix_minors(m)
    adj = matrix_coef(adj)
    adj = transpose(adj)
    det = determinant(m)
    for x, y in product(range(size), range(size)):
        adj[x][y] /= det
    return adj


# Transpose a matrix
def transpose(m):
    size = len(m)
    adj = copy.deepcopy(m)
    for x, y in product(range(size), range(size)):
        adj[x][y] = m[y][x]
    return adj


# Multiply 2 matrices
def mult(ma, mb):
    rows = len(mb)
    if rows is not 0:
        cols = len(mb[0])
    else:
        cols = 0
    res_rows = range(len(ma))
    prod_matrix = [[0] * cols for _ in res_rows]
    for idx in res_rows:
        for j, k in product(range(cols), range(rows)):
            prod_matrix[idx][j] += ma[idx][k] * mb[k][j]
    if cols is not 0:
        return prod_matrix
    else:
        return 0


# Computes a matrix of minors
def matrix_minors(m):
    mat_min = copy.deepcopy(m)
    for x, y in product(range(len(m)), range(len(m))):
        print "{},{}".format(x, y)
        print non(x, y, m)
        mat_min[x][y] = determinant(non(y, x, m))
    return mat_min


def matrix_coef(m):
    for x, y in product(range(len(m)), range(len(m))):
        if (x + y) % 2 == 1:
            m[x][y] *= -1
    return m


#
def cast_fractions(m):
    for y in range(len(m)):
        for x in range(len(m[y])):
            m[y][x] = Fraction(m[y][x])
    return m

print c
cast_fractions(c)
print c
print invert(c)
