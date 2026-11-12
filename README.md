# Project Dux

Project Dux is Voelori’s early-stage exploration of AI in education: learning about AI, using it thoughtfully, and making room for independent thinking. It is a visual draft for discussion, with research and sources to be developed.

[Visit Project Dux](https://dionnedeh.github.io/Project-Dux/)

## What is on the page

| Section | Purpose |
|---|---|
| Learning, with intention | Introduces the project and its central question |
| The exploration | Considers learning about AI, learning with it, and learning without it |
| A thoughtful pause | Offers questions for learners, educators, and families, especially when children are involved |
| Where it began | Shares a reflection by Spencer Hinson from August 13, 2023, and links to a contemporaneous article |

The origin post is archived and visible only to its owner. Its inclusion marks the beginning of the idea; the page is about the broader questions it raises.

## Editorial principles

- Protect curiosity, judgment, and independent learning alongside the exploration of useful AI tools.
- Treat the prompts as starting points for conversation, not universal rules for every learner or classroom.
- Add research with clear sources, context, and limitations. Distinguish historical forecasts from current evidence.
- Keep the page’s draft status clear as its research develops.

## Repository structure

- `index.html` — page content, styles, illustration, and motion control.
- `.github/workflows/pages.yml` — GitHub Actions workflow that publishes the site to GitHub Pages.

The page is static and has no build step or installation dependencies.

## Preview locally

Open `index.html` in a browser, or serve the repository folder:

```sh
python -m http.server 8000
```

Then visit `http://localhost:8000/`.

## Publication and maintenance

GitHub Pages uses the GitHub Actions source. A push to `main` triggers the deployment workflow. Before publishing changes, review the page at desktop and phone widths, try the motion control, check links, and review any new claims against their sources.
