# 1st calculator
from tkinter import *

# global expression variable
exp = ''

def onClick_num(x):
	global exp

	exp = exp + str(x)
	equation.set(exp)

def onClick_equal():

	try:
		global exp

		_sum = str(eval(exp))
		equation.set(_sum)

		exp = ''

	except:
		equation.set('ERROR!')
		exp = ''

def onClick_clear():
	global exp
	exp = ''
	equation.set('')


if __name__ == '__main__':
	root = Tk()

	root.configure(background='grey96')
	root.title('Py Calc - Jen')
	root.geometry('225x155')

	equation = StringVar()
	exp_field = Entry(root, textvariable=equation)
	exp_field.grid(columnspan=4, pady=2)

	# NUM BUTTONS
	button1 = Button(root, text=' 1 ', fg='black', bg='lightcyan2', command=lambda: onClick_num(1), height=1, width=5)
	button1.grid(row=2, column=0)
	button2 = Button(root, text=' 2 ', fg='black', bg='lightcyan2', command=lambda: onClick_num(2), height=1, width=5)
	button2.grid(row=2, column=1)
	button3 = Button(root, text=' 3 ', fg='black', bg='lightcyan2', command=lambda: onClick_num(3), height=1, width=5)
	button3.grid(row=2, column=2)
	button4 = Button(root, text=' 4 ', fg='black', bg='lightcyan2', command=lambda: onClick_num(4), height=1, width=5)
	button4.grid(row=3, column=0)
	 
	button5 = Button(root, text=' 5 ', fg='black', bg='lightcyan2', command=lambda: onClick_num(5), height=1, width=5)
	button5.grid(row=3, column=1)
	button6 = Button(root, text=' 6 ', fg='black', bg='lightcyan2', command=lambda: onClick_num(6), height=1, width=5)
	button6.grid(row=3, column=2)
	button7 = Button(root, text=' 7 ', fg='black', bg='lightcyan2', command=lambda: onClick_num(7), height=1, width=5)
	button7.grid(row=4, column=0)
	button8 = Button(root, text=' 8 ', fg='black', bg='lightcyan2',command=lambda: onClick_num(8), height=1, width=5)
	button8.grid(row=4, column=1)
	button9 = Button(root, text=' 9 ', fg='black', bg='lightcyan2', command=lambda: onClick_num(9), height=1, width=5)
	button9.grid(row=4, column=2)
	button0 = Button(root, text=' 0 ', fg='black', bg='lightcyan2', command=lambda: onClick_num(0), height=1, width=5)
	button0.grid(row=5, column=0)
	# OPERATION BUTTONS
	plus = Button(root, text=' + ', fg='black', bg='lightcyan2', command=lambda: onClick_num("+"), height=1, width=5)
	plus.grid(row=2, column=3)
	 
	minus = Button(root, text=' - ', fg='black', bg='lightcyan2', command=lambda: onClick_num("-"), height=1, width=5)
	minus.grid(row=3, column=3)
	 
	multiply = Button(root, text=' * ', fg='black', bg='lightcyan2', command=lambda: onClick_num("*"), height=1, width=5)
	multiply.grid(row=4, column=3)
	 
	divide = Button(root, text=' / ', fg='black', bg='lightcyan2', command=lambda: onClick_num("/"), height=1, width=5)
	divide.grid(row=5, column=3)

	clear = Button(root, text='Clear', fg='black', bg='lightcyan2', command=onClick_clear, height=1, width=5)
	clear.grid(row=5, column=2)
	 
	Decimal= Button(root, text='.', fg='black', bg='lightcyan2', command=lambda: onClick_num('.'), height=1, width=5)
	Decimal.grid(row=5, column=1)


	equal = Button(root, text=' = ', fg='black', bg='lightcyan2', command=onClick_equal, height=1, width=5)
	equal.grid(row=6, column=0)
	# start the GUI
	root.mainloop()
