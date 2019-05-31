from tkinter import *
import numpy as np
import time
import threading
import random
from collections import Counter
from numpy.random import permutation
import math
from functools import partial

c_index = 1
c_tab = ["white"]

class OneSquare():
    def __init__(self, can, start_x, start_y, end_x, end_y,color,i,j, tab):
        #inicjalizacja
        global c_index
        global c_tab
        self.can=can
        self.id = self.can.create_rectangle((start_x, start_y,
                  end_x, end_y), fill=color)
        self.can.tag_bind(self.id, "<ButtonPress-1>", lambda event, arg=tab: self.set_color(event, arg))
        self.i = i
        self.j = j
        self.color = color
        if color!="white" and color in c_tab:
            self.can.itemconfigure(self.id, fill=color)
            self.color = color
            tab[self.i][self.j] = c_tab.index(self.color)

        elif color!="white":
            tab[self.i][self.j] = c_index
            c_tab.append(self.color)
            c_index += 1

    def set_color(self, event, tab):
        #zmien kolor
        global c_index
        global c_tab
        if self.color == "white":
            color='#{:02x}{:02x}{:02x}'.format(r(), r(), r())
            val = c_index
            c_tab.append(color)
            c_index += 1
        else:
            color="white"
            val = 0

        tab[self.i][self.j] = val
        self.can.itemconfigure(self.id, fill=color)
        self.color = color

def shuffle2d(arr2d, rand=random):
    #2d randomizer
    reshape = []
    data = []
    iend = 0
    for row in arr2d:
        data.extend(row)
        istart, iend = iend, iend+len(row)
        reshape.append((istart, iend))
    rand.shuffle(data)
    return [data[istart:iend] for (istart,iend) in reshape]

def create(numel):
    #utworz wstepna tablice
    global e_tab
    tab = np.zeros(numel * numel).reshape(numel, numel)
    e_tab = np.zeros(numel * numel).reshape(numel, numel)
    return tab

def sc_create(numel):
    tab = np.random.rand(numel * numel).reshape(numel, numel)
    return tab

def pause():
    global paused
    global neigh
    if not paused:
        paused = True
    else:
        paused = False
        show(tab, numel, neigh)

def show(tab, numel, neigh):
    global paused
    neigh = my_var2.get()
    rnd = isRand.get()
    opt = side.get()
    if not paused:
        if neigh=="Moore":
            moore(tab,numel)
        elif neigh=="Neumann":
            neumann(tab,numel)
        elif neigh=="Pentagonal":
            penta(tab,numel)
        elif neigh=="Hexagonal":
            if rnd:
                hexa(tab,numel, 3)
            else:
                hexa(tab,numel, opt)
        elif neigh=="In radius":
            growthRange(tab,numel,int(entry_r.get()))
        prints(tab,numel)
        threading.Timer(1.0, show,(tab,numel,neigh)).start()


def prints(tab, numel):
    can.delete(ALL)
    global c_tab
    global paused
    c = 0
    for i in range(0, numel):
        for j in range(0, numel):
            if tab[i][j]==0:
                c+=1
            OneSquare(can, scale * j, scale * i, scale * j + scale, scale * i + scale, c_tab[int(tab[i][j])], i, j, tab)
    if c<=0 and not paused:
        paused=True

def print_energy():
    can.delete(ALL)
    global e_tab
    global numel
    global paused
    c = 0
    for i in range(0, numel):
        for j in range(0, numel):
            if e_tab[i][j]==0:
                can.create_rectangle(scale * j, scale * i, scale * j + scale, scale * i + scale, fill="white")
                #OneSquare(can, scale * j, scale * i, scale * j + scale, scale * i + scale, "white", i, j, tab)
            else:
                # can.create_rectangle(scale * j, scale * i, scale * j + scale, scale * i + scale, fill="#191970")
                nr = int(e_tab[i][j]*32)
                if nr>0:
                    nr-=1
                can.create_rectangle(scale * j, scale * i, scale * j + scale, scale * i + scale, fill="#1919{:02x}".format(nr))
                #OneSquare(can, scale * j, scale * i, scale * j + scale, scale * i + scale, "#191970", i, j, tab)
    if not paused:
        paused=True

def selected():
    global tab
    global numel
    global sc_tab
    global neigh

    numel = int(entry2.get())

    tab = create(numel)
    sc_tab = sc_create(numel)
    prints(tab, numel)

    opt = my_var.get()
    neigh = my_var2.get()

    rad = int(entry_r.get())
    rows = int(entry_i.get())
    cols = int(entry_j.get())
    amount = int(entry_rnd.get())
    
    if opt == "Homogenous":
        homo(tab, rows, cols)
    elif opt == "In range":
        in_range(tab, rad)
    elif opt == "Manual choose":
        man(tab, numel)
    elif opt == "Random":
        rnd(tab, numel, amount)
    else:
        print("stuff")
        pass

