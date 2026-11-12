from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re, sys
root=Path(__file__).resolve().parents[1]
errors=[]
class Scan(HTMLParser):
    def __init__(self): super().__init__(); self.ids=set(); self.links=[]; self.duplicates=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:
            if d['id'] in self.ids: self.duplicates.append(d['id'])
            self.ids.add(d['id'])
        for key in ('href','src'):
            if key in d: self.links.append(d[key])
pages={}
for p in root.rglob('*.html'):
    scan=Scan(); scan.feed(p.read_text(encoding='utf-8-sig')); pages[p.resolve()]=scan
    if scan.duplicates: errors.append(f'{p}: duplicate ids {scan.duplicates}')
for p, scan in pages.items():
    for link in scan.links:
        u=urlsplit(link)
        if u.scheme or u.netloc: continue
        target=(p.parent / unquote(u.path)).resolve() if u.path else p
        if not target.is_relative_to(root.resolve()) or not target.is_file(): errors.append(f'{p}: missing local target {link}'); continue
        if u.fragment and (target not in pages or unquote(u.fragment) not in pages[target].ids): errors.append(f'{p}: missing anchor {link}')
source=(root/'research/07-source-records.md').read_text(encoding='utf-8')
for i in range(1,18):
    if f'id="s{i:02}"' not in source: errors.append(f'missing source S{i:02}')
index=(root/'index.html').read_text(encoding='utf-8')
for expected in ['An abstract open book with a growing stem','What am I trying to learn for myself?', 'Spencer Hinson', 'Pause motion', 'library/index.html']:
    if expected not in index: errors.append(f'home missing {expected}')
if 'A visual draft for discussion' in index: errors.append('draft label remains')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'PASS: {len(pages)} HTML pages, local references and anchors, unique IDs, seventeen source IDs, and key homepage content.')
