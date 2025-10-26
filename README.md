# document-parser

Small utility that wraps [`docling`](https://github.com/docling-project/docling) to convert documents (PDF/DOCX/etc.) to Markdown and remove repeated images produced by the conversion pipeline.

Install locally:

```bash
pip install .
```

Run the CLI (after installing):

```bash
document-parser -i path/to/input.pdf -o output_dir
```

The CLI maps to the `main()` function in `app.py`. The package installs a `document-parser` console script.

Notes:
- This project depends on heavy packages (e.g., `torch`, `docling`) — install inside a virtualenv.
- `requirements.txt` contains pinned dependency versions used by the project; `pyproject.toml` copies those pins.
