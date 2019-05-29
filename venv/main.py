from tkinter import *
import numpy as np
import time
import threading
import random
from collections import Counter
from numpy.random import permutation

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
    tab = np.zeros(numel * numel).reshape(numel, numel)
    return tab

def pause():
    global paused
    if not paused:
        paused = True
    else:
        paused = False
        show(tab, numel)

def show(tab, numel):
    global paused
    if not paused:
        moore(tab,numel)
        prints(tab,numel)
        threading.Timer(3.0, show,(tab,numel)).start()


def prints(tab, numel):
    can.delete(ALL)
    global c_tab
    for i in range(0, numel):
        for j in range(0, numel):
            OneSquare(can, scale * j, scale * i, scale * j + scale, scale * i + scale, c_tab[int(tab[i][j])], i, j, tab)



def selected():
    global tab
    global numel

    numel = int(entry2.get())

    tab = create(numel)
    prints(tab, numel)

    opt = my_var.get()

    rad = int(entry_r.get())
    rows = int(entry_i.get())
    cols = int(entry_j.get())
    amount = int(entry_rnd.get())
    
    if opt == 30:
        homo(tab, rows, cols)
    elif opt == 60:
        in_range(tab, rad)
    elif opt == 90:
        man(tab, numel)
    elif opt == 225:
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

def neumann():
    pass

def hexa():
    pass

def penta():
    pass

#niestabilny fragment
r = lambda: random.randint(0,255)
tab = np.array([])
t = None
numel = 0
scale = 15
cnt = 0

mGui = Tk()
mGui.geometry('600x745+500+30')
mGui.title('Grains growth')
mGui.resizable(False,False)

my_var = IntVar()
size = StringVar()
WIDTH, HEIGHT = 600, 600

paused = True

rb1 = Radiobutton(mGui, text='Homogenous', variable=my_var, value=30)
rb2 = Radiobutton(mGui, text='In range', variable=my_var, value=60)
rb3 = Radiobutton(mGui, text='Manual choose', variable=my_var, value=90)
rb4 = Radiobutton(mGui, text='Random', variable=my_var, value=225)

but = Button(mGui,text='Show',command=selected)
but1 = Button(mGui,text='Start',command=pause)
but.grid(row=4, sticky='S')
but1.grid(row=7, column=0, sticky='S')

lab_empty = Label(text='\nChoose the rule:\n').grid(row=0, sticky='W', padx=(5,0))

rb1.grid(row=1, sticky='W', padx=(10,0))
rb2.grid(row=2, sticky='W', padx=(10,0))
rb3.grid(row=3, sticky='W', padx=(10,0))
rb4.grid(row=4, sticky='W', padx=(10,0))

lab2 = Label(text='Size:').grid(row=6, column=0, sticky='W')

entry2 = Entry(mGui) #size


entry2.insert(END, '30')

entry2.grid(row=7, column=0, sticky='W')


entry_i = Entry(mGui)
entry_j = Entry(mGui)
entry_rnd = Entry(mGui)
entry_r = Entry(mGui)

entry_i.insert(END, '5')
entry_j.insert(END, '5')
entry_rnd.insert(END, '20')
entry_r.insert(END, '5')


lab_r = Label(text='Radius:').grid(row=1, sticky='E')
entry_r.grid(row=2, column=0, sticky='E')

lab_i = Label(text='Rows:').grid(row=3, sticky='E')
entry_i.grid(row=4, sticky='E')

lab_j = Label(text='Cols:').grid(row=5, sticky='E')
entry_j.grid(row=6, column=0, sticky='E')

lab_j = Label(text='Amount:').grid(row=7, sticky='E')
entry_rnd.grid(row=8, column=0, sticky='E')


can = Canvas(mGui, width=WIDTH, height=HEIGHT, bg="#ffffff")
can.grid(row=9, column=0)


mGui.mainloop()