def homo(tab, a, b):
    #jednorodnie
    step1 = int(numel/a)+1
    step2 = int(numel/b)+1

    i=0
    j=0

    while i<numel:
        while j<numel:
            color='#{:02x}{:02x}{:02x}'.format(r(), r(), r())
            OneSquare(can,scale*j,scale*i,scale*j+scale,scale*i+scale,color,i,j,tab)
            j+=step2
        j=0
        i+=step1


def neighbors(mat, row, col, radius):
    #sasiedztwo w promieniu
    rows, cols = len(mat), len(mat[0])
    c = 0

    for i in range(row - radius, row + radius + 1):
        for j in range(col - radius, col + radius + 1):
            if 0 <= i < rows and 0 <= j < cols:
                if mat[i][j]!=0:
                    c+=1
    return c

def in_range(tab, rad):
    #w promieniu
    for i in permutation(numel):
        for j in permutation(numel):
            c = neighbors(tab, i, j, rad)
            if c==0:
                color='#{:02x}{:02x}{:02x}'.format(r(), r(), r())
                OneSquare(can,scale*j,scale*i,scale*j+scale,scale*i+scale,color,i,j,tab)


def man(tab, numel):
    #ręcznie
    #choose and run
    pass

def rnd(tab, numel, amount):
    #losowo
    cnt = 1
    tab2 = tab.copy()
    for i in range(0, numel):
        for j in range(0, numel):
            tab2[i][j] = 1
            cnt+=1
            if cnt>amount:
                break
        if cnt>amount:
            break

    tab2 = shuffle2d(tab2)

    for i in range(0, numel):
        for j in range(0, numel):
            if tab2[i][j]!=0:
                color='#{:02x}{:02x}{:02x}'.format(r(), r(), r())
                OneSquare(can,scale*j,scale*i,scale*j+scale,scale*i+scale,color,i,j,tab)


def moore(tab, N):
    #moore
    global c_tab
    tab2 = tab.copy()
    y = None
    for i in range(N):
        for j in range(N):
            n_tab = []
            n_tab.append(int(tab[i, (j - 1) % N]))
            n_tab.append(int(tab[i, (j + 1) % N]))
            n_tab.append(int(tab[(i - 1) % N, j]))
            n_tab.append(int(tab[(i + 1) % N, j]))
            n_tab.append(int(tab[(i - 1) % N, (j - 1) % N]))
            n_tab.append(int(tab[(i - 1) % N, (j + 1) % N]))
            n_tab.append(int(tab[(i + 1) % N, (j - 1) % N]))
            n_tab.append(int(tab[(i + 1) % N, (j + 1) % N]))

            l = len(n_tab)
            k = 0
            while k in n_tab:
                n_tab.remove(k)

            if n_tab:
                if n_tab[0]!=0 and tab[i,j]==0:
                    winner = [word for word, word_count in Counter(n_tab).most_common(1)]
                    tab2[i,j] = winner[0]
    tab[:] = tab2[:]

def neumann(tab, N):
    #von neumann
    global c_tab
    tab2 = tab.copy()
    y = None
    for i in range(N):
        for j in range(N):
            n_tab = []
            n_tab.append(int(tab[i, (j - 1) % N]))
            n_tab.append(int(tab[i, (j + 1) % N]))
            n_tab.append(int(tab[(i - 1) % N, j]))
            n_tab.append(int(tab[(i + 1) % N, j]))

            l = len(n_tab)
            k = 0
            while k in n_tab:
                n_tab.remove(k)

            if n_tab:
                if n_tab[0] != 0 and tab[i, j] == 0:
                    winner = [word for word, word_count in Counter(n_tab).most_common(1)]
                    tab2[i, j] = winner[0]
    tab[:] = tab2[:]

def hexa(tab, N, opt):
    #hexagonal edit
    global c_tab
    tab2 = tab.copy()
    repeat = False
    for i in range(N):
        for j in range(N):
            n_tab = []
            if repeat:
                opt = 3

            if opt==3:
                opt=random.randint(1,2)
                repeat = True

            if opt==1:
                n_tab.append(int(tab[i, (j - 1) % N]))
                n_tab.append(int(tab[i, (j + 1) % N]))
                n_tab.append(int(tab[(i - 1) % N, j]))
                n_tab.append(int(tab[(i + 1) % N, j]))
                n_tab.append(int(tab[(i - 1) % N, (j + 1) % N]))
                n_tab.append(int(tab[(i + 1) % N, (j - 1) % N]))

            elif opt==2:
                n_tab.append(int(tab[i, (j - 1) % N]))
                n_tab.append(int(tab[i, (j + 1) % N]))
                n_tab.append(int(tab[(i - 1) % N, j]))
                n_tab.append(int(tab[(i + 1) % N, j]))
                n_tab.append(int(tab[(i - 1) % N, (j - 1) % N]))
                n_tab.append(int(tab[(i + 1) % N, (j + 1) % N]))

            l = len(n_tab)
            k = 0
            while k in n_tab:
                n_tab.remove(k)

            if n_tab:
                if n_tab[0]!=0 and tab[i,j]==0:
                    winner = [word for word, word_count in Counter(n_tab).most_common(1)]
                    tab2[i,j] = winner[0]
    tab[:] = tab2[:]

