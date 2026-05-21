#!/usr/bin/env python3
from pathlib import Path

from PIL import Image


def main():
    root = Path('.')
    bmp_files = sorted(root.glob('*.bmp'))

    if not bmp_files:
        print('no bmp files found')
        return

    print(f'found {len(bmp_files)} bmp files')

    css_lines = ['/* generated css skeleton */', '']

    for bmp in bmp_files:
        png_path = bmp.with_suffix('.png')
        with Image.open(bmp) as img:
            img.save(png_path)
            w, h = img.size

        print(f'converted {bmp.name} -> {png_path.name}')

        name = bmp.stem.lower()

        if name in {'main', 'eqmain', 'pledit'}:
            css_lines.append(f'/* {bmp.name}: base panel */')
            css_lines.append(f'#{name}-panel {{')
            css_lines.append('  position: relative;')
            css_lines.append(f'  width: {w}px;')
            css_lines.append(f'  height: {h}px;')
            css_lines.append(f"  background: url('./{png_path.name}') no-repeat 0 0;")
            css_lines.append('}')
            css_lines.append('')
        else:
            css_lines.append(f'/* {bmp.name}: sprite sheet or icon set */')
            css_lines.append(f'.{name}-sprite {{')
            css_lines.append(f"  background-image: url('./{png_path.name}');")
            css_lines.append('  background-repeat: no-repeat;')
            css_lines.append('}')
            css_lines.append('')

    helper_path = Path('winamp-mapping.txt')
    helper_path.write_text('\n'.join(css_lines), encoding='utf-8')
    print(f'wrote mapping helper to {helper_path.resolve()}')


if __name__ == '__main__':
    main()