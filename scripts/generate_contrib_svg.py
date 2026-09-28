#!/usr/bin/env python3
"""
Fetch GitHub contribution calendar SVG for a username and generate
a 52x7 '3D' extruded SVG into Assets/contrib-3d-52x.svg using the
project color palette.

Usage:
  python scripts/generate_contrib_svg.py --username <github-username>

This script scrapes `https://github.com/users/{username}/contributions` (public)
and converts per-day <rect> data into an extruded SVG visual.
"""

import argparse
import sys
import urllib.request
import re
from html import unescape


PALETTE = [('#0b1020', 0.0), ('#a855f7', 0.33), ('#22d3ee', 0.66), ('#34d399', 1.0)]


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def lerp(a, b, t):
    return a + (b - a) * t


def mix_color(t):
    # t in [0,1] across palette stops
    stops = PALETTE
    if t <= 0:
        return stops[0][0]
    if t >= 1:
        return stops[-1][0]
    for i in range(len(stops)-1):
        p0, w0 = stops[i]
        p1, w1 = stops[i+1]
        if w0 <= t <= w1:
            local = (t - w0) / (w1 - w0) if w1 != w0 else 0
            c0 = hex_to_rgb(p0)
            c1 = hex_to_rgb(p1)
            rgb = tuple(int(lerp(c0[j], c1[j], local)) for j in range(3))
            return rgb_to_hex(rgb)
    return stops[-1][0]


def fetch_contrib_svg(username):
    url = f'https://github.com/users/{username}/contributions'
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return r.read().decode('utf-8')
    except Exception as e:
        print('Error fetching contributions:', e)
        return None


def parse_rects(svg_text):
    # extract rects with data-date and data-count and x/y
    pattern = re.compile(r'<rect[^>]*data-date="(?P<date>[^"]+)"[^>]*data-count="(?P<count>\d+)"[^>]*x="(?P<x>[\d\.\-]+)"[^>]*y="(?P<y>[\d\.\-]+)"[^>]*/?>')
    items = []
    for m in pattern.finditer(svg_text):
        items.append({
            'date': m.group('date'),
            'count': int(m.group('count')),
            'x': float(m.group('x')),
            'y': float(m.group('y')),
        })
    return items


def build_grid(items):
    xs = sorted(sorted({i['x'] for i in items}))
    ys = sorted(sorted({i['y'] for i in items}))
    x_index = {x: idx for idx, x in enumerate(xs)}
    y_index = {y: idx for idx, y in enumerate(ys)}

    grid = [[0 for _ in range(len(xs))] for _ in range(len(ys))]
    maxc = 0
    for it in items:
        xi = x_index[it['x']]
        yi = y_index[it['y']]
        grid[yi][xi] = it['count']
        if it['count'] > maxc:
            maxc = it['count']
    return grid, maxc


def generate_svg(grid, maxc, out_path, username):
    cols = len(grid[0])
    rows = len(grid)
    cell = 12
    gap = 4
    margin_x = 40
    margin_y = 40
    width = margin_x*2 + cols*cell + (cols-1)*gap
    height = margin_y*2 + rows*cell + (rows-1)*gap + 80

    def color_for(count):
        if maxc <= 0:
            return '#071021'
        t = count / maxc
        return mix_color(t)

    parts = []
    parts.append(f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
    parts.append(f'<rect width="100%" height="100%" fill="#07050f" rx="14"/>')

    # title
    parts.append(f'<text x="{width/2}" y="28" text-anchor="middle" fill="#a855f7" font-size="16" font-weight="700">Contribution Galaxy — {username}</text>')

    # grid group
    parts.append(f'<g transform="translate({margin_x},{margin_y+20})">')

    for r in range(rows):
        for c in range(cols):
            count = grid[r][c]
            x = c * (cell + gap)
            y = r * (cell + gap)
            # extrusion height
            h = int((count / maxc) * 18) if maxc>0 else 0
            top_color = color_for(count)
            side_color = '#05101a'

            # top face
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{top_color}" stroke="#08101a" stroke-width="0.6" />')
            if h > 0:
                # right side polygon
                points = f"{x+cell},{y} {x+cell+h},{y+h} {x+cell+h},{y+cell+h} {x+cell},{y+cell}"
                parts.append(f'<polygon points="{points}" fill="{side_color}" opacity="0.55"/>')
                # bottom side polygon
                points2 = f"{x},{y+cell} {x+cell},{y+cell} {x+cell+h},{y+cell+h} {x+h},{y+cell+h}"
                parts.append(f'<polygon points="{points2}" fill="#021018" opacity="0.45"/>')

    parts.append('</g>')
    parts.append('</svg>')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))

    print('Wrote', out_path)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--username', '-u', required=True, help='GitHub username to fetch contributions for')
    p.add_argument('--out', '-o', default='Assets/contrib-3d-52x.svg', help='Output SVG file path')
    args = p.parse_args()

    svg = fetch_contrib_svg(args.username)
    if not svg:
        print('Failed to fetch contributions SVG. Exiting.')
        sys.exit(1)

    svg = unescape(svg)
    items = parse_rects(svg)
    if not items:
        print('No contribution rects found in fetched SVG. Exiting.')
        sys.exit(1)

    grid, maxc = build_grid(items)
    generate_svg(grid, maxc, args.out, args.username)


if __name__ == '__main__':
    main()
