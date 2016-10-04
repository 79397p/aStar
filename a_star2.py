debug = False

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



def printMap(map):
    for list in map:
        s = ''
        for c in list:
            s += c
        print s

Ai = 0
Aj = 0

Bx = 0
By = 0



translate = {'.': 'space', '#': 'wall', 'A': 'A', 'B': 'B'} #because I easily forget, and I suspect that this is usefull later on


if debug: print Ai, Aj, Bx, By


#The overhead is jost to make it easier to think
def go_up(map, node, list):
    i = node.i
    j = node.j
    
    x = node.x
    y = node.y
    g = node.g
    list = createNode(list, map, i - 1, j, x, y, g)
    return list
        

def go_down(map, node, list):
    i = node.i
    j = node.j
    
    x = node.x
    y = node.y
    g = node.g
    list = createNode(list, map, i + 1, j, x, y, g)
    return list

def go_left(map, node, list):
    i = node.i
    j = node.j
    
    x = node.x
    y = node.y
    g = node.g
    list = createNode(list, map, i, j - 1, x, y, g)
    return list

def go_right(map, node, list):
    i = node.i
    j = node.j
    
    x = node.x
    y = node.y
    g = node.g
    list = createNode(list, map, i, j + 1, x, y, g)
    return list

def createNode(list, map, i, j, x, y, g):
    g_value = g

    if i < 0 or j < 0:
        return list
    elif i + 1 > len(map) or j + 1 > len(map[0]):
        return list
    c = map[i][j]
    list.append(Node(i, j, x, y, g, c))
    return list

def expand(map, node): #expand returns a list of nodes
    list = []
    list = go_up(map, node, list)
    list = go_left(map, node, list)
    list = go_down(map, node, list)
    list = go_right(map, node, list)

    #because i don't remember if python copies lists of points to them

    return list


def printTrace(map, node):
    map[node.i][node.j] = ' '
    if node.parent:
        return printTrace(map, node.parent)
    else: return map
    

class Node:
    c = ''
    
    i = 0
    j = 0

    x = 0
    y = 0

    g = 0

    status = True
    parent = None
    kids = []

    def f(self):
        return self.g + self.h()

    def h(self):
        return abs(self.i - self.x) + abs(self.j - self.y)
    
    def __init__(self, i, j, x, y, g, c):
        self.c = c
        self.i = i
        self.j = j

        self.x = x
        self.y = y
        
        self.g = g + costaAllePenga(c)

def best_first_search(map, i, j, x, y):

    map = map
    goal = (x, y)
    
    CLOSED = []
    OPEN = []

    trans_table = {}

    c = map[i][j]
    
    n0 = Node(i, j, x, y, 0, c) #give coordinates and target as input
    trans_table[str(i) + ',' + str(j)] = n0

    OPEN.append(n0)

    while True:
        if debug: print 'running'
        if OPEN == []:
            print 'oh, noes'
            return False
        X = OPEN.pop(0)
        CLOSED.append(X)
        if debug: print (X.i, X.j, X.h())

        if (X.i, X.j) == goal:
            print 'suxxed'
            if debug: print X.parent
            map = printTrace(map, X)
            printMap(map)
            return 0

        SUCC = expand(map, X) #so this should be a list of nodes

        for S in SUCC:
            S.parent = X
            key = str(S.i) + ',' + str(S.j)
            if key not in trans_table:
                trans_table[key] = S
            else:
                if debug: print 't: ' + key
                S = trans_table[key]
                
            X.kids.append(S)
            if S not in OPEN and S not in CLOSED:
                attach_and_eval(S, X)
                OPEN.append(S) #need to be sorted, fix later
                OPEN = sortNodes(OPEN)#sorting the nodes
                if debug: print S.i, S.j, S.f()
                for node in OPEN:
                    if debug: print (node.i, node.j), 'f: ', node.f()
                
            elif X.g + arc_cost(X, S) < S.g: #found cheaper path to S
                attach_and_eval(S, X)
                if S in CLOSED:
                    propagate_path_improvements(S)


def costaAllePenga(c):
    if c == 'w':return 100
    elif c == 'm': return 50
    elif c == 'f': return 10
    elif c == 'g': return 5
    else: return 1

def arc_cost(A, B): #because I suspect that this will change later on
    c = B.c
    return costaAllePenga(c)


def sortNodes(NODES):
    #print 'sorting'
    if len(NODES) < 2:
        return NODES
    result = []
    mid = int(len(NODES)/2)
    y = sortNodes(NODES[:mid])
    z = sortNodes(NODES[mid:])
    while (len(y) > 0) and (len(z) > 0):
        if y[0].f() > z[0].f():
            result.append(z.pop(0))
        else:
            result.append(y.pop(0))
    result += y
    result += z
    return result

def attach_and_eval(C, P):
    C.parent = P
    C.g = P.g + arc_cost(P, C)

def propagate_path_improvements(P):
    for C in P.kids:
        if P.g + arc_cost(P, C) < C.g:
            C.parent = P
            C.g = P.g + arc_cost(P, C)





for i in range(1, 5):
    

    print('\n\n\n')
    map = file_to_map('./boards/board-2-' + str(i) + '.txt')      
    printMap(map)
    
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 'A':
                Ai = i
                Aj = j
            elif map[i][j] == 'B':
                Bx = i
                By = j
                
                best_first_search(map, Ai, Aj, Bx, By)
