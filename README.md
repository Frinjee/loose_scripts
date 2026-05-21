# z_fetch.py
Export Zotero group library items to a styled Excel workbook (.xlsx) from either a single collection tree or the full library. The output includes core item fields plus creator and collection metadata, with recursive traversal and deduplication built in

### usage
```bash
python z_fetch.py -g GROUP_ID -o out.xlsx
-a for full walk
    or
-c for a single collection tree
```

### output example
![out.png](https://github.com/Frinjee/loose_scripts/blob/main/zotero_groupitemfetch/out.png?raw=true)

# media_dl.py
Download X or YouTube videos and convert them to MP4, MP3, or both. The script supports video-only mode, audio-only mode, and full download plus conversion, with yt-dlp handling extraction and ffmpeg handling conversion.

### usage
```bash
python media_dl.py URL -a
-a for both mp4 & mp3
-v for only mp4
-m for only mp3
```