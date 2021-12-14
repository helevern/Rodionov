import pandas as pd
import numpy as np


def generation_variable_x(count_x):
    arr_x = [0 for _ in range(count_x)]
    for i in range(1, count_x + 1, 1):
        arr_x[i-1] = '-x' + str(i)
    arr_x.insert(0, '1')
    return arr_x


def transposing_colm_with_row(col, row, arr_colm, arr_row):
    arr_col = []
    for z in range(len(arr_colm)):
        if arr_colm[z] == '0=':
            arr_col.append(z)
    new_arr_colm = np.delete(np.array(arr_colm), arr_col)
    ind = arr_colm.index(new_arr_colm[col])
    arr_colm[ind] = arr_row[row]
    arr_row[row] = new_arr_colm[col]
    return arr_colm, arr_row


def generation_index(count):
    ind = ['0=' for _ in range(count)]
    return ind


def min_value_in_row(col, matrix):
    min = 999999999999999
    k = -1
    for row in range(len(matrix)):
        if matrix[row][col] > 0:
            if matrix[row][0] / matrix[row][col] < min:
                min = matrix[row][0] / matrix[row][col]
                k = row
    if k < 0:
        return -1
    return k


def replacement_variable_x_in_index(ind_x, arr_ind):
    arr = arr_ind[ind_x].split('-x')
    arr_ind[ind_x] = 'x' + arr[-1] + '='
    return arr_ind


def check_end(arr_ind):
    for val in arr_ind:
        if val == '0=':
            return False
    return True


def paint_table(matrix, arr_ind, arr_var_x):
    arr_col = []
    for col in range(len(arr_var_x)):
        if arr_var_x[col] == '0=':
            arr_col.append(col)
    arr_var_x = np.delete(np.array(arr_var_x), arr_col)
    print(pd.DataFrame(matrix, index=arr_ind, columns=arr_var_x))
    return


def algorithm(matrix, k, s):
    B = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    # шаг 4 все прочим элем. B[i][j] вычисл. по формуле 3
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            B[row][col] = (1 / matrix[k][s]) * (matrix[row][col] * matrix[k][s] - matrix[row][s] * matrix[k][col])
    # шаг 3 всем прочим элем. s столбца делим на A[k][s] и меняем знак
    for row in range(len(matrix)):
        B[row][s] = - (matrix[row][s] / matrix[k][s])
    # шаг 2 все элем. прочии k строки делим на A[k][s]
    for col in range(len(matrix[0])):
        B[k][col] = matrix[k][col] / matrix[k][s]
    # шаг 1 элем. (k,s) меняем на обратный
    B[k][s] = 1 / matrix[k][s]
    return B


def check_on_zero_row(matrix):
    count_zero = 0
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if 0 == matrix[row][col]:
                count_zero += 1
            if count_zero == len(matrix[row]):
                return row
    return False


def check_on_incompatibility(matrix, arr_ind):
    count_zero = 0
    arr_row_zero = []
    for row in range(len(matrix)):
        if not matrix[row][0] == 0:
            for col in range(1, len(matrix[row])):
                if matrix[row][col] == 0:
                    count_zero += 1
            if ((len(matrix[row]) - 1) == count_zero) and (arr_ind[row] == '0='):
                count_zero = 0
                arr_row_zero.append(row)
    return arr_row_zero


def JException(A, C, end_zero_row):
    # проверка на несовместность
    incompatibility_scheme = check_on_incompatibility(C, arr_ind)
    if len(incompatibility_scheme):
        end_zero_row = True
        return A, C, end_zero_row
    # проверка на нулевую строку
    if check_on_zero_row(C):
        row = check_on_zero_row(C)
        matrix_C = np.delete(np.array(C), row, 0)
        new_arr_ind = np.delete(np.array(arr_ind), row)
        if check_end(new_arr_ind):
            paint_table(matrix_C, new_arr_ind, arr_var_x)
            end_zero_row = True
            return A, C, end_zero_row

    print('Введите номер столбца (s):')
    s = int(input())
    # поиск мин. элем. в столбце
    k = min_value_in_row(s, C)
    if not k == -1:
        print('(k,s): ', k+1, s)
        print('Элемент (k,s): ', C[k][s])
        # Жорданово исключение
        matrix_B = algorithm(C, k, s)
        # переворачивает столбец со стокой ("-хi" с "0=")
        transposing_colm_with_row(s, k, arr_var_x, arr_ind)
        replacement_variable_x_in_index(k, arr_ind)
        # удаляем s столбец и отображаем матрицу
        matrix_C = np.delete(np.array(matrix_B), s, 1)
        paint_table(matrix_C, arr_ind, arr_var_x)
        # добавить проверну на нулевую строку,
        # если нулевая то заканчивать отображать, если больше нет в строке "0="
        # если же есть то дальше считаем и отображаем
        # как удалить нужную строку np.delete(np.array(matrix), 1, 0))
        end_zero_row = False
        return matrix_B, matrix_C, end_zero_row

    print('В данном столбце', s, 'нет подходяжего элемента, т.к. все элем. <0')
    return False


end = False
end_zero_row = False

print('Введите кол-во уравнений в системе:')
i = int(input())

print('Введите кол-во неизвестных в системе:')
j = int(input())

A = [[0 for a in range(j)] for b in range(i)]

print('Введите коэффиценты при неизвестных:')
for line in range(i):
    a = [int(el) for el in input().split()]
    if len(a) > j:
        print('Вы ввели больше коэффицентов при неизвестных, чем самих неизвестных!')
        end = True
        break
    A[line] = a

print('Введите свободные коэффиценты:')
free_var = [int(el) for el in input().split()]
if len(free_var) > i:
    print('Вы ввели больше свободных коэффицентов, чем уравнений!')
    end = True
for line in range(i):
    A[line].insert(0, free_var[line])
print('Система: ')
# создание столбцов и сторк вида "-х", "0="
arr_var_x = generation_variable_x(j)
arr_ind = generation_index(i)

print(pd.DataFrame(A, index=arr_ind, columns=arr_var_x))

C = A.copy()

while (not end):
    A, C, end_zero_row = JException(A, C, end_zero_row)
    if check_end(arr_ind) or end_zero_row:
        end = True