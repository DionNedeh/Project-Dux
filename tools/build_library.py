"""Build the Project Dux research library from research/*.md.

Deterministic and standard-library only. Run from anywhere:
    python tools/build_library.py
Then check with tools/check_library.py.
"""
from pathlib import Path
import html, re, json, hashlib, math

ROOT = Path(__file__).resolve().parents[1]
RESEARCH, OUT = ROOT / 'research', ROOT / 'library'
FILES = sorted(RESEARCH.glob('[0-9][0-9]-*.md'))
SNAPSHOT = '12 November 2026'
BASE_URL = '/Project-Dux/'

TOPICS = {
    '00': 'evidence', '01': 'literacy', '02': 'teaching', '03': 'independence', '04': 'children', '05': 'access',
    '06': 'evidence', '07': 'evidence', '08': 'assessment', '09': 'safety', '10': 'teaching', '11': 'literacy',
    '12': 'evidence', '13': 'access', '14': 'safety', '15': 'literacy', '16': 'evidence', '17': 'teaching',
    '18': 'children', '19': 'teaching', '20': 'literacy', '21': 'adult', '22': 'evidence', '23': 'children',
    '24': 'independence', '25': 'independence', '26': 'access', '27': 'assessment', '28': 'evidence',
}
SOURCE_TOPICS = {
    '01': 'independence', '02': 'literacy', '03': 'teaching', '04': 'children', '05': 'children', '06': 'children',
    '07': 'literacy', '08': 'adult', '09': 'teaching', '10': 'adult', '11': 'safety', '12': 'safety', '13': 'safety',
    '14': 'access', '15': 'access', '16': 'teaching', '17': 'adult', '18': 'literacy', '19': 'teaching',
    '20': 'literacy', '21': 'adult', '22': 'children', '23': 'independence', '24': 'independence', '25': 'adult',
    '26': 'independence', '27': 'evidence', '28': 'access', '29': 'assessment', '30': 'assessment', '31': 'children',
    '32': 'children', '33': 'teaching', '34': 'children',
}
LABELS = {
    'evidence': 'Reading evidence', 'literacy': 'AI literacy', 'teaching': 'Teaching',
    'independence': 'Independent learning', 'children': 'Children', 'access': 'Access and inclusion',
    'assessment': 'Assessment', 'safety': 'Privacy and governance', 'adult': 'Adult learning',
}
CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
       "object-src 'none'; base-uri 'none'; form-action 'none'")
SOURCE_LINK = re.compile(r'07-source-records\.md#s(\d{2})')


def version(path):
    """Return a URL for a local asset with a short content hash, so a deploy never pairs new
    HTML with a script or stylesheet a browser cached earlier."""
    return path.name + '?v=' + hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
               lambda m: '<a href="' + re.sub(r'\.md(?=#|$)', '.html', m[2]).replace('"', '&quot;') + '">' + m[1] + '</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    return re.sub(r'(?<!\*)\*([^*]+)\*', r'<em>\1</em>', s)


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def render(text):
    """Small Markdown subset -> HTML. Returns (html, headings) where headings is [(level, id, text)]."""
    out, para, heads, ids = [], [], [], set()
    listing = False

    def flush():
        if para:
            out.append('<p>' + inline(' '.join(para)) + '</p>')
            para.clear()

    for line in text.splitlines() + ['']:
        line = line.strip()
        if not line:
            flush()
            if listing:
                out.append('</ul>'); listing = False
        elif re.fullmatch(r'<a id="s\d{2}"></a>', line):
            flush(); out.append(line)
        elif line.startswith('#'):
            flush()
            if listing:
                out.append('</ul>'); listing = False
            level = len(line) - len(line.lstrip('#'))
            title = line[level:].strip()
            ident = base = slug(title); n = 2
            while ident in ids:
                ident = f'{base}-{n}'; n += 1
            ids.add(ident)
            heads.append((level, ident, title))
            anchor = '' if level == 1 else f' <a class="anchor" href="#{ident}" aria-label="Link to this section">#</a>'
            out.append(f'<h{level} id="{ident}">' + inline(title) + anchor + f'</h{level}>')
        elif line.startswith('- ') or re.match(r'^\d+\. ', line):
            flush()
            if not listing:
                out.append('<ul>'); listing = True
            out.append('<li>' + inline(re.sub(r'^(?:- |\d+\. )', '', line)) + '</li>')
        else:
            para.append(line)
    return '\n'.join(out), heads


def toc(heads):
    level = 2 if sum(1 for h in heads if h[0] == 2) >= 3 else 3
    picked = [h for h in heads if h[0] == level]
    if len(picked) < 3:
        return ''
    links = ''.join(f'<li><a href="#{i}">{inline(t)}</a></li>' for _, i, t in picked)
    return f'<nav class="toc" aria-labelledby="toc-title"><p class="toc-title" id="toc-title">On this page</p><ol>{links}</ol></nav>'


def minutes(text):
    return max(1, math.ceil(len(re.findall(r"\w+", text)) / 200))


