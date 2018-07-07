try:
	from Tkinter import *
except ImportError:
	from tkinter import *
import sudoku_solver

root=Tk()
root['bg']='black'
root.title('Sudoku Solver')
boxrowframes=[None]*3
rowframes=[None]*9
cellframes=[[None]*9]*9
cellvalues=[[]]*9
focusedi=focusedj=0

def cast_to_list_of_lists(cellvalues):
	ret=[]
	for i in range(9):
		ret.append([])
		for j in range(9):
			try:
				ret[i].append(cellvalues[i][j].get())
			except:
				ret[i].append(0)
	return ret

def set_IntVals(list_of_lists,IntVal_list):
	for i in range(9):
		for j in range(9):
			IntVal_list[i][j].set(list_of_lists[i][j])

def set_sudoku_from_file(fw,f):
	filedesc=open(f,'r')
	contents=filedesc.read()
	set_IntVals([i.split() for i in contents.replace('\r','').replace('\n\n','\n').split('\n')],cellvalues)
	fw.destroy()

def read_from_file():
	filename=StringVar()
	filename.set('puzzfile.txt')
	file_window = Toplevel(root,bg='black')
	file_window.grab_set()
	namebox_frame = Frame(file_window,bg='black')
	prompt_text = Label(namebox_frame,text='Enter the full path of the input file:',bg='black',fg='green')
	prompt_text.pack()
	namebox = Entry(namebox_frame,textvariable=filename,width=46)
	namebox.pack()
	namebox.select_range(0,END)
	namebox.focus()
	namebox_frame.pack()
	warningframe = Frame(file_window,bg='yellow')
	warningtext = Label(warningframe,text='Please make sure that the input file is formatted like\n\
the sample file attached with this script!',fg='yellow',bg='black')
	warningtext.pack()
	warningframe.pack()
	controlsframe = Frame(file_window,bg='black')
	Button(controlsframe,text='Cancel',bg='red',fg='black',command=file_window.destroy).pack(side=RIGHT,padx=20)
	Button(controlsframe,text='Read',bg='green',fg='black',command=lambda:set_sudoku_from_file(file_window,filename.get())).pack(side=RIGHT,padx=20)
	controlsframe.pack()
	
def solve():
	sudoku=cast_to_list_of_lists(cellvalues)
	set_IntVals(sudoku_solver.solve(sudoku),cellvalues)

def focus():
	global focusedi,focusedj
	cellentries[focusedi][focusedj].select_range(0,END)
	cellentries[focusedi][focusedj].focus()
	
def changefocus(e):
	global focusedi, focusedj
	if focusedj == 8 and focusedi == 8:
		focus()
		return
	elif focusedj == 8:
		focusedi += 1
		focusedj = 0
	else:
		focusedj += 1
	focus()
	
def reset():
	global focusedi, focusedj
	focusedi = focusedj = 0
	for row in cellvalues:
		for cell in row:
			cell.set(0)
	focus()
	
def findbox(i,j):
	return (i//3)*3 + j//3 + 1

def focus_previous(e,x,y):
	cellvalues[x][y].set(0)
	global focusedi,focusedj
	if focusedi == 0 and focusedj == 0:
		pass
	elif focusedj == 0:
		focusedi -= 1
		focusedj = 8
	else:
		focusedj -= 1
	focus()
	return "break"

def update_focus_on_click(e,x,y):
	global focusedi,focusedj
	focusedi = x
	focusedj = y
	focus()

def gui_setup():
	global cellentries,cellvalues
	cellentries = []

	Frame(root,height=2,bg='black').pack()
	descriptionframe=Frame(root,bg='black')
	desctext='Welcome to Sudoku Solver!\nEnter an unsolved sudoku (0 for blank places) here,\nor \
select an input file to read from, and then press Solve!'
	Label(descriptionframe,bg='black',fg='green',text=desctext,font=("Arial",10)).pack(side=LEFT)
	descriptionframe.pack()

	for i in range(9):
		cellvalues[i]=[IntVar() for _ in range(9)]
	
	for i in range(3):
		boxrowframes[i]=Frame(root,height=60,pady=2,width=180,bg='black',padx=4)
		boxrowframes[i].pack()
	
	for i in range(9):
		rowframes[i]=Frame(boxrowframes[i//3],height=20,width=180,bg='black')
		rowframes[i].pack()
	

	for i in range(9):
		cellentries.append([None for _ in range(9)])
		for j in range(9):
			cellframes[i][j]=Frame(rowframes[i],height=20,width=20,relief=SUNKEN,borderwidth=2,bg='black')
			if findbox(i,j) in (2,4,6,8):
				cellentries[i][j]=Entry(cellframes[i][j],textvariable=cellvalues[i][j],width=3)
			else:
				cellentries[i][j]=Entry(cellframes[i][j],textvariable=cellvalues[i][j],width=3,bg='pale green')
			for x in range(10):
				cellentries[i][j].bind(str(x),changefocus)
			cellentries[i][j].bind('<FocusIn>',lambda e,x=i,y=j:update_focus_on_click(e,x,y))
			cellentries[i][j].bind('<BackSpace>',lambda e,x=i,y=j:focus_previous(e,x,y))
			cellentries[i][j].pack()
			cellframes[i][j].pack(side=LEFT)
			if j in (2,5):
				Frame(rowframes[i],width=4,height=20,bg='black').pack(side=LEFT)
	
	cellentries[0][0].select_range(0,END)
	cellentries[0][0].focus()
	
	controlsframe=Frame(root,pady=10,width=180,padx=10,bg='black')
	
	Button(controlsframe,text='Quit',command=root.destroy,bg='red',fg='black').pack(side=RIGHT,padx=5)
	Button(controlsframe,text='Reset cells',command=reset,bg='white',fg='black').pack(side=RIGHT,padx=5)
	Button(controlsframe,text='Read from file',command=read_from_file,bg='yellow',fg='black').pack(side=RIGHT,padx=5)
	Button(controlsframe,text='Solve!',bg='green',fg='black',command=solve).pack(side=RIGHT,padx=5)
	controlsframe.pack()

gui_setup()
root.mainloop()
