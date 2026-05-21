import PySimpleGUI as psg
import cv2 

layout = [
	[psg.Image(key = '-IMAGE-')], 
	[psg.Text('# of faces in picture: 0', key = '-TEXT-', expand_x = True, justification = 'center')]
]
win = psg.Window('FaceIt', layout, resizable=True)

# get video
vid_stream = cv2.VideoCapture(0) # input source
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
	event, values = win.read(timeout = 0)
	if event == psg.WIN_CLOSED:
		break

	_, frame = vid_stream.read()
	grey_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(grey_scale, scaleFactor = 1.3, minNeighbors = 7, minSize = (25,25))

	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (233, 124, 0), 2)
	# update image
	img_bytes = cv2.imencode('.png', frame)[1].tobytes()
	win['-IMAGE-'].update(data = img_bytes)

	# update # text
	win['-TEXT-'].update(f'# of faces in picture: {len(faces)}')
win.close()