def page(title, body, kind, css, scripts='', description='Project Dux research on AI and education.'):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta http-equiv="Content-Security-Policy" content="{CSP}">'
            f'<meta name="description" content="{html.escape(description)}">'
            f'<title>{html.escape(title)} — Project Dux</title>'
            '<link rel="icon" href="../assets/mark.svg" type="image/svg+xml">'
            f'<link rel="stylesheet" href="{css}"></head><body>'
            '<a class="skip" href="#main">Skip to content</a>'
            '<header><a class="brand" href="../index.html">Project Dux <span>by Voelori</span></a>'
            '<nav aria-label="Main navigation"><a href="../index.html">Home</a><a href="../index.html#tools">Tools</a>'
            '<a href="index.html">Research library</a><a href="06-method-and-questions.html">Our method</a></nav></header>'
            '<main id="main" class="reading"><p class="eyebrow"><a href="index.html">Research library</a> / '
            + html.escape(kind) + ' / ' + SNAPSHOT + '</p>' + body + scripts + '</main>'
            '<footer><span>Project Dux · Learning is a human journey.</span><a href="index.html">Explore the library</a></footer>'
            '</body></html>')


def pager(prev, nxt):
    parts = []
    if prev:
        parts.append(f'<a class="prev" href="{prev["path"]}"><span>Previous</span><strong>{html.escape(prev["title"])}</strong></a>')
    if nxt:
        parts.append(f'<a class="next" href="{nxt["path"]}"><span>Next</span><strong>{html.escape(nxt["title"])}</strong></a>')
    return '<nav class="pager" aria-label="Previous and next notes">' + ''.join(parts) + '</nav>' if parts else ''


def link_list(title, items, ident):
    if not items:
        return ''
    lis = ''.join(f'<li><a href="{i["path"]}">{html.escape(i["title"])}</a> <span>{html.escape(i["label"])}</span></li>' for i in items)
    return f'<section class="related-notes" aria-labelledby="{ident}"><h2 id="{ident}">{title}</h2><ul>{lis}</ul></section>'


