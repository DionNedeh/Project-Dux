from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re, sys, hashlib
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
library=root/'library'
assets={name: name+'?v='+hashlib.sha256((library/name).read_bytes()).hexdigest()[:12] for name in ('library.css','library.js','search-data.js')}
for p in library.glob('*.html'):
    for link in pages[p.resolve()].links:
        name=urlsplit(link).path
        if name in assets and link!=assets[name]: errors.append(f'{p}: stale or unversioned asset {link}; rebuild the library')
catalogue=(library/'index.html').read_text(encoding='utf-8')
for name in ('library.js','search-data.js'):
    if assets[name] not in catalogue: errors.append(f'catalogue missing versioned {name}')
for ident in ('controls','filter','kind','topic','reset','result','catalog'):
    if ident not in pages[(library/'index.html').resolve()].ids: errors.append(f'catalogue missing #{ident}')
source=(root/'research/07-source-records.md').read_text(encoding='utf-8')
for i in range(1,23):
    if f'id="s{i:02}"' not in source: errors.append(f'missing source S{i:02}')
index=(root/'index.html').read_text(encoding='utf-8')
for expected in ['An abstract open book with a growing stem','What am I trying to learn for myself?', 'Spencer Hinson', 'Pause motion', 'library/index.html']:
    if expected not in index: errors.append(f'home missing {expected}')
if 'A visual draft for discussion' in index: errors.append('draft label remains')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'PASS: {len(pages)} HTML pages, local references and anchors, unique IDs, versioned library assets, search controls, twenty-two source IDs, and key homepage content.')
