import time, random
from yaspin import yaspin, Spinner

res = ['Cannot predict now', 'Ask again later', 'Yes', 'No', 'Maybe',
'l o l', 'Not a chance']

def initialQuery():
	q = input('What would you like to know? ')
	spin = Spinner(['🔮 Gazing into my crystal ball', '🙈 Interesting, very interesting', 
		            '🙊 hmmmm I see.....'], 1000)

	with yaspin(spin, text=''):
		time.sleep(3)	

	print('🙉 ', random.choice(res))
initialQuery()

while True:
	_ = input('Ask another question? (y/n):')
	if _.lower().strip()[:1] == 'y': 
		initialQuery()	
	elif _.lower().strip()[:1] == 'n':
		break
	else:
		print('Invalid response, try again')
		