# HASM Logo

Deterministic mathematical logo generators for the HASM project, anchored to August 14, 2026.

## Repository layout

- `scripts/` contains the logo generators.
- `logo/hasm/` stores the core logo outputs.
- `logo/hasm_markdown/` stores Markdown/editor logo variants.
- `docs/` documents the mathematical models.
- `tests/` contains smoke tests.

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## Generate logos

Run from the repository root so generated files are written to the expected location:

```powershell
python scripts/generate_hasm_logo.py
python scripts/generate_hasm_markdown_logo.py
```

The scripts require Python 3.10 or newer, NumPy, and Matplotlib.

Each logo family provides the same four desktop-app-ready variants: transparent,
dark background, light background, and favicon. Tauri can copy the PNGs directly
from `logo/hasm/` and `logo/hasm_markdown/` into its bundled frontend assets.

## Test

```powershell
python -m pytest
```

The command automatically creates an HTML report with each test case, status,
duration, captured output, and failure details at `test-reports/report.html`.
Install the development dependencies first:

```powershell
python -m pip install -e ".[dev]"
```
