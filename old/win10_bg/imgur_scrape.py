import requests, os, shutil

client_id ='e72932ddbed6183'
save_directory = 'imgur_scrape\\'

def scrape_album(album_id):
	directory = save_directory+album_id+'\\'
	album_items = []
	images = []
	album_link = 'https://api.imgur.com/3/album/' + album_id
	header = {'Authorization': 'Client-Id ' +client_id}
	imgur_album = requests.get(album_link, headers=header).json()

	if not imgur_album['success']:
		raise Exception(imgur_album['data']['error'])

	for img in imgur_album['data']['images']:
		images.append(img['link'])

	if not os.path.exists(directory):
		os.makedirs(directory)

	for _ in images:
		dl = requests.get(_, stream=True)
		i_path = directory+_[_.find('com/')+4:]

		#dl if does not exist only
		if not os.path.isfile(i_path):
			print(f'Downloaded {i_path}')
			with open(i_path, 'wb') as oFile:
				shutil.copyfileobj(dl.raw, oFile)
			album_items.append(_)
	return album_items

if __name__ == '__main__':
	while True:
		link = input('Enter album link: ')
		if '/a/' in link:
			scrape_album(link[link.find('/a/')+3:])
		elif 'gallery' in link:
			scrape_album(link[link.find('/gallery')+9:])
		else:
			print('Invalid link')