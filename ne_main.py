import numpy as np


# Шаг жардановых исключений
def zhordan(matrix, k, s):
    k = k - 1
    s = s - 1

    newmatr = np.empty([len(matrix), len(matrix[0])], float)
    for rows in range(len(matrix)):
        for cols in range(len(matrix[0])):
            if rows != k and cols != s:
                newmatr[rows][cols] = ((matrix[rows][cols] * matrix[k][s]) - (matrix[rows][s] * matrix[k][cols])) / \
                                      matrix[k][s]
            if rows != k and cols == s:
                newmatr[rows][cols] = (matrix[rows][s]) / matrix[k][s]
            if rows == k and cols != s:
                newmatr[rows][cols] = (-1 * matrix[rows][cols]) / matrix[k][s]
    newmatr[k][s] = 1 / matrix[k][s]

    return newmatr


if __name__ == '__main__':
    print('Входящие элементы матрицы A|B:\n')
    m = int(input('Колличество строк: '))
    n = int(input('Колличество столбцов с учетом Столбцв вводных членов: '))
    matr = np.empty([m, n], float)
    print('Элементы матрицы:\n')
    head = []
    for i in range(m):
        for j in range(n):
            matr[i][j] = float(input())
    for h in range(n - 1):
        head.append('x' + str(h + 1))
    head.append('B')
    print(head)
    print(matr)
    tmpmatr = matr
    usedrows = []
    usedcols = []
    flag = 0
    for repeats in range(len(matr[0]) - 1):
        r = int(input('Номер строки разрешающего элемента a[k][s]:'))
        c = int(input('Номер столбца разрешающего элемента a[k][s]:'))
        if tmpmatr[r - 1][c - 1] != 0 and c < len(tmpmatr[0]) and not usedrows.count(r):
            usedrows.append(r)
            usedcols.append(c)
            print('Шаг метода Жордановых исключений:')
            tmpmatr = zhordan(tmpmatr, r, c)
            print(tmpmatr)
            flag = 0
        elif tmpmatr[r - 1][c - 1] == 0 and tmpmatr[r - 1][len(tmpmatr[0]) - 1] == 1:
            flag = 1
        elif tmpmatr[r - 1][c - 1] == 0 and tmpmatr[r - 1][len(tmpmatr[0]) - 1] == 0:
            params = []
            eqs = []
            count = 1
            for ur in range(len(tmpmatr)):
                for uc in range(len(tmpmatr[0]) - 1):
                    if tmpmatr[ur][uc] == 0.0 and tmpmatr[ur][len(tmpmatr[0]) - 1] == 0.0:
                        params.append('x' + str(count) + '=param' + str(count))
                        count += 1
            for ur in range(len(tmpmatr)):
                if tmpmatr[ur][len(tmpmatr[0]) - 1] != 0.0:
                    eqs.append('x' + str(count) + '=' + str(-1 * tmpmatr[ur][len(tmpmatr[0]) - 1]))
                    count += 1
                for uc in range(len(tmpmatr[0]) - 1):
                    if tmpmatr[ur][len(tmpmatr[0]) - 1] != 0.0 and not usedcols.count(uc+1) and tmpmatr[ur][uc] != 0.0:
                        eqs[ur] = str(eqs[ur]) + ' - ' + str(-1 * tmpmatr[ur][uc]) + '*' + 'x' + str(uc + 1)
            print(params)
            print(eqs)
            flag = 2
            break
        else:
            print('a[k][s] не должен быть равен 0')
            repeats = repeats - 1
    if flag == 0:
        print('Решение:')
        print(-1 * tmpmatr[:, n - 1])
    if flag == 1:
        print('0 == 1')
        print('Нет решений для это матрицы!')
    if flag == 2:
        print('0 == 0')
        print('Параметрическое решение для этой матрицы!')
