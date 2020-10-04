import random
import numpy as np
import _pickle as pickle

count = 16
a=np.zeros(count)
first_time=True

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

def choose_cell(a):
    c=[]
    for i in range(len(a)):
        if a[i]==0:
            c.append(i)
    #print('c')
    #print(c)
    #print('/c')

    
    #print('j', j)

    r=random.randint(0, len(c)-1)
    #print(r)
    return int(c[r])

def random_int():
    r=random.randint(1,2)*2
    return r

def do_step(a, num=1):
    for i in range(num):
        a[choose_cell(a) ] = 2

def dtoxy(d):

    if d==1:
        x=1;y=0
    if d==2:
        x=0;y=-1
    if d==3:
        x=-1;y=0
    if d==4:
        x=0;y=1
    
    return((x, y))

def is_free(b, xy, i, j): 
    '''проверка, свободна ли предыдущая клеточка с направление хода (есть ли куда двигаться текушей фишке)'''
    #xy = dtoxy(d)
    #print('is_free', xy, 'ij', i,j,'i - xy[0]*3', i - xy[0]*3, 'j - xy[1]*3;',j - xy[1]*3 )
    #print(b)
    if b[i - xy[0] ][j - xy[1] ] == 0:
        if (i - xy[0]*2)>=0 and (i - xy[0]*2)<4 and (j - xy[1]*2)>=0 and (j - xy[1]*2)<4 : 
            if b[i - xy[0]*2 ][j - xy[1]*2 ] == 0:
                if (i - xy[0]*3)>=0 and (i - xy[0]*3)<4 and (j - xy[1]*3)>=0 and (j - xy[1]*3)<4 :
                    if b[i - xy[0]*3 ][j - xy[1]*3 ] == 0:
                        return 3
                return 2
        return 1
    return 0

def move_to(b, d, i, j):
    xy = dtoxy(d)
    #print('move_to, d,xy,i,j ', d, xy,i,j)
    k = is_free(b, xy, i, j)
    if k > 0:
        #print('перемещение,i - xy[1] ,j - xy[0] , b[i][j], k', i - xy[0]*k ,j - xy[1]*k, b[i][j], k)
        #print(b)
        b[i - xy[0]*k ][j - xy[1]*k ] = b[i][j]
        b[i][j]=0
        #print(b)

def dtoij(d):
    #print(d)
    if d==1:
        ij = (1,4,1)
        ji = (0,4,1)
    if d==2:
        ij = (0,4,1)
        ji = (2,-1,-1)    
    if d==3:
        ij = (2,-1,-1)
        ji = (0,4,1)
    if d==4:
        ij = (0,4,1)
        ji = (1,4,1)
    return (ij, ji)

def move(b,d):

    #a4 w1 s2 d3
    (ij, ji)=dtoij(d)
    #print('move')
    for i in range(ij[0], ij[1], ij[2]):
        for j in range(ji[0], ji[1], ji[2]):
            #print('move i,j, b[i][j]', i,j, b[i][j] )
            if b[i][j]!=0:
                move_to(b, d, i, j)

def switch_dict(x):
    d=0
    #print('switch_dict(x):')
    #print('x=', x, type(x))
    #print('x=',x[0])
    if x[0]==112 or x[0]=='p': d=-2 #pickle and exit
    if x[0]==117 or x[0]=='u': d=6 #unpickle and continue
    if x[0]==119 or x[0]==72  or x[0]=='w' or x[0]=='A': d = 1
    if x[0]==100 or x[0]==77 or x[0]=='d' or x[0]=='C': d = 2
    if x[0]==115 or x[0]==80 or x[0]=='s' or x[0]=='B': d = 3 
    if x[0]==97 or x[0]==75 or x[0]=='a' or x[0]=='D': d = 4
    if x[0]==113 or x[0]=='q': d = -1
    #print('d=',d)
    return d

def d_to_int(d):
    #print('d_to_int d=',d)
    d0 = switch_dict(d)
    #print('d=',d,d0)
    return d0
    #if d==w:

def microcollapse(b, xy, i, j):
    #print(b)
    #print('microcollapse, i, j, i - x ,j - y, b[i - x ][j - y ], (b[i][j])*2', i, j, i - xy[0] ,j - xy[1], b[i - xy[0] ][j - xy[1] ], (b[i][j])*2 )
    b[i - xy[0] ][j - xy[1] ] = int(b[i][j])*2
    b[i][j] = 0
    #print(b)

def collapse(b, d):
    xy = dtoxy(d)
    
    t = dtoij(d)
    ij = t[0]
    ji = t[1]


    for i in range(ij[0], ij[1], ij[2]):
        for j in range(ji[0], ji[1], ji[2]):
            if b[i][j] == b[i - xy[0] ][j - xy[1] ]:
                microcollapse(b, xy, i, j )

def check_move(a,c):
    return ( not (a==c).all() )

def check_end(a):
    '''конец игры '''
    #print('check_end')
    for i in a:
        if i==0:
            return False
    return True    

def process_game(b,d):
    
    move(b, d)
    collapse(b,d)
    move(b, d)
    '''i=0
    for i in range(1): #замена while с ограничивающим контуром
        i+=1
        a_old = np.copy(b.reshape(16))
        print(a_old)
        print('process, before collapse')
        collapse(b,d)
        print('process, after collapse')
        a=b.reshape(16)
        print(a)
        print(b)
        if check_move(a, a_old):
            print('process, cheked move')
            move(b,d)
            print('process, after move')
            print(b)
        else:
            break'''
    return b

def first_step(a):
    do_step(a,2)

def player_move():
    inp = getch()
    d = d_to_int(inp)
    return d

def game(a):
    not_end = True    
    if first_time:
        #print('first')
        do_step(a)
    while (not_end):
        do_step(a)
        print('|||||||||||||||||||||||||||||||||||||||||||')
        print(a.reshape((4,4)))
        if not check_end(a):
            #print('player_move')
            d=0
            while (d==0):
                d = player_move()
            print('past player_move d=|', d, '|')
            if d<0:
                if d==-2:
                    with open('2048.pickle', 'wb') as f:
                        pickle.dump(a, f)
                print('end game')
                not_end = False
            if d==6:
                with open('2048.pickle', 'rb') as f:
                    a = pickle.load(f)
                    continue
            if not_end:
                b = process_game(a.reshape((4,4)), d)
                a = b.reshape(16) 
            #print(b)
        else:
            print('you win')

def testing(a):
    pass
def test_d_to_xy():
    print('test_d_to_xy')
    for i in range(1,5):
        print('test i=', i, 'xy=', dtoxy(i))
#test_d_to_xy()
print('Игра 2048. Клавиши - wasd, стрелочки, q для выхода, p и u для сохранения/загрузки')
game(a)

                    
