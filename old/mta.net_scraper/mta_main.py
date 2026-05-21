# URL to scrape https://www.malware-traffic-analysis.net/training-exercises.html

## TODO ##
# 1. Get post dates and titles of exercises
# 2. Sort exercises by year
# 3. Select exercises by year
# 4. Select exercise by title in year section
# 5. Display brief desc + task, notes, page url, and download link for pcap + password for zip
# 6. Download pcap into selectable os folder
# 7. Ask user if they want to select another or exit
import re, requests, zipfile, io
import datetime as dt
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup

url = 'https://www.malware-traffic-analysis.net/training-exercises.html'

# open a connection and grab the webpage, offload content into page dump, close the client
mta_client = ureq(url)
mta_page_dump = mta_client.read()
mta_client.close()

# html parsing
mta_soup = soup(mta_page_dump, 'html.parser')
link_content, link_info, hosted_urls, isc_urls, dates, titles = ([] for _ in range(6))

# url extraction. 
for _ in mta_soup.find_all('a', href=True):
	if _.text:
		link_content.append(_['href'])
		link_info.append(_.text)

# separate links hosted on site and links hosted on isc
link_pattern = re.compile(r'[a-zA-Z]+://([a-zA-Z]+(\.[a-zA-Z]+)+)', re.IGNORECASE)
for _ in link_content:
	if re.match(link_pattern, _): isc_urls.append(_)
	else: 
		x = 'https://www.malware-traffic-analysis.net/' + _
		hosted_urls.append(x)

# data and title extraction
date_pattern = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', re.IGNORECASE)
for _ in link_info:
	if re.match(date_pattern, _): dates.append(_)
	else: titles.append(_)

# extract years only from dates list
read_years = {}
years = [dt.datetime.strptime(_, '%Y-%m-%d').year for _ in dates]
years = list(set(years))
years.sort(reverse=True)

hosted_urls = list(set(hosted_urls))
hosted_urls.sort(reverse=True)

def link_dict_converter(x):
	iterable = iter(x)
	returned_dict = dict(zip(iterable, iterable))
	return returned_dict

# convert our link_info to dictionary
link_dict = link_dict_converter(link_info)
hosted_dict = link_dict_converter(hosted_urls)
link_dict.pop('Return to main menu')


menu_link = {}
descriptor_link = {}

counter = 1
for k in link_dict.items():
	_str = str(counter)
	menu_link[_str] = k
	counter += 1

def get_desc(url):
	page_url = url
	mta_client = ureq(page_url)
	mta_pg_dump = mta_client.read()
	mta_client.close()
	mta_soup = soup(mta_pg_dump, 'html.parser')
	for _ in mta_soup.find_all('li'):
				if _.text:
					print(_.get_text())

def download_pcap(url):
	page_url = url
	mta_client = ureq(page_url)
	mta_pg_dump = mta_client.read()
	mta_client.close()
	mta_soup = soup(mta_pg_dump, 'html.parser')
	for _ in mta_soup.find_all('a', {'class': 'menu_link'}):
				if _.text:
					zip_pattern = re.compile(r"([A-Za-z0-9]+(-[A-Za-z0-9]+)+).*\.[a-zA-Z]+", re.IGNORECASE)
					_s = _.get_text()
					if re.match(zip_pattern, _s): 
						print('Saving File As: ' + _s)
						_s = url +'/'+ _s
						res = requests.get(_s, stream = True)
						z_file = zipfile.ZipFile(io.BytesIO(res.content))
count = 0
for v in hosted_urls:
	_c = str(count)
	descriptor_link[_c] = v
	count += 1

descriptor_link.pop('0')

def main_menu():
	for k,v in menu_link.items():
		print(k, v)
	
	selection = input('SELECT AN ITEM: ')
	print(f'Selected: {menu_link[selection]}')
	if selection in menu_link.keys():
		options = input('1. View Description, 2. Download, 3. Return to Main, 4. Exit\n')
		if options == '1':
			print('Description: ...')
			desc_url = descriptor_link.get(selection)
			get_desc(desc_url)
		if options == '2':
			print('Downloading ...')
			dl_url = descriptor_link.get(selection)
			download_pcap(dl_url)
		if options == '3':
			print('Returning to main menu ...')
			main_menu()
		if options == '4':
			print('Exiting ...')
			exit(0)
main_menu()


















'''for _ in mta_soup2.find_all('h2'):
	if _.text:
		print(_)

for _ in mta_soup2.find_all('li'):
	if _.text:
		print(_)'''




'''def descriptor():
	counter = 1
	for _ in hosted_urls:
		_c = str(counter)
		descriptor_link[_c] = _
		counter += 1
descriptor()
'''


'''for k,v in descriptor_link.items():
	print(k,v)'''

'''def main_menu():
	for k,v in menu_link.items():
		print(k, v)
	
	selection = input('SELECT AN ITEM: ')
	if selection in menu_link.keys():
		print(f'Selected: {menu_link[selection]}')
		options = input('1. View Description, 2. Download, 3. Return to Main, 4. Exit\n')
		if options == '1':
			print('Description: ...')
		if options == '2':
			print('Downloading ...')
		if options == '3':
			print('Returning to main menu ...')
			main_menu()
		if options == '4':
			sys.exit()
main_menu()'''


'''for k,v in link_dict.items():
	print(k)
	print(v)'''



# main_content >> content >> ul >> li
'''
main_content = mta_soup.findAll('div', {'class':'content'})
headers = mta_soup.findAll('a', {'class':'list_header'})
content = main_content[0]'''


'''def main_menu():
	counter = 1
	print('Select a year: ')
	for _ in years:
		print(counter, '-' , _)
		counter += 1

main_menu()'''

#menu_link = dict.fromkeys(range(len(link_dict)))