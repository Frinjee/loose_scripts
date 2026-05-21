#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

import yt_dlp


def parse_args():
    p = argparse.ArgumentParser(
        description='Download an X or YouTube video and optionally convert the audio to MP3.'
    )
    p.add_argument('url', help='video url')
    p.add_argument('-d', '--dir', default='downloads', help='output directory')
    p.add_argument('-b', '--bitrate', default='192k', help='mp3 bitrate, e.g. 128k, 192k, 256k, 320k')
    p.add_argument('--js-runtime', default='deno', help='yt-dlp javascript runtime for YouTube extraction')

    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('-a', action='store_true', help='download mp4 and mp3')
    mode.add_argument('-v', action='store_true', help='download only mp4')
    mode.add_argument('-m', action='store_true', help='download only mp3')

    return p.parse_args()


def build_common_opts(output_dir, js_runtime):
    return {
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
        'js_runtimes': js_runtime,
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
            }
        },
        'outtmpl': str(Path(output_dir) / '%(title).80s.%(ext)s'),
    }


def download_video(url, output_dir, js_runtime):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = build_common_opts(output_dir, js_runtime)
    ydl_opts.update({
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
    })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = Path(ydl.prepare_filename(info))
        if filename.suffix.lower() != '.mp4':
            filename = filename.with_suffix('.mp4')

    print(f'saved video: {filename}')
    return filename


def download_mp3(url, output_dir, bitrate, js_runtime):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = build_common_opts(output_dir, js_runtime)
    ydl_opts.update({
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate.rstrip('k'),
            }
        ],
    })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        base = Path(ydl.prepare_filename(info))
        mp3_path = base.with_suffix('.mp3')

    print(f'saved mp3: {mp3_path}')
    return mp3_path


def convert_mp4_to_mp3(mp4_path, bitrate):
    mp4_path = Path(mp4_path)
    if not mp4_path.exists():
        print(f'[ERROR] file not found: {mp4_path}')
        return None

    mp3_path = mp4_path.with_suffix('.mp3')
    cmd = [
        'ffmpeg',
        '-y',
        '-i',
        str(mp4_path),
        '-vn',
        '-acodec',
        'libmp3lame',
        '-b:a',
        bitrate,
        '-ar',
        '44100',
        str(mp3_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr.strip())
        return None

    print(f'saved mp3: {mp3_path}')
    return mp3_path


def main():
    args = parse_args()

    if not args.url.strip():
        print('[ERROR] no url provided')
        sys.exit(1)

    if args.m:
        mp3_file = download_mp3(args.url.strip(), args.dir, args.bitrate, args.js_runtime)
        print('done')
        print(f'  mp3 -> {mp3_file}')
        return

    mp4_file = download_video(args.url.strip(), args.dir, args.js_runtime)
    if not mp4_file:
        print('[ERROR] download failed')
        sys.exit(1)

    if args.v:
        print('done')
        print(f'  mp4 -> {mp4_file}')
        return

    mp3_file = convert_mp4_to_mp3(mp4_file, args.bitrate)
    if not mp3_file:
        print('[ERROR] mp3 conversion failed')
        sys.exit(1)

    print('done')
    print(f'  mp4 -> {mp4_file}')
    print(f'  mp3 -> {mp3_file}')


if __name__ == '__main__':
    main()