def penta(tab, N):
    #pentagonal edit
    global c_tab
    tab2 = tab.copy()
    y = None
    for i in range(N):
        for j in range(N):
            n_tab = []
            opt = random.randint(1,4)
            if opt==1:
                n_tab.append(int(tab[i, (j - 1) % N]))
                n_tab.append(int(tab[(i - 1) % N, j]))
                n_tab.append(int(tab[(i + 1) % N, j]))
                n_tab.append(int(tab[(i - 1) % N, (j - 1) % N]))
                n_tab.append(int(tab[(i + 1) % N, (j - 1) % N]))
            elif opt==2:
                n_tab.append(int(tab[i, (j + 1) % N]))
                n_tab.append(int(tab[(i - 1) % N, j]))
                n_tab.append(int(tab[(i + 1) % N, j]))
                n_tab.append(int(tab[(i - 1) % N, (j + 1) % N]))
                n_tab.append(int(tab[(i + 1) % N, (j + 1) % N]))
            elif opt==3:
                n_tab.append(int(tab[i, (j - 1) % N]))
                n_tab.append(int(tab[i, (j + 1) % N]))
                n_tab.append(int(tab[(i - 1) % N, j]))
                n_tab.append(int(tab[(i - 1) % N, (j - 1) % N]))
                n_tab.append(int(tab[(i - 1) % N, (j + 1) % N]))
            elif opt==4:
                n_tab.append(int(tab[i, (j - 1) % N]))
                n_tab.append(int(tab[i, (j + 1) % N]))
                n_tab.append(int(tab[(i + 1) % N, j]))
                n_tab.append(int(tab[(i + 1) % N, (j - 1) % N]))
                n_tab.append(int(tab[(i + 1) % N, (j + 1) % N]))

            l = len(n_tab)
            k = 0
            while k in n_tab:
                n_tab.remove(k)

            if n_tab:
                if n_tab[0]!=0 and tab[i,j]==0:
                    winner = [word for word, word_count in Counter(n_tab).most_common(1)]
                    tab2[i,j] = winner[0]
    tab[:] = tab2[:]


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def growthRange(tab,N, radius):
    #w promieniu - środki ciężkości edit
    global sc_tab
    tab2 = tab.copy()
    rows, cols = len(tab), len(tab[0])
    for i in range(N):
        for j in range(N):
            n_tab =[]
            c = neighbors(tab, i, j, radius)
            if c!=0:
                for x in range(i - radius, i + radius + 1):
                    for y in range(j - radius, j + radius + 1):
                        if 0 <= x < rows and 0 <= y < cols:
                            if x!=y:
                                d = calculateDistance(x+sc_tab[x][y],y+sc_tab[x][y],i+sc_tab[i][j],j+sc_tab[i][j])
                                if d<radius:
                                    n_tab.append(int(tab[x][y]))

                                l = len(n_tab)
                                k = 0
                                while k in n_tab:
                                    n_tab.remove(k)

                                if n_tab:
                                    if n_tab[0] != 0 and tab[i, j] == 0:
                                        winner = [word for word, word_count in Counter(n_tab).most_common(1)]
                                        tab2[i, j] = winner[0]
    tab[:] = tab2[:]

def energy():
    global tab
    global e_tab
    global numel
    N = numel
    rows, cols = len(tab), len(tab[0])
    for i in permutation(N):
        for j in permutation(N):
            n_tab = []
            for x in range(i - 1, i + 2):
                for y in range(j - 1, j + 2):
                    if 0 <= x < rows and 0 <= y < cols and x!=y:
                         n_tab.append(int(tab[x,y]))
            n_tab2 = n_tab.copy()
            c = neighbors(tab, i, j, radius=1)
            if c<=0:
                return
            else:
                k = tab[i][j]
                while k in n_tab:
                    n_tab.remove(k)
                if len(n_tab)==0:
                    e_tab[i][j] = 0
                    continue

                eBefore = len(n_tab)

                newNum = random.choice(n_tab)
                #print(newNum)
                k = newNum

                while k in n_tab2:
                    n_tab2.remove(k)
                eAfter = len(n_tab2)

                deltaE = eAfter - eBefore;
                Kt = 0.6
                p = random.random();
                expo = math.exp(-((deltaE) / (Kt)));
                # print('xd')
                # print(eBefore)
                # print(eAfter)

                if (deltaE <= 0):
                    tab[i][j] = newNum
                    e_tab[i][j] = eAfter
                elif p < expo:
                    tab[i][j] = newNum
                    e_tab[i][j] = eAfter
                else:
                    e_tab[i][j] = eBefore
    prints(tab,numel)

