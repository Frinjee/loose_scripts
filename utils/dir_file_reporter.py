#!/usr/bin/env python3
from pathlib import Path


def main():
    directories = [
        Path('./'),
        Path('./'),
        Path('./'),
        Path('./'),
        Path('./'),
    ]

    output_file = Path('dirfile_list.txt')

    with output_file.open('w', encoding='utf-8') as f:
        for directory in directories:
            f.write(f'\n=== files in: {directory} ===\n')
            if not directory.exists():
                f.write('[directory not found]\n')
                continue

            for item in sorted(directory.iterdir()):
                if item.is_file():
                    f.write(f'{item.name}\n')

    print(f'wrote file names to {output_file}')


if __name__ == '__main__':
    main()