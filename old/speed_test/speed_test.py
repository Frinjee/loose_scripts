import speedtest

stest = speedtest.Speedtest(secure=True)

dl = stest.download()
up = stest.upload()

# mbps conversion
dl = dl/1000000
up = up/1000000

print('Download is: ', round(dl, 3), 'Mbps')
print('Upload is: ', round(up, 3), 'Mbps')

stest.get_servers([])
ping = stest.results.ping

print('Ping is: ', round(ping))