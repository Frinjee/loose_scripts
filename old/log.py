import win32evtlog
import datetime



def get_app_events():
	log_type = 'Application'
	server = 'localhost'
	events = []

	handle = win32evtlog.OpenEventLog(server, log_type)
	flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

	while True:
		records = win32evtlog.ReadEventLog(handle, flags, 0)
		if not records:
			break

		for record in records:
			if record.EventID in [1033, 11724]:
				events.append((record.TimeGenerated, record.SourceName, record.StringInserts))

	win32evtlog.CloseEventLog(handle)
	return events


def log_events(events):
	now = datetime.datetime.now()
	date = now.strftime('%Y-%m-%d')
	time = now.strftime('%H-%M-%S')
	file = f'{date}_{time}_log.txt'

	with open(file, 'w') as file:
		for event in events:
			time_generated = event[0].strftime('%Y-%m-%d %H:%M:%S')
			source_name = event[1]
			string_inserts = ' | '.join(event[2]) if event[2] else 'No additional details'
			file.write(f'Time: {time_generated}, Source: {source_name}, Details: {string_inserts}\n')

	print(f'Events logged to file: {file}')

if __name__ == '__main__':
	events = get_app_events()

	if events:
		log_events(events)
	else:
		print('No matching events found.')