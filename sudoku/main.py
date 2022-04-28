import tkinter
from tkinter import *
import random
#sudoku tela
guess = str()
grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

root = Tk()
root.title("Sudoku")
root.minsize(width=500, height=715)
root.attributes("-alpha", 0.90)
root.configure(background="#282828")

title = Label(root, text='Sudoku', fg="#382888", font="Geneva 30", bg="#282828")
title.pack()

box = Canvas(root, width=435, height=435, background="#282828", bd=6, highlightthickness=6)
box.pack()

entry_list = [[], [], []]
var = []
done = False


def one_grid(row):
    global grid, entry_list
    g1 = Entry(row, textvariable=var, width=2, fg="white", font="Geneva 30 bold", bg="#373737", justify=CENTER)
    entry_list[0].append(g1)
    g1.place(x=5, y=5)
    g2 = Entry(row, textvariable=var, width=2, fg="white", font="Geneva 30 bold", bg="#373737", justify=CENTER)
    entry_list[0].append(g2)
    g2.place(x=52, y=5)
    g3 = Entry(row, textvariable=var, width=2, fg="white", font="Geneva 30 bold", bg="#373737", justify=CENTER)
    g3.place(x=102, y=5)
    entry_list[0].append(g3)
    g4 = Entry(row, textvariable=var, width=2, fg="white", font="Geneva 30 bold", bg="#373737", justify=CENTER)
    g4.place(x=5, y=52)
    entry_list[1].append(g4)
    g5 = Entry(row, textvariable=var, width=2, fg="white", font="Geneva 30 bold", bg="#373737", justify=CENTER)
    g5.place(x=52, y=52)
    entry_list[1].append(g5)
    g6 = Entry(row, textvariable=var, width=2, fg="white", font="Geneva 30 bold", bg="#373737", justify=CENTER)
    g6.place(x=102, y=52)
    entry_list[1].append(g6)
    g7 = Entry(row, textvariable=var, width=2, fg="white", font="Geneva 30 bold", bg="#373737", justify=CENTER)
    g7.place(x=5, y=102)
    entry_list[2].append(g7)
    g8 = Entry(row, textvariable=var, width=2, fg="white", font="Geneva 30 bold", bg="#373737", justify=CENTER)
    g8.place(x=52, y=102)
    entry_list[2].append(g8)
    g9 = Entry(row, textvariable=var, width=2, fg="white", font="Geneva 30 bold", bg="#373737", justify=CENTER)
    g9.place(x=102, y=102)
    entry_list[2].append(g9)


def display_val():
    global entry_list
    u = 0
    for a in entry_list:
        a_splited = [a[x:x + 9] for x in range(0, len(a), 9)]
        for y in range(9):
            if (grid[u][y] != 0):
                a_splited[0][y].insert(0, grid[u][y])
        u += 1
    u = 3
    for a in entry_list:
        a_splited = [a[x:x + 9] for x in range(0, len(a), 9)]
        for y in range(9):
            if (grid[u][y] != 0):
                a_splited[1][y].insert(0, grid[u][y])
        u += 1

    u = 6
    for a in entry_list:
        a_splited = [a[x:x + 9] for x in range(0, len(a), 9)]
        for y in range(9):
            if (grid[u][y] != 0):
                a_splited[2][y].insert(0, grid[u][y])
        u += 1


def clear():
    global grid
    grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]


def scramble():
    global grid
    clear()
    for a in entry_list:
        for b in a:
            b.delete(first=0, last=100)
    amount = 20

    for i in range(amount):
        y = random.randint(0, len(grid) - 1)
        x = random.randint(0, len(grid) - 1)
        num = random.randint(1, len(grid))
        allow = 0
        for e in range(len(grid)):
            if num not in grid[x] and num != grid[e][y]:
                allow += 1
        grid[x][y] = num
        tempo = grid
        tempo = rearrange(tempo)

        for e in range(len(grid)):
            if (duplicate_checker(tempo[e])):
                allow = 0
        if allow != len(grid):
            grid[x][y] = 0

    display_val()


