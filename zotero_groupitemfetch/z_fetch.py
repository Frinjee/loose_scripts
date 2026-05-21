#!/usr/bin/env python3
import argparse
import sys

import pandas as pd
from pyzotero import zotero


FIELDS = [
    'key', 'itemType', 'title', 'date', 'url',
    'abstractNote', 'language', 'rights',
    'publisher', 'place', 'edition',
    'journalAbbreviation', 'volume', 'issue', 'pages',
    'series', 'seriesTitle', 'websiteTitle',
    'institution', 'university', 'libraryCatalog',
    'callNumber', 'archiveLocation', 'dateAdded', 'dateModified',
]


def get_creators(data):
    creators = data.get('creators', [])
    parts = []

    for c in creators:
        last = c.get('lastName')
        if last:
            parts.append(f"{last}, {c.get('firstName', '')}".strip())
        else:
            name = c.get('name', '')
            if name:
                parts.append(name)

    return '; '.join(parts)


def get_collections(data):
    return '; '.join(data.get('collections', []))


def parse_args():
    p = argparse.ArgumentParser(
        description='Export Zotero group items to a styled Excel workbook.'
    )
    p.add_argument('-g', '--group-id', type=int, default=320614, help='zotero group id')
    p.add_argument('-o', '--output', default='zotero_group_320614.xlsx', help='output xlsx file')

    mode = p.add_mutually_exclusive_group()
    mode.add_argument('-c', '--collection-id', help='root collection id to fetch recursively')
    mode.add_argument('-a', '--all', action='store_true', help='fetch full library recursively')

    return p.parse_args()


def collect_items_from_collections(zot, collection_ids):
    seen = set()
    items = []

    for coll_id in collection_ids:
        for item in zot.collection_items(coll_id):
            item_key = item.get('key') or item.get('data', {}).get('key')
            if not item_key or item_key in seen:
                continue
            seen.add(item_key)
            items.append(item)

    return items, seen


def fetch_recursive(zot, collection_id):
    collections = zot.all_collections(collid=collection_id)
    coll_ids = [c.get('key') for c in collections if c.get('key')]
    return collect_items_from_collections(zot, coll_ids)


def fetch_full_library_recursive(zot):
    collections = zot.all_collections()
    coll_ids = [c.get('key') for c in collections if c.get('key')]
    items, seen = collect_items_from_collections(zot, coll_ids)

    print('fetching unfiled items...')
    for item in zot.everything(zot.top()):
        item_key = item.get('key') or item.get('data', {}).get('key')
        if not item_key or item_key in seen:
            continue
        seen.add(item_key)
        items.append(item)

    return items


def build_rows(all_items):
    rows = []

    for item in all_items:
        data = item.get('data', {})
        row = {field: data.get(field, '') for field in FIELDS}
        row['creators'] = get_creators(data)
        row['collections'] = get_collections(data)
        rows.append(row)

    return rows


def style_sheet(writer, df):
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    header_fmt = workbook.add_format({
        'bold': True,
        'font_name': 'Georgia',
        'font_color': '#FFFFFF',
        'bg_color': '#4A5568',
        'text_wrap': True,
        'valign': 'top',
        'border': 0,
    })

    body_fmt = workbook.add_format({
        'font_name': 'Arial',
        'font_size': 10,
        'font_color': '#333333',
        'text_wrap': True,
        'valign': 'top',
        'border': 0,
    })

    alt_fmt = workbook.add_format({
        'font_name': 'Arial',
        'font_size': 10,
        'font_color': '#333333',
        'bg_color': '#F7FAFC',
        'text_wrap': True,
        'valign': 'top',
        'border': 0,
    })

    worksheet.freeze_panes(1, 0)

    max_width = 30
    for col_idx, col_name in enumerate(df.columns):
        values = [str(col_name)] + [str(v) if v is not None else '' for v in df.iloc[:, col_idx].tolist()]
        width = min(max(len(v) for v in values) + 2, max_width)
        worksheet.set_column(col_idx, col_idx, width, body_fmt)

    worksheet.set_row(0, None, header_fmt)

    for row_idx in range(1, len(df) + 1):
        fmt = alt_fmt if row_idx % 2 == 0 else body_fmt
        worksheet.set_row(row_idx, None, fmt)

    worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)


def main():
    args = parse_args()
    zot = zotero.Zotero(args.group_id, 'group')

    if args.all:
        print('fetching full library recursively...')
        all_items = fetch_full_library_recursive(zot)
    elif args.collection_id:
        print(f'fetching collection tree: {args.collection_id}')
        all_items, _ = fetch_recursive(zot, args.collection_id)
    else:
        print('fetching top-level items...')
        all_items = zot.everything(zot.top())

    print(f'total items retrieved: {len(all_items)}')

    rows = build_rows(all_items)
    df = pd.DataFrame(rows, columns=['creators', 'collections'] + FIELDS)

    try:
        with pd.ExcelWriter(args.output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            style_sheet(writer, df)
    except ImportError:
        print('[ERROR] xlsxwriter is required for xlsx export')
        sys.exit(1)

    print(f'saved to: {args.output}')


if __name__ == '__main__':
    main()