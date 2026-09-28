#!/usr/bin/env python3
"""Annotate inner column <g> elements under #columns with style="--i:N" for staggered CSS animations.
Usage: python scripts/stagger_svg_columns.py [path-to-svg]
If path omitted, defaults to Assets/contrib-3d-52x.svg
"""
import sys
from xml.etree import ElementTree as ET

svg_path = sys.argv[1] if len(sys.argv) > 1 else 'Assets/contrib-3d-52x.svg'

# Parse with ET and handle default namespace if present
with open(svg_path, 'r', encoding='utf-8') as f:
    data = f.read()

# Find namespace if any
ns = ''
if data.lstrip().startswith('<?xml'):
    pass

# Register SVG namespace to preserve it
ET.register_namespace('', 'http://www.w3.org/2000/svg')
root = ET.fromstring(data)

# Helper to strip namespace
def strip_tag(tag):
    return tag.split('}', 1)[1] if '}' in tag else tag

# Find element with id==columns
columns_elem = None
for elem in root.iter():
    if elem.get('id') == 'columns':
        columns_elem = elem
        break

if columns_elem is None:
    print('No element with id="columns" found.')
    sys.exit(1)

# Collect inner groups that directly contain a rect child
targets = []
# We want all descendant <g> elements that contain a rect as direct child
for g in columns_elem.findall('.//{http://www.w3.org/2000/svg}g'):
    # check if any direct child is a rect
    has_rect = any(strip_tag(ch.tag) == 'rect' for ch in list(g))
    if has_rect:
        targets.append(g)

# Assign style attribute --i sequentially
for idx, g in enumerate(targets):
    existing = g.get('style', '')
    # preserve existing style, append --i
    new_style = existing + (' ' if existing and not existing.endswith(';') else '') + f'--i:{idx}'
    g.set('style', new_style)

# Write back
ET.indent(root, space="  ")
new_xml = ET.tostring(root, encoding='unicode')
with open(svg_path, 'w', encoding='utf-8') as f:
    f.write(new_xml)

print(f'Annotated {len(targets)} groups with --i values in {svg_path}')
