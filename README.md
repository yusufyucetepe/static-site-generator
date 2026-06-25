# Static Site Generator

A Python-based static site generator that converts Markdown content into a fully styled HTML website. Built from scratch with a custom Markdown parser, HTML node tree, and recursive page builder.

## How It Works

1. Static assets (`static/`) are copied into `docs/`
2. Every `.md` file under `content/` is parsed and converted to HTML
3. Each page is rendered using `template.html` and written to the matching path in `docs/`
4. The site is served from `docs/`, which GitHub Pages reads directly

## Project Structure

```
content/        # Markdown source files (mirrors the site structure)
static/         # CSS and images copied as-is to docs/
src/            # Python source: Markdown parser, HTML nodes, page generator
template.html   # Shared HTML shell used for every page
docs/           # Generated output served by GitHub Pages
build.sh        # Build for GitHub Pages (uses /static-site-generator/ basepath)
main.sh         # Build and serve locally at http://localhost:8888
```

## Usage

**Local development**

```bash
bash main.sh
```

Opens a server at `http://localhost:8888`.

**Build for GitHub Pages**

```bash
bash build.sh
```

Generates the site with the correct `/static-site-generator/` basepath, ready to commit and push.

## Adding Content

Create a `.md` file anywhere under `content/` and it will be picked up automatically. The directory structure maps directly to the URL structure of the site.

```
content/blog/my-post/index.md  →  /blog/my-post/
```

## Live Site

[yusufyucetepe.github.io/static-site-generator](https://yusufyucetepe.github.io/static-site-generator)
