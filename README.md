# HASM Logo

Deterministic mathematical logo generators for the HASM project, anchored to August 14, 2026.

This public repository distributes the HASM logo assets and the scripts used
to generate them. It is maintained as a project resource, not as a community
contribution repository.

## License and usage

The code and generated assets in this repository are released under the
[MIT License](LICENSE). The license permits reuse, including in proprietary
projects, provided that the copyright and license notice are retained.

Pull requests, issues, feature requests, documentation changes, and other
community contributions are not accepted. See [CONTRIBUTING.md](CONTRIBUTING.md)
for the repository policy.

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

## Generate splash screens

Tauri desktop splash windows can display animated HTML/CSS/JavaScript. This
repository generates live, randomly themed HTML rather than an MP4 with a fixed
sequence or platform-dependent video codecs. It also supplies transparent PNGs.
See [the Tauri integration guide](docs/splashscreen.md) for the verified approach,
transparency limitations, and configuration.

The splash generator additionally requires Node.js **22.7+** (24 LTS recommended)
to read the color repository's public JavaScript API.

```powershell
git submodule update --init
python scripts/generate_splash.py
# Optional: change the theme interval (default: 3 seconds)
python scripts/generate_splash.py --interval 5
```

Both `logo/hasm/` and `logo/hasm_markdown/` receive:

- `sprash_transparent.png`: 1200 x 720, transparent, dark text for light surfaces.
- `sprash_transparent_light.png`: transparent, light text for dark surfaces.
- `sprash_animation.html`, `.css`, `.js`: responsive animated splash bundle,
  using the existing transparent logo, the app name, and
  **Human Activity Structure Model**.

The requested `sprash_*` spelling is intentional. Open the HTML directly for a
preview. Its background is transparent by default; append `?background=theme`
to animate the matching theme background as well. Text/accent colors change
every three seconds without consecutive duplicate themes. Reduced-motion
preferences stop animation and theme changes; hidden pages pause theme changes.

`--output-dir PATH` exports both application folders to another directory,
including their existing logo PNG dependencies. The default writes into `logo/`.
Source templates live in `scripts/splash/`; regenerate after editing them.
Generated `sprash_*` files are ignored by Git to keep repository storage small.
Generate them locally before previewing or copying them into an application.

The `hasm_color_pattern` submodule tracks `master`, pinned initially to
`754d8742c2e8db1353bea64e350704424f747130`. To deliberately update the pinned
palette, run `git submodule update --remote hasm_color_pattern`, regenerate the
splashes, review the results, and commit the new submodule pointer. Generated
assets remain local. Ordinary generation never updates or fetches the submodule.

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
