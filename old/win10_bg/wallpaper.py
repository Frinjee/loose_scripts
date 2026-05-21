import random, time
import os, ctypes
import ctypes,win32con


def getWallpaper():
    ubuf = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER,len(ubuf),ubuf,0) # ..Infow for x64
    return ubuf.value

def setWallpaper(path):
    changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER,0,path,changed) # ..Infow for x64

if __name__ == '__main__':
	minute = 2
	curr_wp = getWallpaper()
	wp_loc = 'imgur_scrape\\rBarn\\'
	wp_listing = os.listdir(wp_loc)
	while True:
		new_wp = random.choice(wp_listing)
		time.sleep(minute*60)
		i_suff = random.choice(wp_listing)
		if i_suff != new_wp:
			new_wp = wp_loc+i_suff
		else:
			time.sleep(minute*60)
			new_wp = random.choice(wp_listing)
		setWallpaper(new_wp)
#print(wp_listing)