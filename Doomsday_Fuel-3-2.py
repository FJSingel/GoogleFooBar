from __future__ import division
from itertools import product
from fractions import Fraction
import copy


# Answer method
def answer(m):

    if len(m) == 1:
        return [1, 1]

    terminal = [0] * len(m)
    m = preformat(m)
    terminal_indexes = [x for x in range(len(m)) if m[x] == terminal]

    q_size = len(m) - len(terminal_indexes)
    denominators = []

    for row_index in range(q_size):
        denominators.append(sum(m[row_index]))
        for value_index in range(len(m[row_index])):
            m[row_index][value_index] = Fraction(m[row_index][value_index], denominators[row_index]).limit_denominator()

    q_matrix = []
    r_matrix = []
    for row in m[:q_size]:
        q_matrix.append(row[:q_size])
        r_matrix.append(row[q_size:])

    iq = subtract(identity(len(q_matrix)), q_matrix)
    print "I-Q = {}".format(iq)

    n = invert(iq)
    print "N = {}".format(n)

    b = mult(n, r_matrix)
    print "B = {}".format(b)

    denominators = []
    for fraction in b[0]:
        denominators.append(fraction.denominator)

    final_answer = []
    max_denominator = max(denominators)
    print max_denominator
    for value in b[0]:
        final_answer.append((value * max_denominator).numerator)
    final_answer.append(max_denominator)

    print "\nAnswer: {}\n".format(final_answer)
    return final_answer


# Move all the empty states to the end
def preformat(m):
    transformed = copy.deepcopy(m)

    # First row is initial state
    unsorted = True
    while unsorted:
        first_empty_index = -1
        for first_empty_index in range(1, len(m)):
            if transformed[first_empty_index] == ([0] * len(m)):
                break
        for last_nonempty_index in range(len(m) - 1, -1, -1):
            if transformed[last_nonempty_index] != ([0] * len(m)):
                break
        if first_empty_index > last_nonempty_index:
            unsorted = False
        else:
            # Gotta swap the row
            temp = transformed[first_empty_index]
            transformed[first_empty_index] = transformed[last_nonempty_index]
            transformed[last_nonempty_index] = temp
            # And now the columns
            for row in transformed:
                temp_val = row[first_empty_index]
                row[first_empty_index] = row[last_nonempty_index]
                row[last_nonempty_index] = temp_val
    return transformed


# don't give this a non-square matrix
def determinant(m):
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[1][0] * m[0][1]
    det = 0
    add_or_sub = 1
    for x in range(len(m)):
        msub = minor(x, 0, m)
        det += add_or_sub * m[0][x] * determinant(msub)
        add_or_sub *= -1
    return det


# removes the row and column intersecting at i,j
def minor(i, j, m):
    return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]


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

    if len(m) == 2:
        mat_min[0][0] = m[1][1]
        mat_min[1][1] = m[0][0]

        # probs should be negative?
        mat_min[1][0] = m[0][1]
        mat_min[0][1] = m[1][0]
    else:
        for x, y in product(range(len(m)), range(len(m))):
            mat_min[x][y] = determinant(minor(y, x, m))
    return mat_min


def matrix_coef(m):
    for x, y in product(range(len(m)), range(len(m))):
        if (x + y) % 2 == 1:
            m[x][y] *= -1
    return m


# Generate an identity matrix
def identity(n):
    identity = []
    for x in range(n):
        row = [0] * n
        row[x] = 1
        identity.append(row)
    return identity


def subtract(ma, mb):
    mc = copy.deepcopy(ma)
    for x, y in product(range(len(ma)), range(len(ma))):
        mc[x][y] = ma[x][y] - mb[x][y]
    return mc
