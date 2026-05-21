#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys


def convert_aiff(folder):
    for name in sorted(os.listdir(folder)):
        if not name.lower().endswith(('.aiff', '.aif')):
            continue

        src = os.path.join(folder, name)
        dst = os.path.splitext(src)[0] + '.wav'

        print(f'converting {name} -> {os.path.basename(dst)}')
        subprocess.run(
            ['ffmpeg', '-i', src, '-y', dst],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        os.remove(src)
        print(f'deleted {name}')


def rename_wav(folder):
    for name in sorted(os.listdir(folder)):
        if not name.lower().endswith('.wav'):
            continue

        parts = name.split('__', 2)
        if len(parts) < 3:
            print(f'skipping unexpected name: {name}')
            continue

        new_name = parts[2]
        if new_name == name:
            print(f'skipping already renamed: {name}')
            continue

        old_path = os.path.join(folder, name)
        new_path = os.path.join(folder, new_name)

        if os.path.exists(new_path):
            print(f'skipping overwrite: {new_name}')
            continue

        os.rename(old_path, new_path)
        print(f'renamed {name} -> {new_name}')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--folder', default='.')
    args = p.parse_args()

    if not os.path.isdir(args.folder):
        print('[ERROR] folder not found')
        sys.exit(1)

    convert_aiff(args.folder)
    rename_wav(args.folder)


if __name__ == '__main__':
    main()