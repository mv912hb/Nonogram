from typing import *

WHITE = 0
BLACK = 1
EMPTY = -1


def row_variations(row: List[int], bloks: List[int]):
    return row_variations_helper(row, bloks, 0, 0, [])



def checker(row):
    summation = 0
    for element in row:
        if element > 0:
            summation += element
    return summation


def row_variations_helper(row: List[int], blocks: List[int], index_constraint: int, row_ind: int, results_list: List[List[int]]):

    if index_constraint == len(blocks) or checker(row) == sum(blocks):
        for cell in range(len(row)):
            if row[cell] == EMPTY:
                row[cell] = WHITE
        if row not in results_list and checker_1(blocks, row):
            results_list.append(row[:])
        return results_list

    temp_row = row[:]
    for option in first_constraint(temp_row, blocks[index_constraint], row_ind):
        if EMPTY in option[0]:
            row_ind = option[1] + 1
            row_variations_helper(option[0], blocks, index_constraint + 1, row_ind, results_list)
        else:
            if checker_1(blocks, option[0]) and option[0] not in results_list:
                results_list.append(option[0][:])
    return results_list


def first_constraint(row: List[int], constraint: int, row_ind: int):
    sequences = []
    list_index_start = []
    list_index_start_filter = []
    list_index = []
    list_of_black = []
    if BLACK not in row and EMPTY not in row:
        return []

    for i in range(row_ind, len(row)):
        if row[i] == BLACK:
            list_of_black.append(i)
        if row[i] == BLACK or row[i] == EMPTY:
            list_index_start.append(i)

    for i in range(len(list_index_start)):
        if list_index_start[i] + constraint <= len(row):
            list_index_start_filter.append(list_index_start[i])

    for i in range(len(list_index_start_filter)):
        flag = True
        if constraint == 1 and i + 1 != len(list_index_start_filter):
            if row[list_index_start_filter[i] + 1] == 1:
                flag = False

            elif constraint == 1 and i - 1 >= 0:
                if row[list_index_start_filter[i] - 1] == 1:
                    flag = False
        else:
            for j in range(constraint):
                if row[list_index_start_filter[i] + j] == 0:
                    flag = False
                    break
        if flag:
            list_index.append(list_index_start_filter[i])
    last_list_index = list_index
    for i in range(len(last_list_index)):
        tmp = row[::]
        start = last_list_index[i]
        end = last_list_index[i] + constraint
        for j in range(len(row)):
            if j == start - 1 or j == end:
                if tmp[j] != BLACK:
                    tmp[j] = WHITE
            elif j < start - 1:
                if tmp[j] == EMPTY:
                    tmp[j] = WHITE
            elif j >= start and j < end:
                tmp[j] = BLACK
        if tmp not in sequences:
            temp_with_ind = tmp, end
            sequences.append(temp_with_ind)
    return sequences


def constraint_satisfactions(n, blocks):
    if len(blocks) == 0:
        return [[0] * n]
    if n <= 0:
        return
    return satisfactions_helper(n, 0, 0, blocks, [], [0] * n)


def satisfactions_helper(n: int, ind1: int, ind2: int, blocks: List, results:
List[list], temp_list: List) -> List[List[int]]:
    if ind1 == len(blocks):
        if sum(temp_list) == sum(blocks):
            results.append(temp_list[::1])
        return results
    for i in range(ind2, n - blocks[ind1] + 1):
        temp_list[i: i + blocks[ind1]] = [1] * blocks[ind1]
        satisfactions_helper(n, ind1 + 1, i + blocks[ind1] + 1, blocks,
                             results, temp_list)
        temp_list[i: i + blocks[ind1]] = [0] * blocks[ind1]
    return results


def intersection_row(rows: List[List[int]]):
    if len(rows) != 0:
        intersection = []
        for i in range(len(rows[0])):
            flag = True
            current_square = rows[0][i]
            for j in range(len(rows)):
                if current_square == -1:
                    current_square = rows[j][i]
                if rows[j][i] != current_square and rows[j][i] != -1:
                    flag = False
                    break
            if flag:
                intersection.append(current_square)
            else:
                intersection.append(-1)
        return intersection
    return []


def check_row(row, variations):
    new_list = []
    for variable in variations:
        counter = 0
        for j in range(len(row)):
            if row[j] != 1 and variable[j] == 1:
                counter += 1
                break
        if counter == 0:
            new_list.append(variable)
    return new_list

def create_board(lenght, high):
    board = []
    for i in range(high):
        row = []
        for j in range(lenght):
            row.append(EMPTY)
        board.append(row)
    return board


def exit_condition(board):
    for row in board:
        if -1 in row:
            return True
    return False


def solve_easy_nonogram(constraints: List[List], board = []):
    shift_changing = 1
    constraints_for_row = constraints[0]
    constraints_for_col = constraints[1]
    if not board:
        board = create_board(len(constraints_for_col), len(constraints_for_row))

    while exit_condition(board) and shift_changing != 0:
        shift_changing = 0
        shift_changing_up = solve_easy_nonogram_helper(constraints_for_row,
                                                     board, shift_changing)
        shift_changing = shift_changing + shift_changing_up[0]
        if shift_changing_up[1] == None:
            return None
        board = update_board(board)

        shift_changing_up = solve_easy_nonogram_helper(constraints_for_col,
                                                     board, shift_changing)
        shift_changing = shift_changing + shift_changing_up[0]
        board = update_board(board)
        if shift_changing_up[1] == None:
            return None
    return board



def solve_easy_nonogram_helper(constraints, board, shift_changing = 0):
    for row in range(len(constraints)):
        result_row = intersection_row(row_variations(board[row],
                                                     constraints[row]))
        if not result_row:
            return shift_changing, None
        if result_row != board[row]:
            shift_changing += 1
            board[row] = result_row

    return shift_changing, 1



def print_board(board):
    for row in board:
        print(row)


def update_board(matrix):
    updated_board: list = []
    for symbol in range(len(matrix[0])):
        line_board = []
        for line in range(len(matrix)):
            line_board.append(matrix[line][symbol])
        updated_board.append(line_board)
    return updated_board


def checker_1(constrains, ints):

    string_ints = [str(int) for int in ints]
    str_of_ints = "".join(string_ints).split("0")
    str_of_ints_up = []
    for element in str_of_ints:
        if element:
            str_of_ints_up.append(element)

    if len(str_of_ints_up) != len(constrains):
        return False
    for element in range(len(str_of_ints_up)):
        if len(str_of_ints_up[element]) != constrains[element]:
            return False
    return True


def solve_nonogram(constraints: List[List[List[int]]]):
    solution = solve_easy_nonogram(constraints)
    if not exit_condition(solution):
        return [solution]
    return solver_helper(constraints, solution, [])


def solver_helper(constraints, solution, solutions):
    if solve_easy_nonogram(constraints, solution) == None:
        return solutions
    if not exit_condition(solution):
        check_solution = solution[::]
        check_solution = update_board(check_solution)
        if solve_easy_nonogram_helper(constraints[1], check_solution) != (0, None):
            if solution not in solutions:
                solutions.append(solution[::])
                return solutions
    for row in range(len(solution)):
        if -1 in solution[row]:
            variations = row_variations(solution[row], constraints[0][row])
            for option in variations:
                current_option = solution[row][::]
                solution[row] = option
                solver_helper(constraints, solution, solutions)
                solution[row] = current_option
    return solutions
