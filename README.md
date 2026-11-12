# Project Dux

Project Dux is Voelori’s exploration of AI in education: learning about AI, using it thoughtfully, and making room for independent thinking. Its library is a dated foundation, not a systematic review or a substitute for local educational and safety decisions.

## What is on the site

The homepage keeps its original introduction, paths, thoughtful-pause questions, origin reflection, leaf illustration and motion control. It adds six small explanatory tools, dated research findings, a panel on what the research cannot say yet, further reading and a project timeline, and links to companion projects with distinct subjects.

### The explanatory tools

Each tool opens with a one-line takeaway, works without JavaScript (the page ships a default in its HTML and the controls stay hidden until the script runs), and redraws its result if the browser restores a choice. Nothing typed or chosen is stored or sent. Each carries a badge, defined in a key on the page:

- **Qualitative guide**: questions, prompts and examples, with no figures and no scores.
- **Illustration**: arithmetic on numbers the reader chooses; not an estimate of anything real.
- **Published estimate**: a figure from a cited source, inside that study’s setting. The dated findings use these.

| Tool | Badge | What it does |
|---|---|---|
| What kind of help fits this moment? | Qualitative guide | Six moments (practising for a test, feedback on writing, understanding something hard, brainstorming, checking a fact, a young child exploring), each with what to try, what to keep in mind, and a library link. |
| Keep it, or hand it over? | Qualitative guide | A sorting game: eight requests a learner might type. No score; each card shows one way to see it, and one honestly depends on the purpose. |
| Who does what in a learning moment | Qualitative guide | The parts played by a learner, an educator, a family and an AI tool across five tasks. |
| Before taking on a new AI tool: step by step | Qualitative guide | Seven native disclosures, from naming the learning goal to planning how to stop and report a problem. |
| Percent or points? | Illustration | Two sliders show why a relative difference is not a difference in points. |
| After I used it | Qualitative guide | A private six-question check-in with a short reflection. |

The tools draw on the library and add no new claims. The homepage and every library page carry a Content-Security-Policy that allows only the site’s own scripts, stylesheets and images.

## Research library

The library contains twenty-eight topical chapters, one annotated source catalogue with thirty-four individual source notes, a method and explicit gaps. Source notes distinguish experiments from surveys and institutional guidance, report access limitations, and keep paper versions apart. Original third-party publications are linked, not redistributed. Each page has an “On this page” list where useful, section links, reading time, previous and next links, and links between chapters and the sources they cite. The catalogue has full-text search, type and topic filters, and sorting.

- `index.html`, `styles.css`, `site.js`: the hand-written homepage, its stylesheet and its tools.
- `research/`: maintained Markdown research and source notes.
- `library/`: generated static pages, stylesheet, and browser-local search and filters.
- `404.html`: generated not-found page with absolute links.
- `tools/build_library.py`: deterministic generator, Python standard library only. It also stamps every stylesheet and script link with a content hash (`?v=`), so a deploy never pairs new HTML with an asset a browser cached earlier.
- `tools/check_library.py`: links and anchors, unique IDs, one h1 per page, no inline style or script, current asset versions, sequential source records, the catalogue controls and the homepage tools.
- `.github/workflows/site-check.yml`: rebuilds and checks the site on every pull request and push to `main`, and fails if committed pages differ from a fresh build.
- `.github/workflows/pages.yml`: publishes the repository root to GitHub Pages on pushes to `main`.

## Preview and validate

```sh
python tools/build_library.py
python tools/check_library.py
python -m http.server 8000
```

Visit `http://localhost:8000/`. Before publication review desktop and mobile layouts, motion controls, the homepage tools, library search, source links and the exact research wording. Recheck current laws, product terms and research versions when used. All site files, including research Markdown and tools, would be public through the current root-upload workflow. The library has no accounts, analytics or third-party runtime dependencies.
