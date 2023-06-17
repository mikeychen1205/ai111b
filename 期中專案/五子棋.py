import numpy as np

# 定義棋盤大小
BOARD_SIZE = 15

# 定義棋盤狀態
EMPTY = 0
BLACK = 1
WHITE = 2

# 創建一個空的棋盤
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

# 定義下棋函數
def make_move(row, col, player):
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
        # 檢查是否在有效的範圍內
        print("無效的位置！")
        return False
    if board[row, col] != EMPTY:
        # 檢查該位置是否已經有棋子
        print("該位置已經有棋子！")
        return False
    
    # 在指定位置下棋
    board[row, col] = player
    return True

# 定義檢查是否勝利的函數
def check_win(player):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row, col] == player:
                # 檢查水平方向是否有五子連線
                if col + 4 < BOARD_SIZE and np.all(board[row, col:col+5] == player):
                    return True
                # 檢查垂直方向是否有五子連線
                if row + 4 < BOARD_SIZE and np.all(board[row:row+5, col] == player):
                    return True
                # 檢查右上斜方向是否有五子連線
                if col + 4 < BOARD_SIZE and row - 4 >= 0 and np.all(board[row-4:row+1, col:col+5] == player):
                    return True
                # 檢查右下斜方向是否有五子連線
                if col + 4 < BOARD_SIZE and row + 4 < BOARD_SIZE and np.all(board[row:row+5, col:col+5] == player):
                    return True
    return False

# 定義虛擬對手下棋函數
def make_computer_move(player):
    # 優先攻擊
    if make_winning_move(player):
        return True
    # 其次防守
    if make_defensive_move(player):
        return False
    # 隨機下棋
    empty_cells = np.argwhere(board == EMPTY)
    np.random.shuffle(empty_cells)
    for cell in empty_cells:
        row, col = cell
        if make_move(row, col, player):
            if check_win(player):
                return True
            break
    return False

# 定義攻擊策略，嘗試形成連線
def make_winning_move(player):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row, col] == EMPTY:
                if check_winning_line(row, col, player):
                    make_move(row, col, player)
                    return True
    return False

# 檢查是否形成連線
def check_winning_line(row, col, player):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for direction in directions:
        count = 0
        for i in range(1, 5):
            r = row + direction[0] * i
            c = col + direction[1] * i
            if r < 0 or r >= BOARD_SIZE or c < 0 or c >= BOARD_SIZE:
                break
            if board[r, c] == player:
                count += 1
            elif board[r, c] != EMPTY:
                break
        if count == 4:
            return True
    return False

# 定義防守策略，阻止玩家形成連線
def make_defensive_move(player):
    opponent = WHITE if player == BLACK else BLACK
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row, col] == EMPTY:
                if check_winning_line(row, col, opponent):
                    make_move(row, col, player)
                    return True
    return False

# 主遊戲循環
def play_game():
    player = BLACK
    while True:
        print(board)  # 輸出當前棋盤
        if player == BLACK:
            print("輪到黑棋下！")
            row = int(input("請輸入行數(0-14):"))
            col = int(input("請輸入列數(0-14):"))
            if make_move(row, col, player):
                if check_win(player):
                    print(board)
                    print("遊戲結束，黑棋獲勝！")
                    break
                player = WHITE
        else:
            print("輪到白棋下！")
            if make_computer_move(player):
                print(board)
                print("遊戲結束，白棋獲勝！")
                break
            player = BLACK

# 運行遊戲
play_game()

