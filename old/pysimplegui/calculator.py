import PySimpleGUI as psg
import random

def create_main_window(theme):
	psg.theme(theme)
	psg.set_options(font = 'Calibri 14', button_element_size = (6,3)) 
	num_button_size = (6,3)

	layout = [
		[psg.Push(), psg.Text('', font = 'Franklin 22', pad = (10, 20), right_click_menu = theme_menu, key = '-TEXT-')],
		[psg.Button('Clear', expand_x = True), psg.Button('Enter', expand_x = True)], 
		[psg.Button(7, size = num_button_size), psg.Button(8, size = num_button_size), psg.Button(9, size = num_button_size), psg.Button('*', size = num_button_size)],
		[psg.Button(4, size = num_button_size), psg.Button(5, size = num_button_size), psg.Button(6, size = num_button_size), psg.Button('/', size = num_button_size)],
		[psg.Button(1, size = num_button_size), psg.Button(2, size = num_button_size), psg.Button(3, size = num_button_size), psg.Button('-', size = num_button_size)],
		[psg.Button(0, expand_x = True), psg.Button('.', size = num_button_size), psg.Button('+', size = num_button_size)],
	]

	return psg.Window('Calculator', layout)

themes = ['BlueMono', 'BrightColors', 'LightTeal', 'TanBlue', 'DarkBlack1', 'DarkRed2']
theme_selector = random.choice(themes)

theme_menu = ['theme menu', themes]
win = create_main_window(theme_selector)

curr_num_tracker = []
smooth_operations = []

while True:
	event, values = win.read()
	if event == psg.WIN_CLOSED:
		break

	if event in theme_menu[1]:
		win.close()
		win = create_main_window(event)

	if event in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
		curr_num_tracker.append(event)
		num_string = ''.join(curr_num_tracker)
		win['-TEXT-'].update(num_string)

	if event in ['+', '-', '/', '*']:
		smooth_operations.append(''.join(curr_num_tracker))
		curr_num_tracker = []
		smooth_operations.append(event)
		win['-TEXT-'].update('')

	if event == 'Enter':
		smooth_operations.append(''.join(curr_num_tracker))
		result = eval(' '.join(smooth_operations))
		win['-TEXT-'].update(result)
		smooth_operations = []

	if event == 'Clear':
		curr_num_tracker = []
		smooth_operations = []
		win['-TEXT-'].update('')

win.close()



