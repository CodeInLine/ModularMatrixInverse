import numpy as np

def matrixModInverse(matrix_in, n):
    matrix = np.copy(matrix_in)
    size = np.size(matrix, 0)
    if size != np.size(matrix, 1):
        print('Error: size not same.')
        return None
    I = generateUnitMatrix(size)
    for i in range(size):
        numOfRows = i
        while matrix[i][i] == 0 or gcd(matrix[i][i], n) != 1:
            if numOfRows == size - 1:
                print('Error: sigular matrix.')
                return None
            else:
                matrix = putRowToBottom(matrix, i)
                I = putRowToBottom(I, i)
                numOfRows += 1
        
        if matrix[i][i] != 1:
            m = inverse(matrix[i][i], n)
            for j in range(size):
                matrix[i][j] = mul(matrix[i][j], m, n)
                I[i][j] = mul(I[i][j], m, n)
        
        for j in range(i+1, size):
            if matrix[j][i] != 0:
                multiply = -matrix[j][i]
                matrix = mulAddByRow(matrix, multiply, i, j, n)
                I = mulAddByRow(I, multiply, i, j, n)
    
    for i in range(size-1, -1, -1):
        for j in range(i-1, -1, -1):
            if matrix[j][i] != 0:
                multiply = -matrix[j][i]
                matrix = mulAddByRow(matrix, multiply, i, j, n)
                I = mulAddByRow(I, multiply, i, j, n)
    
    return I

def matrixModMultiply(matrix1, matrix2, n):
    if np.size(matrix1, 1) != np.size(matrix2, 0):
        print('Error: size invalid.')
        return None
    result = np.zeros((np.size(matrix1, 0), np.size(matrix2, 1)), int)
    for i in range(np.size(result, 0)):
        for j in range(np.size(result, 1)):
            for k in range(np.size(matrix1, 1)):
                result[i][j] = add(result[i][j], mul(matrix1[i][k], matrix2[k][j], n), n)
    return result

def matrixModSum(matrix1, matrix2, n):
    height = np.size(matrix1, 0)
    width = np.size(matrix2, 1)
    result = np.zeros((height, width), int)
    for i in range(height):
        for j in range(width):
            result[i][j] = add(matrix1[i][j], matrix2[i][j], n)
    return result

def gcd(x, y):
    while x != 0:
        x, y = y%x, x
    return y

def mul(x, y, n):
    return (x * y) % n

def add(x, y, n):
    return (x + y) % n

def inverse(x, n):
    if gcd(x, n) != 1:
        return None
    p1, p2, p3 = 1, 0, x
    q1, q2, q3 = 0, 1, n
    while q3 != 0:
        q = p3 // q3
        q1, q2, q3, p1, p2, p3 = (p1 - q * q1), (p2 - q * q2), (p3 - q * q3), q1, q2, q3
    return p1 % n

def generateUnitMatrix(size):
    I = np.zeros((size, size),dtype=int)
    for i in range(size):
        I[i][i] = 1
    return I

def putRowToBottom(matrix_in, rowIndex):
    matrix = matrix_in
    row = np.reshape(np.copy(matrix[rowIndex]), (1, -1))
    matrix = np.delete(matrix, rowIndex, 0)
    matrix = np.append(matrix, row, 0)
    return matrix

def mulAddByRow(matrix_in, multiply, srcIndex, dstIndex, n):
    matrix = matrix_in
    for i in range(np.size(matrix, 1)):
        matrix[dstIndex][i] = add(mul(matrix[srcIndex][i], multiply, n), matrix[dstIndex][i], n)
    return matrix

a = np.array([[0,0,0,3,0,0,8,0,0,1,0,0],
	[0,0,0,0,3,0,0,8,0,0,1,0],
	[0,0,0,0,0,3,0,0,8,0,0,1],
	[18,0,0,15,0,0,11,0,0,1,0,0],
	[0,18,0,0,15,0,0,11,0,0,1,0],
	[0,0,18,0,0,15,0,0,11,0,0,1],
	[0,0,0,24,0,0,4,0,0,1,0,0],
	[0,0,0,0,24,0,0,4,0,0,1,0],
	[0,0,0,0,0,24,0,0,4,0,0,1],
	[3,0,0,4,0,0,16,0,0,1,0,0],
	[0,3,0,0,4,0,0,16,0,0,1,0],
	[0,0,3,0,0,4,0,0,16,0,0,1]])

b = np.reshape(np.array([3,18,17,12,18,8,14,15,11,23,11,9]), (-1, 1))

l = np.array([[3,6,4],[5,15,18],[17,8,5]])

x = np.array([[0,3,8],
	[18,15,11],
	[0,24,4],
	[3,4,16],
	[20,0,19],
	[8,14,13]])

y = np.array([[3,18,17],
	[12,18,8],
	[14,15,11],
	[23,11,9],
	[1,25,20],
	[11,11,12]])

result = matrixModMultiply(matrixModInverse(a, 26), b, 26)
print('Keys:')
print(result)
print()
l = np.reshape(result[0:9], (3,3))
b = np.reshape(np.repeat(np.reshape(result[9:12], (1, -1)), 6, 0), (6,3))
print('Verify the key:')
print('decrypt:')
print(matrixModSum(matrixModMultiply(x, l, 26), b, 26))
print('cipher:')
print(y)
