from pathlib import Path
import html, re, json
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / 'research'
OUT = ROOT / 'library'
FILES = sorted(RESEARCH.glob('[0-9][0-9]-*.md'))

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: '<a href="'+re.sub(r'\.md(?=#|$)', '.html', m[2]).replace('"', '&quot;')+'">'+m[1]+'</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*', r'<em>\1</em>', s)
    return s

def render(text):
    out=[]; para=[]; listing=False
    def flush():
        if para:
            out.append('<p>'+inline(' '.join(para))+'</p>'); para.clear()
    for line in text.splitlines()+['']:
        line=line.strip()
        if not line:
            flush()
            if listing: out.append('</ul>'); listing=False
        elif re.fullmatch(r'<a id="s\d{2}"></a>',line):
            flush(); out.append(line)
        elif line.startswith('#'):
            flush()
            if listing: out.append('</ul>'); listing=False
            level=len(line)-len(line.lstrip('#')); title=line[level:].strip()
            out.append(f'<h{level}>'+inline(title)+f'</h{level}>')
        elif line.startswith('- '):
            flush()
            if not listing: out.append('<ul>'); listing=True
            out.append('<li>'+inline(line[2:])+'</li>')
        elif re.match(r'^\d+\. ',line):
            flush()
            if not listing: out.append('<ul>'); listing=True
            out.append('<li>'+inline(re.sub(r'^\d+\. ','',line))+'</li>')
        else: para.append(line)
    return '\n'.join(out)

def page(title, body):
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Project Dux research on AI and education."><title>'''+html.escape(title)+''' — Project Dux</title><link rel="icon" href="../assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="library.css"></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="../index.html">Project Dux <span>by Voelori</span></a><nav><a href="../index.html">Home</a><a href="index.html">Research library</a><a href="06-method-and-questions.html">Our method</a></nav></header><main id="main" class="reading"><p class="eyebrow"><a href="index.html">Research library</a> / 12 November 2026</p>'''+body+'''</main><footer>Project Dux · Learning is a human journey. <a href="index.html">Explore the library</a></footer></body></html>'''

OUT.mkdir(exist_ok=True)
for f in FILES:
    t=f.read_text(encoding='utf-8-sig'); title=t.splitlines()[0].lstrip('# ').strip()
    (OUT/(f.stem+'.html')).write_text(page(title, render(t)),encoding='utf-8')
cards=[]
search=[]
for f in FILES:
    t=f.read_text(encoding='utf-8-sig'); title=t.splitlines()[0].lstrip('# ').strip()
    search.append({'path':f.stem+'.html','text':t.lower()})
    cards.append('<li data-path="'+f.stem+'.html"><a href="'+f.stem+'.html"><span>'+f.stem[:2]+' / Research</span><strong>'+html.escape(title)+'</strong><span>Read the chapter →</span></a></li>')
body='''<p class="eyebrow">Research library / A foundation for learning</p><h1>Questions worth <em>learning with.</em></h1><p class="lead">Explore what research and guidance say about AI in education, and what remains uncertain. Read a chapter or search across the chapters below.</p><p class="note">A focused starting collection, not a systematic review. Research snapshot: 12 November 2026.</p><label for="filter">Find a chapter</label><input id="filter" type="search" placeholder="Search the research library" autocomplete="off"><p id="result" role="status"></p><ul class="catalog" id="catalog">'''+''.join(cards)+'''</ul><p><a href="07-source-records.html">Browse all annotated source records →</a></p><script src="search-data.js" defer></script><script src="library.js" defer></script>'''
(OUT/'index.html').write_text(page('Research library',body),encoding='utf-8')
(OUT/'search-data.js').write_text('window.DUX_SEARCH = '+json.dumps(search,ensure_ascii=False)+';\n',encoding='utf-8')
print(f'Built {len(FILES)} chapters and library index')
