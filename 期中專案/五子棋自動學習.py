import numpy as np
import tensorflow as tf

# 定義遊戲相關常數
BOARD_SIZE = 15
EMPTY = 0
PLAYER = 1
AI_PLAYER = 2

# 初始化棋盤
def initialize_board():
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int)
    return board

# 檢查遊戲是否結束
def game_over(board):
    # 檢查水平方向是否有五子連線
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE - 4):
            if np.all(board[i, j:j+5] == PLAYER) or np.all(board[i, j:j+5] == AI_PLAYER):
                return True
    
    # 檢查垂直方向是否有五子連線
    for i in range(BOARD_SIZE - 4):
        for j in range(BOARD_SIZE):
            if np.all(board[i:i+5, j] == PLAYER) or np.all(board[i:i+5, j] == AI_PLAYER):
                return True
    
    # 檢查左上到右下方向是否有五子連線
    for i in range(BOARD_SIZE - 4):
        for j in range(BOARD_SIZE - 4):
            if np.all(np.diagonal(board[i:i+5, j:j+5]) == PLAYER) or np.all(np.diagonal(board[i:i+5, j:j+5]) == AI_PLAYER):
                return True
    
    # 檢查右上到左下方向是否有五子連線
    for i in range(BOARD_SIZE - 4):
        for j in range(4, BOARD_SIZE):
            if np.all(np.diagonal(board[i:i+5, j-4:j+1]) == PLAYER) or np.all(np.diagonal(board[i:i+5, j-4:j+1]) == AI_PLAYER):
                return True
    
    # 檢查是否平局
    if np.count_nonzero(board == EMPTY) == 0:
        return True
    
    return False

# 獲取合法行動
def get_valid_actions(board):
    valid_actions = np.where(board.flatten() == EMPTY)[0]
    return valid_actions

# 在棋盤上執行行動
def make_move(board, action, player):
    board[action // BOARD_SIZE][action % BOARD_SIZE] = player
    return board

# 遊戲結果
def get_game_result(board):
    if np.all(board == PLAYER):
        return "玩家勝利"
    elif np.all(board == AI_PLAYER):
        return "電腦勝利"
    else:
        return "平局"

# 定義深度神經網絡模型
def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(BOARD_SIZE*BOARD_SIZE,)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(BOARD_SIZE*BOARD_SIZE, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    return model

# 將棋盤狀態轉換為模型輸入格式
def preprocess_state(board):
    state = np.array(board.flatten(), dtype=np.float32)
    state[state == PLAYER] = -1.0  # 將玩家棋子設為-1.0
    state[state == AI_PLAYER] = 1.0  # 將電腦棋子設為1.0
    return state

# 自我對弈遊戲
def self_play(model):
    board = initialize_board()  # 初始化棋盤
    
    while not game_over(board):
        # 獲取當前狀態
        state = preprocess_state(board)
        
        # 使用模型預測行動概率分佈
        action_probs = model.predict(np.expand_dims(state, axis=0))[0]
        
        # 過濾出合法行動
        valid_actions = get_valid_actions(board)
        valid_action_probs = [action_probs[action] for action in valid_actions]
        
        # 根據行動概率分佈選擇行動
        action = np.random.choice(valid_actions, p=valid_action_probs)
        
        # 在棋盤上執行行動
        board = make_move(board, action, AI_PLAYER)
        
    # 獲取遊戲結果（勝利、平局、失敗）
    result = get_game_result(board)
    
    return result

# 訓練模型
def train_model():
    model = build_model()  # 初始化模型
    
    for epoch in range(num_epochs):
        # 收集自我對弈數據
        data = []
        for _ in range(num_games_per_epoch):
            result = self_play(model)
            data.append(result)
        
        # 輸出訓練進度
        print('Epoch: {}, Results: {}'.format(epoch, data))
    
    return model

# 設定訓練參數
num_epochs = 10
num_games_per_epoch = 100

# 訓練模型
trained_model = train_model()

# 測試訓練好的模型
def test_model(model):
    board = initialize_board()  # 初始化棋盤
    
    while not game_over(board):
        # 獲取當前狀態
        state = preprocess_state(board)
        
        # 使用模型預測行動概率分佈
        action_probs = model.predict(np.expand_dims(state, axis=0))[0]
        
        # 過濾出合法行動
        valid_actions = get_valid_actions(board)
        valid_action_probs = [action_probs[action] for action in valid_actions]
        
        # 根據行動概率分佈選擇行動
        action = np.random.choice(valid_actions, p=valid_action_probs)
        
        # 在棋盤上執行行動
        board = make_move(board, action, AI_PLAYER)
    
    # 獲取遊戲結果
    result = get_game_result(board)
    print('遊戲結束！結果：{}'.format(result))

# 使用訓練好的模型進行遊戲
test_model(trained_model)