def main():
    OUT.mkdir(exist_ok=True)
    css = version(OUT / 'library.css')

    # Collect every note first, so pages can link to one another.
    items = []
    for f in FILES:
        t = f.read_text(encoding='utf-8-sig')
        num = f.stem[:2]
        if num not in TOPICS:
            raise SystemExit(f'{f.name}: add a topic for chapter {num} in TOPICS')
        items.append({'path': f.stem + '.html', 'title': t.splitlines()[0].lstrip('# ').strip(), 'kind': 'synthesis',
                      'topic': TOPICS[num], 'number': num, 'raw': t,
                      'label': 'Source catalogue' if num == '07' else 'Synthesis',
                      'cites': sorted(set(SOURCE_LINK.findall(t)))})
    records = (RESEARCH / '07-source-records.md').read_text(encoding='utf-8-sig')
    parts = re.split(r'<a id="s(\d{2})"></a>\s*', records)
    for i in range(1, len(parts), 2):
        num, text = parts[i], parts[i + 1].strip()
        if num not in SOURCE_TOPICS:
            raise SystemExit(f'source S{num}: add a topic in SOURCE_TOPICS')
        title = re.search(r'^### S\d+ — (.+)$', text, re.M).group(1)
        text = re.sub(r'^### S\d+ — (.+)$', r'# \1', text, count=1, flags=re.M)
        items.append({'path': f'source-s{num}.html', 'title': title, 'kind': 'source', 'topic': SOURCE_TOPICS[num],
                      'number': num, 'raw': text, 'label': f'Source note S{num}', 'cites': []})

    by_source = {i['number']: i for i in items if i['kind'] == 'source'}
    cited_by = {n: [] for n in by_source}
    for item in items:
        if item['kind'] == 'synthesis' and item['number'] != '07':
            for n in item['cites']:
                if n not in by_source:
                    raise SystemExit(f'{item["path"]}: cites missing source S{n}')
                cited_by[n].append(item)

    # Pages.
    for idx, item in enumerate(items):
        body, heads = render(item['raw'])
        prev = items[idx - 1] if idx else None
        nxt = items[idx + 1] if idx + 1 < len(items) else None
        meta = (f'<p class="meta">{html.escape(LABELS[item["topic"]])} · {minutes(item["raw"])} min read</p>')
        if item['kind'] == 'source':
            body += ('<p class="note">This dated source note is part of the <a href="07-source-records.html#s' + item['number']
                     + '">complete annotated source catalogue</a>. Read it alongside the '
                     '<a href="06-method-and-questions.html">research method and open questions</a>.</p>')
            body += link_list('Discussed in these chapters', cited_by[item['number']], 'discussed-in')
        elif item['number'] != '07':
            body += link_list('Sources cited in this chapter', [by_source[n] for n in item['cites']], 'sources-cited')
        # Put the meta line and contents list right after the h1.
        h1_end = body.find('</h1>') + len('</h1>')
        body = body[:h1_end] + meta + toc(heads) + body[h1_end:] + pager(prev, nxt)
        (OUT / item['path']).write_text(page(item['title'], body, item['label'], css), encoding='utf-8')

    # Search data first: the catalogue references it with a content hash.
    search = [{'path': i['path'], 'title': i['title'], 'kind': i['kind'], 'topic': i['topic'],
               'text': i['raw'].lower(), 'number': i['number']} for i in items]
    (OUT / 'search-data.js').write_text('window.DUX_SEARCH = ' + json.dumps(search, ensure_ascii=False) + ';\n', encoding='utf-8')

    cards = []
    for order, item in enumerate(items):
        topic = LABELS[item['topic']]
        kind = 'Source note' if item['kind'] == 'source' else item['label']
        cards.append(f'<li data-path="{item["path"]}" data-kind="{item["kind"]}" data-topic="{item["topic"]}" '
                     f'data-order="{order}" data-minutes="{minutes(item["raw"])}" data-title="{html.escape(item["title"].lower())}">'
                     f'<a href="{item["path"]}"><span>{kind} · {html.escape(topic)}</span><strong>{html.escape(item["title"])}</strong>'
                     f'<span>{minutes(item["raw"])} min read →</span></a></li>')
    options = ''.join(f'<option value="{k}">{html.escape(v)}</option>' for k, v in LABELS.items())
    chapters = sum(1 for i in items if i['kind'] == 'synthesis')
    sources = len(items) - chapters
    body = ('<p class="eyebrow">The Project Dux research library</p><h1>Go deeper. <em>Keep the learner in view.</em></h1>'
            '<p class="lead">Explore studies, guidance, learning ideas and the questions they leave open. Search the full text or start with a reading path.</p>'
            f'<p class="note">A targeted collection, not a systematic review. Research snapshot: {SNAPSHOT}. '
            f'{chapters} chapters and {sources} individual source notes. <a href="06-method-and-questions.html">How to read the evidence</a></p>'
            '<div class="reading-paths"><a href="20-literacy-across-ages.html"><span>Start with understanding</span><strong>AI literacy across ages →</strong></a>'
            '<a href="03-learning-and-independence.html"><span>Start with the learner</span><strong>Learning and independence →</strong></a>'
            '<a href="04-children-and-safeguards.html"><span>Start with care</span><strong>Children and safeguards →</strong></a>'
            '<a href="07-source-records.html"><span>Start with evidence</span><strong>Annotated source catalogue →</strong></a></div>'
            '<h2>Find your next question.</h2><div id="controls" hidden><label for="filter">Search titles and full text</label>'
            '<input id="filter" type="search" placeholder="Try feedback, privacy, or adult learning" autocomplete="off">'
            '<div class="filter-row"><label>Type<select id="kind"><option value="all">All types</option>'
            '<option value="synthesis">Research chapters</option><option value="source">Individual source notes</option></select></label>'
            f'<label>Topic<select id="topic"><option value="all">All topics</option>{options}</select></label>'
            '<label>Order<select id="sort"><option value="order">Reading order</option><option value="title">Title, A to Z</option>'
            '<option value="short">Shortest read first</option></select></label>'
            '<button type="button" id="reset">Reset filters</button></div></div>'
            f'<p id="result" role="status">{len(items)} research chapters and source notes</p>'
            '<noscript><p>All notes are listed below. Use your browser’s Find command to search titles.</p></noscript>'
            '<p id="empty" class="note" hidden>No notes match these filters. Try fewer words, or reset the filters.</p>'
            '<ul class="catalog" id="catalog">' + ''.join(cards) + '</ul>'
            f'<script src="{version(OUT / "search-data.js")}" defer></script><script src="{version(OUT / "library.js")}" defer></script>')
    (OUT / 'index.html').write_text(page('Research library', body, 'Catalogue', css), encoding='utf-8')

    # Not-found page. Pages serves it at any missing path, so its links are absolute.
    not_found = page('Page not found',
                     '<h1>This page <em>isn’t here.</em></h1><p class="lead">The address may have changed, or the page may have moved into the research library.</p>'
                     f'<p><a href="{BASE_URL}index.html">Go to the Project Dux homepage</a></p><p><a href="{BASE_URL}library/index.html">Search the research library</a></p>',
                     'Not found', BASE_URL + 'library/' + css)
    not_found = not_found.replace('href="../', f'href="{BASE_URL}').replace('href="index.html"', f'href="{BASE_URL}library/index.html"') \
                         .replace('href="06-method', f'href="{BASE_URL}library/06-method')
    (ROOT / '404.html').write_text(not_found, encoding='utf-8')

    # Stamp the hand-written homepage's own assets.
    for home in (ROOT / 'index.html', ROOT / 'origin.html'):
        text = home.read_text(encoding='utf-8')
        for name in ('styles.css', 'site.js'):
            text = re.sub(r'(["\'])' + re.escape(name) + r'(?:\?v=[0-9a-f]+)?\1', lambda m: m[1] + version(ROOT / name) + m[1], text)
        home.write_text(text, encoding='utf-8')

    print(f'Built {chapters} chapters, {sources} source notes, catalogue and 404 page')


if __name__ == '__main__':
    main()
