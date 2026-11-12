# Project Dux

Project Dux is Voelori’s exploration of AI in education: learning about AI, using it thoughtfully, and making room for independent thinking. Its library is a dated foundation, not a systematic review or a substitute for local educational and safety decisions.

## Research library

The site retains its original introduction, paths, thoughtful-pause questions, origin reflection, leaf illustration, and motion control. It adds a research entry point and links to companion projects with distinct subjects. The library contains eighteen topical chapters and one annotated source catalogue, with a method and explicit gaps. Source notes distinguish experiments from institutional guidance and report access limitations. Original third-party publications are linked, not redistributed.

- `index.html`: homepage and artwork.
- `research/`: maintained Markdown research and source notes.
- `library/`: generated static pages, stylesheet, and browser-local full-text chapter filter.
- `tools/build_library.py`: deterministic library generator, Python standard library only.
- `tools/check_library.py`: local structural and link checks.
- `.github/workflows/pages.yml`: existing Pages workflow; it publishes the repository root on pushes to `main`.

## Preview and validate

```sh
python tools/build_library.py
python tools/check_library.py
python -m http.server 8000
```

Visit `http://localhost:8000/`. Before publication review desktop and mobile layouts, motion controls, library search, source links and the exact research wording. Recheck current laws, product terms and research versions when used. All site files, including research Markdown and tools, would be public through the current root-upload workflow. The library has no accounts, analytics or third-party runtime dependencies.
