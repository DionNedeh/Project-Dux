"""Check the Project Dux site: local links and anchors, unique IDs, one h1 per page, versioned
assets, the catalogue's search controls, the homepage tools, and source records.

    python tools/check_library.py
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re, sys, hashlib

root = Path(__file__).resolve().parents[1]
BASE = '/Project-Dux/'
errors = []


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.duplicates, self.h1, self.inline_style = set(), [], [], 0, False
        self.in_script_inline = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'h1':
            self.h1 += 1
        if 'style' in d:
            self.inline_style = True
        if tag == 'style' or (tag == 'script' and 'src' not in d):
            self.in_script_inline = True
        if 'id' in d:
            if d['id'] in self.ids:
                self.duplicates.append(d['id'])
            self.ids.add(d['id'])
        for key in ('href', 'src'):
            if key in d:
                self.links.append(d[key])


def version(path):
    return path.name + '?v=' + hashlib.sha256(path.read_bytes()).hexdigest()[:12]


pages = {}
for p in sorted(root.rglob('*.html')):
    if '.git' in p.parts:
        continue
    scan = Scan()
    scan.feed(p.read_text(encoding='utf-8-sig'))
    pages[p.resolve()] = scan
    rel = p.relative_to(root)
    if scan.duplicates:
        errors.append(f'{rel}: duplicate ids {scan.duplicates}')
    if scan.h1 != 1:
        errors.append(f'{rel}: expected one h1, found {scan.h1}')
    if scan.inline_style or scan.in_script_inline:
        errors.append(f'{rel}: inline style or script would be blocked by the Content-Security-Policy')

for p, scan in pages.items():
    rel = p.relative_to(root.resolve())
    for link in scan.links:
        u = urlsplit(link)
        if u.scheme or u.netloc:
            continue
        if u.path.startswith(BASE):
            target = (root / unquote(u.path[len(BASE):])).resolve()
        elif u.path.startswith('/'):
            errors.append(f'{rel}: absolute link outside the site base {link}'); continue
        else:
            target = (p.parent / unquote(u.path)).resolve() if u.path else p
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            errors.append(f'{rel}: missing local target {link}'); continue
        if u.fragment and (target not in pages or unquote(u.fragment) not in pages[target].ids):
            errors.append(f'{rel}: missing anchor {link}')

# Versioned assets: every reference to these must carry the current content hash.
assets = {root / 'styles.css', root / 'site.js', root / 'library/library.css', root / 'library/library.js', root / 'library/search-data.js'}
for p, scan in pages.items():
    for link in scan.links:
        path = urlsplit(link).path
        for asset in assets:
            if path.endswith(asset.name) and (path == asset.name or path.endswith('/' + asset.name)):
                if not link.endswith(version(asset)):
                    errors.append(f'{p.relative_to(root.resolve())}: stale or unversioned asset {link}; run tools/build_library.py')

library = root / 'library'
catalogue = pages[(library / 'index.html').resolve()]
for ident in ('controls', 'filter', 'kind', 'topic', 'sort', 'reset', 'result', 'empty', 'catalog'):
    if ident not in catalogue.ids:
        errors.append(f'catalogue missing #{ident}')

home_scan = pages[(root / 'index.html').resolve()]
for ident in ('fit-select', 'fit-verdict', 'roles-field', 'roles-body', 'sort-play', 'sort-static', 'percent-base',
              'percent-change', 'percent-sum', 'checkin-form', 'checkin-result', 'findings', 'timeline-list', 'motion'):
    if ident not in home_scan.ids:
        errors.append(f'home missing #{ident}')

source = (root / 'research/07-source-records.md').read_text(encoding='utf-8')
numbers = re.findall(r'<a id="s(\d{2})"></a>', source)
expected = [f'{i:02}' for i in range(1, len(numbers) + 1)]
if numbers != expected:
    errors.append(f'source anchors not sequential: {numbers}')
if len(numbers) < 22:
    errors.append(f'expected at least 22 sources, found {len(numbers)}')
for n in numbers:
    if not (library / f'source-s{n}.html').is_file():
        errors.append(f'missing page for source S{n}')

index = (root / 'index.html').read_text(encoding='utf-8')
for expected_text in ['An abstract open book with a growing stem', 'What am I trying to learn for myself?',
                      'Spencer Hinson', 'Pause motion', 'library/index.html', 'Content-Security-Policy']:
    if expected_text not in index:
        errors.append(f'home missing {expected_text}')
if 'A visual draft for discussion' in index:
    errors.append('draft label remains')

if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'PASS: {len(pages)} HTML pages; links, anchors, unique IDs, one h1 each, no inline style or script, '
      f'versioned assets, catalogue controls, homepage tools, and {len(numbers)} sequential source records.')