def ppt():
    global tab
    global numel
    N = numel
    can.delete(ALL)
    for i in range(N):
        for j in range(N):
            OneSquare(can, scale * j, scale * i, scale * j + scale, scale * i + scale, "white", i, j, tab)
    prints(tab,numel)

#niestabilny fragment
r = lambda: random.randint(0,255)
tab = np.array([])
sc_tab = np.array([])
e_tab = np.array([])
t = None
numel = 0
scale = 10
cnt = 0

mGui = Tk()
mGui.geometry('600x765+500+25')
mGui.title('Grains growth')
mGui.resizable(True,True)

my_var = IntVar()
size = StringVar()


WIDTH, HEIGHT = 600, 600

paused = True

neigh = None

# rb1 = Radiobutton(mGui, text='Homogenous', variable=my_var, value=30)
# rb2 = Radiobutton(mGui, text='In range', variable=my_var, value=60)
# rb3 = Radiobutton(mGui, text='Manual choose', variable=my_var, value=90)
# rb4 = Radiobutton(mGui, text='Random', variable=my_var, value=225)

OPTIONS = [
"Homogenous",
"In range",
"Manual choose",
"Random"
]

lab_nuc = Label(text='\nGrain nucleation:\n').grid(row=0, sticky='W', padx=(3,0))

my_var = StringVar(mGui)
my_var.set(OPTIONS[0])

dl1 = OptionMenu(mGui,my_var,*OPTIONS).grid(row=1, sticky='W', padx=(3,0))

but = Button(mGui,text='Show',command=selected)
but1 = Button(mGui,text='Start',command=pause)
but2 = Button(mGui,text='Energy',command=energy)
but3 = Button(mGui,text='Print Energy',command=print_energy)
but4 = Button(mGui,text='Print Normal',command=ppt)

but.grid(row=1, sticky='E')
but1.grid(row=2, sticky='E')
but2.grid(row=3, sticky='E')
but3.grid(row=4, sticky='E')
but4.grid(row=5, sticky='E')


OPTIONS2 = [
"Moore",
"Neumann",
"Pentagonal",
"Hexagonal",
"In radius"
]

lab_neig = Label(text='\nNeighborhood:\n').grid(row=2, sticky='W', padx=(3,0))

my_var2 = StringVar(mGui)
my_var2.set(OPTIONS2[0])

dl2 = OptionMenu(mGui,my_var2,*OPTIONS2).grid(row=3, sticky='W', padx=(3,0))

isRand = BooleanVar(mGui)
isRand.set(False)
rb1 = Checkbutton(mGui, text='Random', variable=isRand)
rb1.grid(row=4, sticky='W', padx=(3,0))

entry2 = Entry(mGui) #size

side = IntVar(mGui)

rb2 = Radiobutton(mGui, text='Left', variable=side, value="1")
rb2.grid(row=5, sticky='W', padx=(10,0))
rb2.select()
rb3 = Radiobutton(mGui, text='Right', variable=side, value="2")
rb3.grid(row=6, sticky='W', padx=(10,0))

lab2 = Label(text='Size:').grid(row=6, column=0, sticky='N')
entry2.insert(END, '50')
entry2.grid(row=7, column=0, sticky='N')


entry_i = Entry(mGui)
entry_j = Entry(mGui)
entry_rnd = Entry(mGui)
entry_r = Entry(mGui)

entry_i.insert(END, '5')
entry_j.insert(END, '5')
entry_rnd.insert(END, '10')
entry_r.insert(END, '5')


lab_r = Label(text='Radius:').grid(row=0, column=0, sticky='N')
entry_r.grid(row=0, column=0, sticky='S')

lab_i = Label(text='Rows:').grid(row=1, column=0, sticky='N')
entry_i.grid(row=2, column=0, sticky='N')

lab_j = Label(text='Cols:').grid(row=2, column=0, sticky='S')
entry_j.grid(row=3, column=0, sticky='N')

lab_j = Label(text='Amount:').grid(row=4, column=0, sticky='N')
entry_rnd.grid(row=5, column=0, sticky='N')


can = Canvas(mGui, width=WIDTH, height=HEIGHT, bg="#ffffff")
can.grid(row=8, column=0)


mGui.mainloop()