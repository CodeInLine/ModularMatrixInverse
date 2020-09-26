import numpy as np

def matrixModularInverse(matrix, n):
    return np.mod(np.multiply(inverse(det(matrix, n), n), adj(matrix, n)), n)

def det(matrix, n):
    if np.size(matrix, 0) != np.size(matrix, 1):
        raise ValueError
    if np.size(matrix, 0) == 0:
        return None
    elif np.size(matrix, 0) == 1:
        return matrix[0]
    else:
        determin = 0
        width = np.size(matrix, 1)
        for i in range(width):
            determin += matrix[0][i] * det(submatrix(matrix, (0, i)), 26) * (-1) ** i
        return np.sum(determin) % n

def adj(matrix, n):
    adjugate = np.copy(matrix)
    height = np.size(adjugate, 0)
    width = np.size(adjugate, 1)
    for i in range(height):
        for j in range(width):
            adjugate[i][j] = (cofactor(matrix, (j,i), n) * (-1) ** (i + j)) % n
    return adjugate

def cofactor(matrix, location, n):
    return det(submatrix(matrix, location), n)

def submatrix(matrix, location):
    return np.delete(np.delete(matrix, location[0], 0),location[1], 1)

def gcd(x, y):
    while x != 0:
        x, y = y%x, x
    return y * np.sign(y)

def mul(x, y, n):
    return (x * y) % n

def add(x, y, n):
    return (x + y) % n

def inverse(x, n):
    if gcd(x, n) != 1:
        raise ValueError
    p1, p2, p3 = 1, 0, x
    q1, q2, q3 = 0, 1, n
    while q3 != 0:
        q = p3 // q3
        q1, q2, q3, p1, p2, p3 = (p1 - q * q1), (p2 - q * q2), (p3 - q * q3), q1, q2, q3
    return p1 % n