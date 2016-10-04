
def file_to_map(s = './boards/board-1-1.txt'):
    map = []
    file = open(s)

    for line in file:

        line = line.strip()

        list = []
        for char in line:
            list.append(char)
            
        map.append(list)
    return map

map = file_to_map()
for list in map:
    print list

Ai = 0
Aj = 0

Bx = 0
By = 0



translate = {'.': 'space', '#': 'wall', 'A': 'A', 'B': 'B'} #because I easily forget, and I suspect that this is usefull later on


for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] == 'A':
            Ai = i
            Aj = j
        elif map[i][j] == 'B':
            Bx = i
            By = j
            
print Ai, Aj, Bx, By


#The overhead is jost to make it easier to think
def go_up(map, node, list):
    i = node.i
    j = node.j
    
    x = node.x
    y = node.y
    g = node.g

    if i > 0:
        n = Node(i - 1, j, x, y, g)
        list.append(n)
    return list
        

def go_down(map, node, list):
    i = node.i
    j = node.j
    
    x = node.x
    y = node.y
    g = node.g

    if i < len(map):
        n = Node(i + 1, j, x, y, g)
        list.append(n)
    return list

def go_left(map, node, list):
    i = node.i
    j = node.j
    
    x = node.x
    y = node.y
    g = node.g

    if j > 0:
        n = Node(i, j - 1, x, y, g)
        list.append(n)
    return list

def go_down(map, node, list):
    i = node.i
    j = node.j
    
    x = node.x
    y = node.y
    g = node.g

    if i < len(map[0]):
        n = Node(i, j + 1, x, y, g)
        list.append(n)
    return list

def expand(map, node): #expand returns a list of nodes
    list = []
    list = go_down(map, node, list)
    list = go_up(map, node, list)
    list = go_left(map, node, list)
    list = go_down(map, node, list)

    #because i don't remember if python copies lists of points to them

    return list

    

class Node:
    i = 0
    j = 0

    x = 0
    y = 0

    g = 0
    h = 0
    f = 0
    
    #status
    parent = None
    kids = []

    def h(self):
        return abs(self.i - self.x) + abs(self.j - self.y)
    
    def __init__(self, i, j, x, y, g):
        self.i = i
        self.j = j

        self.x = x
        self.y = y
        
        g = g + 1
        
        
def best_first_search(map, i, j, x, y):

    map = map
    goal = (x, y)
    
    CLOSED = []
    OPEN = []
    n0 = Node(i, j, x, y, 0) #give coordinates and target as input

    OPEN.append(n0)

    while True:
        if OPEN == []:
            return False
        X = OPEN.pop()
        CLOSED.append(X)

        #if x is sollution return something (x, succeed)

        SUCC = expand(map, X) #so this should be a list of nodes

        for S in SUCC:
            #if note S* has previously been created, and is state(S*)
            X.kids.append(S)
            if S not in OPEN and S not in CLOSED:
                attach_and_eval(S, X)
                OPEN.append(S) #need to be sorted, fix later
            elif X.g + arc_cost(X, S) < S.g: #found cheaper path to S
                attach_and_eval(S, X)
                if S in CLOSED:
                    propagate_path_improvements(S)

def arc_cost(A, B):
    return 1

def attach_and_eval(C, P):
    C.parent = P
    C.g = P.g + arc_cost(P, C)
    C.f = C.g + C.h()

def propagate_path_improvements(P):
    for C in P.kids:
        if P.g + arc_cost(P, C) < C.g:
            C.parent = P
            C.g = P.g + arc_cost(P, C)
            C.f = C.g + C.h()


best_first_search(map, Ai, Aj, Bx, By)
