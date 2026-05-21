import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier

n = ToastNotifier()
coords = '39.328480,-76.709100'

def getdata(url):
	r = requests.get(url)
	return r.text
	
htmldata = getdata(f"https://weather.com/en-US/weather/today/l/{coords}?par=google&temp=c/")

soup = BeautifulSoup(htmldata, 'html.parser')

current_temp = soup.find_all("span", class_= "_-_-components-src-organism-CurrentConditions-CurrentConditions--tempValue--MHmYY")

chances_rain = soup.find_all("div", class_= "_-_-components-src-organism-CurrentConditions-CurrentConditions--precipValue--2aJSf")

temp = (str(current_temp))

temp_rain = str(chances_rain)

result = "current_temp " + temp[128:-9] + "\n" + temp_rain[131:-14]
n.show_toast("live Weather update",
			result, duration = 10)