#此程式碼主參考chatGPT並予以修改，並未參考除chatGPT外任何網站
objs = ["人", "狼", "羊", "菜"]
state = [0, 0, 0, 0]

def neighbors(s):
    side = s[0]
    next_states = []
    checkAdd(next_states, move(s, 0))
    for i in range(1, len(s)):
        if s[i] == side:
            checkAdd(next_states, move(s, i))
    return next_states

def checkAdd(next_states, s):
    if not isDead(s):
        next_states.append(s)

def isDead(s):
    if s[1] == s[2] and s[1] != s[0]: # 狼吃羊
        return True
    if s[2] == s[3] and s[2] != s[0]: # 羊吃菜
        return True
    return False

# 人带着 obj 移到另一边
def move(s, obj):
    new_s = s.copy() # 复制一份列表
    side = s[0]
    another_side = 1 - side
    new_s[0] = another_side
    new_s[obj] = another_side
    return new_s 

visited_map = {}

def visited(s):
    str_s = ''.join(map(str, s))
    return str_s in visited_map

def isSuccess(s):
    for i in range(len(s)):
        if s[i] == 0:
            return False
    return True

def state2str(s):
    str_state = ""
    for i in range(len(s)):
        str_state += objs[i] + str(s[i]) + " "
    return str_state

path = []

def printPath(path):
    for s in path:
        print(state2str(s))

def dfs(s):
    if visited(s):
        return
    path.append(s)
    if isSuccess(s):
        print("success!")
        printPath(path)
        return
    visited_map[''.join(map(str, s))] = True
    neighbors_list = neighbors(s)
    for next_s in neighbors_list:
        dfs(next_s)
    path.pop()

dfs(state)
