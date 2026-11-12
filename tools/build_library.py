from pathlib import Path
import html, re, json, hashlib
ROOT = Path(__file__).resolve().parents[1]
RESEARCH, OUT = ROOT / 'research', ROOT / 'library'
FILES = sorted(RESEARCH.glob('[0-9][0-9]-*.md'))
TOPICS = {
'00':'evidence','01':'literacy','02':'teaching','03':'independence','04':'children','05':'access','06':'evidence','07':'evidence','08':'assessment','09':'safety','10':'teaching','11':'literacy','12':'evidence','13':'access','14':'safety','15':'literacy','16':'evidence','17':'teaching','18':'children','19':'teaching','20':'literacy','21':'adult','22':'evidence','23':'children'}
SOURCE_TOPICS={'01':'independence','02':'literacy','03':'teaching','04':'children','05':'children','06':'children','07':'literacy','08':'adult','09':'teaching','10':'adult','11':'safety','12':'safety','13':'safety','14':'access','15':'access','16':'teaching','17':'adult','18':'literacy','19':'teaching','20':'literacy','21':'adult','22':'children'}
LABELS={'evidence':'Reading evidence','literacy':'AI literacy','teaching':'Teaching','independence':'Independent learning','children':'Children','access':'Access and inclusion','assessment':'Assessment','safety':'Privacy and governance','adult':'Adult learning'}

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: '<a href="'+re.sub(r'\.md(?=#|$)', '.html', m[2]).replace('"','&quot;')+'">'+m[1]+'</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    return re.sub(r'(?<!\*)\*([^*]+)\*', r'<em>\1</em>', s)

def version(name):
    return name+'?v='+hashlib.sha256((OUT/name).read_bytes()).hexdigest()[:12]

def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def render(text):
    out=[]; para=[]; listing=False; ids=set()
    def flush():
        if para: out.append('<p>'+inline(' '.join(para))+'</p>'); para.clear()
    for line in text.splitlines()+['']:
        line=line.strip()
        if not line:
            flush()
            if listing: out.append('</ul>'); listing=False
        elif re.fullmatch(r'<a id="s\d{2}"></a>',line): flush(); out.append(line)
        elif line.startswith('#'):
            flush()
            if listing: out.append('</ul>'); listing=False
            level=len(line)-len(line.lstrip('#')); title=line[level:].strip(); ident=slug(title); base=ident; n=2
            while ident in ids: ident=base+'-'+str(n); n+=1
            ids.add(ident); out.append(f'<h{level} id="{ident}">'+inline(title)+f'</h{level}>')
        elif line.startswith('- ') or re.match(r'^\d+\. ',line):
            flush()
            if not listing: out.append('<ul>'); listing=True
            out.append('<li>'+inline(re.sub(r'^(?:- |\d+\. )','',line))+'</li>')
        else: para.append(line)
    return '\n'.join(out)

