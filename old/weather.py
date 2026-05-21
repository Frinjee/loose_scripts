import requests

API_KEY = '41e37c504e5c617ad37e51003aad84f4'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

zip_code = input('Enter a zip code: ')
request_url = f'{BASE_URL}?zip={zip_code}&appid={API_KEY}'
res = requests.get(request_url)

if res.status_code == 200:
	data = res.json()
	weather = data['weather'][0]['description']


	_low = round(data['main']['temp_min'] - 273.15, 0)
	_high = round(data['main']['temp_max'] - 273.15, 0)
	
	
	temp_cels = round(data['main']['temp'] - 273.15, 2)
	temp_feel = round(data['main']['feels_like'] - 273.15, 0)
	humidity = data['main']['humidity']
	
	wind_speed = data['wind']['speed']
	
	city_name = data['name']
	country = data['sys']['country']

	print(f'{city_name}, {country} \nCurrent Temperature: {temp_cels}°c - Feels like: {temp_feel}°c \nLow of: {_low}°c & High of: {_high}°c')
	print(f'Humidity - {humidity} \nWind speeds of {wind_speed}')

else:
	print('An error occurred')