def stay(num, x, y):
    for e in range(9):
        if grid[y][e] == num:
            return False
    for e in range(9):
        if grid[e][x] == num:
            return False

    for i in range(3):
        for e in range(3):
            if grid[((y // 3) * 3) + i][((x // 3) * 3) + e] == num:
                return False
    return True


def pressed_solve():
    global grid, done
    done = False
    solver()


def solver():
    global grid, done

    if (done == False):

        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    for num in range(1, 10):
                        if stay(num, x, y):
                            grid[y][x] = num
                            solver()
                            grid[y][x] = 0
                    return
        done = True
        for a in entry_list:
            for b in a:
                b.delete(first=0, last=100)
        display_val()

        return


def rearrange(a):
    temp = [[], [], [], [], [], [], [], [], []]
    count = 0
    ch = 0
    for e in range(len(a)):
        for x in range(3):
            if (a[e][x] != 0):
                temp[ch].append(a[e][x])
        count += 1
        if (count == 3):
            ch += 1
            count = 0
    for e in range(len(a)):
        for x in range(3, 6):
            if (a[e][x] != 0):
                temp[ch].append(a[e][x])
        count += 1
        if (count == 3):
            ch += 1
            count = 0
    for e in range(len(a)):
        for x in range(6, 9):
            if (a[e][x] != 0):
                temp[ch].append(a[e][x])
        count += 1
        if (count == 3):
            ch += 1
            count = 0
    return temp


def duplicate_checker(a):
    b = set(a)
    result = len(a) != len(b)
    # print(result)
    if (result == True):
        return True


def checkrow_horz(a):
    for x in a:
        if (duplicate_checker(x) == True):
            return True


def checkrow_vert(a):
    for y in range(len(a)):
        temp = []
        for x in a:
            temp.append(x[y])
        if (duplicate_checker(temp) == True):
            return True


def checkcol(a):
    for y in range(3):
        temp = []
        for x in range(int(len(a) / 3)):
            temp.append(a[x][3 * y])
            temp.append(a[x][3 * y + 1])
            temp.append(a[x][3 * y + 2])
        if (duplicate_checker(temp) == True):
            return True
        temp = []
        for x in range(3, (int(len(a) / 3)) * 2):
            temp.append(a[x][3 * y])
            temp.append(a[x][3 * y + 1])
            temp.append(a[x][3 * y + 2])
        if (duplicate_checker(temp) == True):
            return True
        temp = []
        for x in range(6, (int(len(a) / 3)) * 3):
            temp.append(a[x][3 * y])
            temp.append(a[x][3 * y + 1])
            temp.append(a[x][3 * y + 2])
        if (duplicate_checker(temp) == True):
            return True


def submit():
    global entry_list

    temp = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    u = 0
    for a in entry_list:
        a_splited = [a[x:x + 9] for x in range(0, len(a), 9)]
        for y in range(9):
            if (a_splited[0][y].get() != ''):
                temp[u][y] = int(a_splited[0][y].get())
        u += 1
    u = 3
    for a in entry_list:
        a_splited = [a[x:x + 9] for x in range(0, len(a), 9)]
        for y in range(9):
            if (a_splited[1][y].get() != ''):
                temp[u][y] = int(a_splited[1][y].get())
        u += 1

    u = 6
    for a in entry_list:
        a_splited = [a[x:x + 9] for x in range(0, len(a), 9)]
        for y in range(9):
            if (a_splited[2][y].get() != ''):
                temp[u][y] = int(a_splited[2][y].get())
        u += 1

    if (checkrow_horz(temp) == True or checkrow_vert(temp) == True or checkcol(temp) == True):
        wrong()
    else:
        correct()


def wrong():
    title.config(fg="#990000", text="Tente novamente")
    row1.config(highlightbackground="#990000")
    row2.config(highlightbackground="#990000")
    row3.config(highlightbackground="#990000")
    row4.config(highlightbackground="#990000")
    row5.config(highlightbackground="#990000")
    row6.config(highlightbackground="#990000")
    row7.config(highlightbackground="#990000")
    row8.config(highlightbackground="#990000")
    row9.config(highlightbackground="#990000")
    row1.after(2100, lambda: row1.config(highlightbackground="white"))
    row2.after(2100, lambda: row2.config(highlightbackground="white"))
    row3.after(2100, lambda: row3.config(highlightbackground="white"))
    row4.after(2100, lambda: row4.config(highlightbackground="white"))
    row5.after(2100, lambda: row5.config(highlightbackground="white"))
    row6.after(2100, lambda: row6.config(highlightbackground="white"))
    row7.after(2100, lambda: row7.config(highlightbackground="white"))
    row8.after(2100, lambda: row8.config(highlightbackground="white"))
    row9.after(2100, lambda: row9.config(highlightbackground="white"))
    title.after(2100, lambda: title.config(fg="#382888", text="Sudoku"))


def correct():
    title.config(fg="#288888", text="Correto")
    row1.config(highlightbackground="#288888")
    row2.config(highlightbackground="#288888")
    row3.config(highlightbackground="#288888")
    row4.config(highlightbackground="#288888")
    row5.config(highlightbackground="#288888")
    row6.config(highlightbackground="#288888")
    row7.config(highlightbackground="#288888")
    row8.config(highlightbackground="#288888")
    row9.config(highlightbackground="#288888")
    row1.after(2100, lambda: row1.config(highlightbackground="white"))
    row2.after(2100, lambda: row2.config(highlightbackground="white"))
    row3.after(2100, lambda: row3.config(highlightbackground="white"))
    row4.after(2100, lambda: row4.config(highlightbackground="white"))
    row5.after(2100, lambda: row5.config(highlightbackground="white"))
    row6.after(2100, lambda: row6.config(highlightbackground="white"))
    row7.after(2100, lambda: row7.config(highlightbackground="white"))
    row8.after(2100, lambda: row8.config(highlightbackground="white"))
    row9.after(2100, lambda: row9.config(highlightbackground="white"))
    title.after(2100, lambda: title.config(fg="#382888", text="Sudoku"))


row1 = Canvas(box, width=120, height=120, background="#282828", bd=10, highlightthickness=10)
one_grid(row1)
row1.place(x=0, y=0)
row2 = Canvas(box, width=120, height=120, background="#282828", bd=10, highlightthickness=10)
one_grid(row2)
row2.place(x=150, y=0)
row3 = Canvas(box, width=120, height=120, background="#282828", bd=10, highlightthickness=10)
one_grid(row3)
row3.place(x=300, y=0)

row4 = Canvas(box, width=120, height=120, background="#282828", bd=10, highlightthickness=10)
one_grid(row4)
row4.place(x=0, y=150)
row5 = Canvas(box, width=120, height=120, background="#282828", bd=10, highlightthickness=10)
one_grid(row5)
row5.place(x=150, y=150)
row6 = Canvas(box, width=120, height=120, background="#282828", bd=10, highlightthickness=10)
one_grid(row6)
row6.place(x=300, y=150)

row7 = Canvas(box, width=120, height=120, background="#282828", bd=10, highlightthickness=10)
one_grid(row7)
row7.place(x=0, y=300)
row8 = Canvas(box, width=120, height=120, background="#282828", bd=10, highlightthickness=10)
one_grid(row8)
row8.place(x=150, y=300)
row9 = Canvas(box, width=120, height=120, background="#282828", bd=10, highlightthickness=10)
one_grid(row9)
row9.place(x=300, y=300)

scramble()

but = Canvas(root, width=500, height=45, background="#282828", bd=13, highlightthickness=0)
but.pack()
# enter = Button(but, text="Entrar", fg="#282828", command=submit, font="Geneva 30 bold", bg='#282828',
#                activebackground='#282828', highlightbackground="#288888", disabledforeground="#288888", justify=CENTER)
# enter.configure(bg='#282828', width=12)
# enter.place(x=200, y=10)
reset = Button(but, text="Redefinir", fg="#282828", command=scramble, font="Geneva 30 bold", bg='#382888',
               activebackground='#382888', highlightbackground="#382888", disabledforeground="#382888", justify=CENTER)
reset.configure(bg='#382888', width=12)
reset.place(x=120, y=10)
solve = Button(root, text="Resolver", fg="#282828", command=pressed_solve, font="Geneva 30 bold", bg='#FCD4D4',
               activebackground='#FCD4D4', highlightbackground="#FCD4D4", disabledforeground="#FCD4D4", justify=CENTER)
solve.configure(bg='#FCD4D4', width=12)
solve.place(x=120, y=585)

root.mainloop()
