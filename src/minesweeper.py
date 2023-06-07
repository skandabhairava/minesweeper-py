import random

def populate_bombs():
    board = [["" for _ in range(20)] for _ in range(20)]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if random.randint(0, 19) == 0:
                board[j][i] = "X"

    return board

def printb(board):
    for i in board:
        for j in i:
            print(j, end=" ")
        print()

def check_bomb(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            #check each pos around u
            count = 0
            if board[i][j] == "X":
                continue
            for dx in range(3):
                    for dy in range(3):
                        if dx-1+j >=0 and dy-1+i>=0:
                            dxx = dx-1+j
                            dyy = dy-1+i
                        else:
                            continue
                        #
                        if not (dxx < len(board[i]) and dyy < len(board)):
                            continue
                        #
                        #print(dyy, dxx)
                        if board[dyy][dxx] == "X":
                                count += 1
            board[i][j] = count



board = populate_bombs()
check_bomb(board)
hidden_board = [["☐" for x in range(len(board[0]))] for y in range(len(board))]

ans_board = [["☐" if board[y][x] == "X" else board[y][x] for x in range(len(board[0]))] for y in range(len(board))]

def propagate(matrix, pos: tuple[int, int], iterations):
    queue1: list[tuple[int, int]] = []

    hidden_board[pos[0]][pos[1]] = matrix[pos[0]][pos[1]]

    if ((pos[0] + 1) < len(matrix)) and (matrix[(pos[0] + 1)][(pos[1])] != "X"):
        queue1.append((pos[0]+1, pos[1]))
    
    if ((pos[1]+1) < len(matrix[0])) and (matrix[(pos[0])][(pos[1] + 1)] != "X"):
        queue1.append((pos[0], pos[1]+1))

    if ((pos[1] - 1) >= 0) and (matrix[(pos[0])][(pos[1]-1)] != "X"):
        queue1.append((pos[0], pos[1]-1))

    if ((pos[0]-1) >= 0) and (matrix[(pos[0] - 1)][(pos[1])] != "X"):
        queue1.append((pos[0]-1, pos[1]))

    if iterations == 0:
        return
    
    for item in queue1:
        hidden_board[item[0]][item[1]] = matrix[item[0]][item[1]]
        propagate(matrix, item, iterations-1)

    """ queue1.append(
                                        matrix[pos[0] - 1][pos[1]],
        matrix[pos[0]][pos[1] - 1],        matrix[pos[0]][pos[1]],         matrix[pos[0]][pos[1] + 1],
                                        matrix[pos[0] + 1][pos[1]]
            
    ) """


hint_list = list("ABCDEFGHIJKLMNOPQRST")

def clear_screen():
    for i in range(30):
        print()

def print_full_board(board):
    print("  " + " ".join(hint_list))
    for i in range(len(board)):
        print(hint_list[i], end=" ")
        for j in board[i]:
            print(j, end=" ")
        print()

#propagate(board, ((len(board)-1)//2, (len(board)-1)//2), 3)
while True:
    print_full_board(hidden_board)

    if hidden_board == ans_board:
        print("YOU WON!!!")
        break

    select = input("Enter selection (ROW)(COLUMN): ")
    if (select[0] in hint_list) and (select[1] in hint_list):
        y, x = (hint_list.index(select[0]), hint_list.index(select[1]))

        if board[y][x] == "X":
            clear_screen()
            print("Game Over!")
            print_full_board(board)
            break

        if hidden_board[y][x] == "☐":
            propagate(board, (y, x), 3)
            clear_screen()
            continue

    
    clear_screen()
    print("Invalid Selection!")