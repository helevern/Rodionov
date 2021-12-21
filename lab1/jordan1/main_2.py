import numpy as np


def init():
    st = int(input("Введите количество строк: "))
    col = int(input("Введите количество столбцов(с учетом столбца F): "))

    takenSt = []
    takenCol = []
    inpMatrix = np.empty([st, col], float)
    tempMatrix = inpMatrix
    fillMatrix(tempMatrix, st, col)
    setSolutionType(inpMatrix, tempMatrix, takenSt, takenCol, col)


def fillMatrix(tempMatrix, st, col):
    for i in range(0, st):
        for j in range(0, col):
            print("Введите элемент строки: ", i + 1, " столбца: ", j + 1)
            tempMatrix[i, j] = float(input())
    letters(tempMatrix, col, -1)
    print(tempMatrix)

def letters(tempMatrix, col, a):
    sign1 = []

    for sn in range(col - 1):

        if sn == a - 1:
            sn += 1
        else:
            sign1.append('x' + str(sn + 1))
    sign1.append('B')
    print(sign1)

def setSolutionType(inpMatrix, tempMatrix, takenSt, takenCol, col):
    for i in range(len(inpMatrix[0]) - 1):
        rSt = int(input("Введите номер строки разрешающего элемента: "))
        rCol = int(input("Введите номер столбца разрешающего элемента: "))
        print("Выбран элемент строки: ", rSt, " и столбца: ", rCol, " элемент в которых равен: ",
              tempMatrix[rSt - 1, rCol - 1])
        if tempMatrix[rSt - 1, rCol - 1] != 0 and rCol < len(tempMatrix[0]) and not takenSt.count(rSt):
            takenSt.append(rSt)
            takenCol.append(rCol)
            tempMatrix = jordan(tempMatrix, rSt, rCol)
            print("Метод Жордановых исключений: ")

            tempMatrix = np.delete(tempMatrix, rCol-1, 1)

            letters(tempMatrix, col, rCol)

            print(tempMatrix)
            listener = 1
        elif tempMatrix[rSt - 1, rCol - 1] == 0 and tempMatrix[rSt - 1][len(tempMatrix[0]) - 1] == 1:
            listener = 2
        elif tempMatrix[rSt - 1, rCol - 1] == 0 and tempMatrix[rSt - 1][len(tempMatrix[0]) - 1] == 0:
            parameters = []
            equals = []
            counter = 1
            for ts in range(len(tempMatrix)):
                for tc in range(len(tempMatrix[0]) - 1):
                    if tempMatrix[ts, tc] == 0.0 and tempMatrix[ts, len(tempMatrix[0]) - 1] == 0.0:
                        parameters.append('x' + str(counter) + '=parameter' + str(counter))
                        counter += 1
            for ts in range(len(tempMatrix)):
                if tempMatrix[ts, len(tempMatrix[0]) - 1] != 0.0:
                    equals.append('x' + str(counter) + '=' + str(-1 * tempMatrix[ts, len(tempMatrix[0]) - 1]))
                    counter += 1
                for tc in range(len(tempMatrix) - 1):
                    if tempMatrix[ts, len(tempMatrix[0]) - 1] != 0.0 and not takenCol.count(tc + 1) and tempMatrix[ts, tc] != 0.0:
                        equals[ts] = str(equals[ts]) + ' - ' + str(-1 & tempMatrix[ts, tc]) + '*' + 'x' + str(tc + 1)
            print(parameters)
            print(equals)
            listener = 3
            break
        else:
            print("Разрешающий элемент не может быть равен нулю.")
            i = i - 1
    checkListener(listener, tempMatrix, col)


def checkListener(listener, tempMatrix, col):
    if listener == 1:
        print("Ответ: ")
        print(tempMatrix)
    if listener == 2:
        print("Ответ отсутствует.")
    if listener == 3:
        print("Параметрическое решение матрицы.")


# k, s - переменные разрешающего элемента
def jordan(matrix, k, s):
    k = k - 1
    s = s - 1
    newMatrix = np.empty([len(matrix), len(matrix[0])], float)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if i != k and j != s:
                newMatrix[i, j] = ((matrix[i, j] * matrix[k, s]) - (matrix[i, s] * matrix[k, j])) / matrix[k, s]
            if i != k and j == s:
                newMatrix[i, j] = matrix[i, s] / matrix[k, s]
            if i == k and j != s:
                newMatrix[i, j] = (matrix[i, j]) / matrix[k, s]
    newMatrix[k, s] = 1 / matrix[k, s]

    return newMatrix

init()
