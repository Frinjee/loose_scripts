# 1. Determine EPD
# EPS x DAY = EPD
# 2. Determine disk space (raw v norm)
# EPD x RAW = SIZE
#		(NORM)
# 3. Compress Events with 10:1, divide daily size by 10
# SIZE / 10 - DISK(raw/norm)
# 4. Determine the annual req disk space by multiplying daily disk req by 365
# DISK (raw/norm) x 365 = Year
# to determine the storage req for the EPS measure
# EPD x RAW/10 * 365 = YEAR(compressed)
# EPD x NORM/10 * 365 = YEAR(compressed)


DAY = 86400 # seconds
RAW = 600 #bytes
NORM = 1500 #bytes
COMPRESS = 10 # 10:1
EPS = 0
EPD = 0
YEAR = 365

def convert_byte_to_gb(data):
	conv_dict = {'k': 1, 'm':2, 'g': 3}
	_ = float(data)
	byte_size = 1024
	return data / (byte_size ** conv_dict['g'])


def calc_epd_and_size(eps):
	EPD = eps * DAY
	print(f'EPD is {EPD}')

	raw_size = EPD * RAW
	norm_size = EPD * NORM

	daily_disk_raw = raw_size / COMPRESS
	daily_disk_norm = norm_size / COMPRESS
	
	disk_raw = daily_disk_raw * YEAR
	disk_norm = daily_disk_norm * YEAR

	comp_raw = round(EPD * disk_raw / 10 * 365)
	comp_norm = round(EPD * disk_norm / 10 * 365)

	raw_size = round(convert_byte_to_gb(raw_size),2)
	norm_size = round(convert_byte_to_gb(norm_size),2)

	daily_disk_raw = round(convert_byte_to_gb(daily_disk_raw),2)
	daily_disk_norm = round(convert_byte_to_gb(daily_disk_norm),2)

	disk_raw = round(convert_byte_to_gb(disk_raw),2)
	disk_norm = round(convert_byte_to_gb(disk_norm),2)

	comp_raw = round(convert_byte_to_gb(comp_raw),2)
	comp_norm = round(convert_byte_to_gb(comp_norm),2)


	print(f'RAW SIZE: {raw_size} gb \nNORM SIZE: {norm_size} gb \nDaily Disk Required: \nRAW - {daily_disk_raw} gb \nNORM - {daily_disk_norm} gb')
	print(f'Annual disk space required: \nRAW - {disk_raw} gb \nNORM - {disk_norm} gb \nCompressed RAW - {comp_raw} gb \nCompressed Norm - {comp_norm} gb')
	
def firewall_calc():
	firewall_str = '1. Check Point - Internal, 2. Cisco - Internal, 3. Check Point DMZ, 4. Cisco DMZ'
	select_firewall = input('Select an option: ' + firewall_str)

	if select_firewall == '1' or select_firewall == '2':
		num_dev = input('Enter number of firewalls: ')
		EPS = 10 * int(num_dev)
		calc_epd_and_size(EPS)
	if select_firewall == '3' or select_firewall == '4':
		num_dev = input('Enter number of firewalls: ')
		EPS = 50 * int(num_dev)
		calc_epd_and_size(EPS)

def switch_calc():
	num_dev = input('Enter number of switches: ')
	EPS = 2 * int(num_dev)
	calc_epd_and_size(EPS)


def workstations_calc():
	num_dev = input('Enter number of Desktops: ')
	EPS = 1 * int(num_dev)
	calc_epd_and_size(EPS)

def windows_servers_calc():
	server_string = '1. HIGH EPS, 2. MED EPS, 3. LOW EPS'
	select_server = input('Select est EPS value: ' + server_string)

	if select_server == '1':
		num_dev = input('Enter number of servers: ')
		EPS = 50 * int(num_dev)
		calc_epd_and_size(EPS)
	if select_server == '2':
		num_dev = input('Enter number of servers: ')
		EPS = 3 * int(num_dev)
		calc_epd_and_size(EPS)
	if select_server == '3':
		num_dev = input('Enter number of servers: ')
		EPS = 1 * int(num_dev)
		calc_epd_and_size(EPS)

def load_balancer_calc():
	num_dev = input('Enter number of load balancers: ')
	EPS = 5 * int(num_dev)
	calc_epd_and_size(EPS)

def linux_server_calc():
	num_dev = input('Enter number of linux servers: ')
	num_web = input('Enter number of web servers: ')
	num_dev = int(num_dev)
	num_web = int(num_web)
	if num_web <= 0:
		EPS = 1 * num_dev
		calc_epd_and_size(EPS)
	if num_web > 0:
		EPS = 2 * (num_web  + num_dev)
		calc_epd_and_size(EPS)

def main_menu():
	main_str = '\n1. Firewalls, 2. Switches, 3. Windows Desktops, 4. Windows Servers, \n5.Linux Servers + Web Servers, 6. Load Balancers, 7. Exit '
	main_selection = input('Select an option:' + main_str + '\n')

	if main_selection == '1': firewall_calc()
	if main_selection == '2': switch_calc()
	if main_selection == '3': workstations_calc()
	if main_selection == '4': windows_servers_calc()
	if main_selection == '5': linux_server_calc()
	if main_selection == '6': load_balancer_calc()
	if main_selection == '7': sys.exit()
main_menu()