def page(title, body, kind='Research note'):
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Project Dux research on AI and education."><title>'''+html.escape(title)+''' — Project Dux</title><link rel="icon" href="../assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="'''+version('library.css')+'''"></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="../index.html">Project Dux <span>by Voelori</span></a><nav aria-label="Main navigation"><a href="../index.html">Home</a><a href="index.html">Research library</a><a href="06-method-and-questions.html">Our method</a></nav></header><main id="main" class="reading"><p class="eyebrow"><a href="index.html">Research library</a> / '''+html.escape(kind)+''' / 12 November 2026</p>'''+body+'''</main><footer>Project Dux · Learning is a human journey. <a href="index.html">Explore the library</a></footer></body></html>'''

OUT.mkdir(exist_ok=True)
items=[]
for f in FILES:
    t=f.read_text(encoding='utf-8-sig'); title=t.splitlines()[0].lstrip('# ').strip(); topic=TOPICS[f.stem[:2]]
    (OUT/(f.stem+'.html')).write_text(page(title, render(t), 'Source catalogue' if f.stem[:2]=='07' else 'Synthesis'),encoding='utf-8')
    items.append({'path':f.stem+'.html','title':title,'kind':'synthesis','topic':topic,'text':t.lower(),'number':f.stem[:2]})
records=(RESEARCH/'07-source-records.md').read_text(encoding='utf-8-sig')
parts=re.split(r'<a id="s(\d{2})"></a>\s*',records)
for i in range(1,len(parts),2):
    num, text = parts[i], parts[i+1].strip(); title=re.search(r'^### S\d+ — (.+)$',text,re.M).group(1)
    text=re.sub(r'^### S\d+ — (.+)$',r'# \1',text,count=1,flags=re.M)
    path='source-s'+num+'.html'; body=render(text)+'<p class="note">This dated source note is part of the <a href="07-source-records.html#s'+num+'">complete annotated source catalogue</a>. Read it alongside the <a href="06-method-and-questions.html">research method and open questions</a>.</p>'
    (OUT/path).write_text(page(title,body,'Source note S'+num),encoding='utf-8')
    items.append({'path':path,'title':title,'kind':'source','topic':SOURCE_TOPICS[num],'text':text.lower(),'number':num})
(OUT/'search-data.js').write_text('window.DUX_SEARCH = '+json.dumps(items,ensure_ascii=False)+';\n',encoding='utf-8')
cards=[]
for item in items:
    topic=LABELS[item['topic']]; kind='Source note' if item['kind']=='source' else ('Source catalogue' if item['number']=='07' else 'Synthesis')
    cards.append('<li data-path="'+item['path']+'" data-kind="'+item['kind']+'" data-topic="'+item['topic']+'"><a href="'+item['path']+'"><span>'+kind+' · '+html.escape(topic)+'</span><strong>'+html.escape(item['title'])+'</strong><span>Read the note →</span></a></li>')
options=''.join('<option value="'+k+'">'+html.escape(v)+'</option>' for k,v in LABELS.items())
body='''<p class="eyebrow">The Project Dux research library</p><h1>Go deeper. <em>Keep the learner in view.</em></h1><p class="lead">Explore studies, guidance, learning ideas and the questions they leave open. Search the full text or start with a reading path.</p><p class="note">A targeted collection, not a systematic review. Research snapshot: 12 November 2026. <a href="06-method-and-questions.html">How to read the evidence</a></p><div class="reading-paths"><a href="20-literacy-across-ages.html"><span>Start with understanding</span><strong>AI literacy across ages →</strong></a><a href="03-learning-and-independence.html"><span>Start with the learner</span><strong>Learning and independence →</strong></a><a href="04-children-and-safeguards.html"><span>Start with care</span><strong>Children and safeguards →</strong></a><a href="07-source-records.html"><span>Start with evidence</span><strong>Annotated source catalogue →</strong></a></div><h2>Find your next question.</h2><div id="controls" hidden><label for="filter">Search titles and full text</label><input id="filter" type="search" placeholder="Try feedback, privacy, or adult learning" autocomplete="off"><div class="filter-row"><label>Type<select id="kind"><option value="all">All types</option><option value="synthesis">Research chapters</option><option value="source">Individual source notes</option></select></label><label>Topic<select id="topic"><option value="all">All topics</option>'''+options+'''</select></label><button type="button" id="reset">Reset filters</button></div></div><p id="result" role="status">'''+str(len(items))+''' research chapters and source notes</p><noscript><p>All notes are listed below. Use your browser’s Find command to search titles.</p></noscript><ul class="catalog" id="catalog">'''+''.join(cards)+'''</ul><script src="'''+version('search-data.js')+'''" defer></script><script src="'''+version('library.js')+'''" defer></script>'''
(OUT/'index.html').write_text(page('Research library',body,'Catalogue'),encoding='utf-8')
print(f'Built {len(FILES)} chapters, {len(items)-len(FILES)} source notes and catalogue')
