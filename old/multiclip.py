import sys, clipboard, json

S_DATA = 'clipboard.json'

def save_json(file_path, data):
	with open(file_path, 'w') as f:
		json.dump(data, f)

def load_jsonFile_andReturn(file_path):
	try: # attempt to load file
		with open(file_path, 'r') as f:
			data = json.load(f)	
			return data
	except: # if file doesn't exist return empty dict
		return {}

def return_options():
	options = ['--save', '--load', '--list', '--help']	
	print('Commands available:', options)

# accept only 1 command, e.g. python multiclip.py [save, load, list]
if len(sys.argv) == 2:
	cmd = sys.argv[1] # accept 2nd argument for command
	data = load_jsonFile_andReturn(S_DATA)

	if cmd == '--save':
		key = input('Enter a key: ') # ask for key

		data[key] = clipboard.paste() # save whatever was on kb
		save_json(S_DATA, data) # save data to file
		print('Data Saved')
	elif cmd == '-load':
		key = input('Enter key to search for')

		if key in data: # check if key is in stored data
			clipboard.copy(data[key]) # if it is copy the value of the key 
			print('Data Copied to clipboard') 
		else: # if key does not exist print so
			print('Key does not exist')
	elif cmd == '--list':
		print(data)

	elif cmd == '--help':
		return_options()

	else:
		print('{cmd} is not a valid command, use --help for available commands')
else:
	print('multiple arguments are not supported')