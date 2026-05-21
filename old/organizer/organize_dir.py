import os
from pathlib import Path

SUBDIRECTORIES = {
	"DOCUMENTS": ['.pdf','.txt'],
	"AUDIO": ['.m4a','.mp3'],
	"VIDEOS": ['.mp4','.mov','.mkv'],
	"IMAGES": ['.jpg','.jpeg','.png']
	"CODE": ['.py', '.java', '.html', '.css', '.js']
}

def sel_directory(val):
	for category, suffixes in SUBDIRECTORIES.items():
		for suff in suffixes:
			if suff == val:
				return category
	return 'MISC'
print(sel_directory('.jpg'))

def organize_directory():
	for items in os.scandir():
		if items.is_dir():
			continue
		item_path = Path(items)
		filetype = item_path.suffix.lower()
		directory = sel_directory(filetype)
		dir_path = Path(directory)

		if dir_path.is_dir() != True:
			dir_path.mkdir()
		item_path.rename(dir_path.joinpath(item_path))
organize_directory()