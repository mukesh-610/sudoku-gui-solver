from Tkinter import *
import sudoku_solver

root=Tk()
root['bg']='black'
root.title('Sudoku Solver')
boxrowframes=[None]*3
rowframes=[None]*9
cellframes=[[None]*9]*9
cellvalues=[[]]*9

def cast_to_list_of_lists(cellvalues):
	ret=[[]]*9
	for i in range(9):
		ret[i]=[cellvalues[i][j].get() for j in range(9)]
	return ret

def set_IntVals(list_of_lists,IntVal_list):
	for i in range(9):
		for j in range(9):
			IntVal_list[i][j].set(list_of_lists[i][j])

def set_sudoku_from_file(fw,f):
	filedesc=open(f,'r')
	contents=filedesc.read()
	set_IntVals([i.split() for i in contents.replace('\n\n','\n').split('\n')],cellvalues)
	fw.destroy()

def read_from_file():
	filename=StringVar()
	file_window = Toplevel(root,bg='black')
	namebox_frame = Frame(file_window,bg='black')
	prompt_text = Label(namebox_frame,text='Enter the full path of the input file:',bg='black',fg='green')
	prompt_text.pack()
	namebox = Entry(namebox_frame,textvariable=filename,width=46)
	namebox.pack()
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
	
def gui_setup():
	Frame(root,height=2,bg='black').pack()
	descriptionframe=Frame(root,bg='black')
	desctext='Welcome to Sudoku Solver!\nEnter an unsolved sudoku (0 for blank places) here,\nor \
select an input file to read from, and then press Solve!'
	Label(descriptionframe,bg='black',fg='green',text=desctext).pack(side=LEFT)
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
		for j in range(9):
			cellframes[i][j]=Frame(rowframes[i],height=20,width=20,relief=SUNKEN,borderwidth=2,bg='black')
			Entry(cellframes[i][j],textvariable=cellvalues[i][j],width=3).pack()
			cellframes[i][j].pack(side=LEFT)
			if j in (2,5):
				Frame(rowframes[i],width=4,height=20,bg='black').pack(side=LEFT)
		
	controlsframe=Frame(root,pady=10,width=180,padx=10,bg='black')
	
	Button(controlsframe,text='Quit',command=root.destroy,bg='red',fg='black').pack(side=RIGHT)
	Frame(controlsframe,width=20,bg='black').pack(side=RIGHT)
	Button(controlsframe,text='Read from file',command=read_from_file,bg='yellow',fg='black').pack(side=RIGHT)
	Frame(controlsframe,width=20,bg='black').pack(side=RIGHT)
	Button(controlsframe,text='Solve!',bg='green',fg='black',command=solve).pack(side=RIGHT)
	Frame(controlsframe,width=20,bg='black').pack(side=RIGHT)
	controlsframe.pack()

gui_setup()
root.mainloop()