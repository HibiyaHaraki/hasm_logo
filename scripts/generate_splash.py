import argparse
from dataclasses import dataclass
from html import escape
import json
import math
from pathlib import Path
import re
import shutil
import subprocess

import matplotlib
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = Path(__file__).resolve().parent / "splash"
COLOR_REPOSITORY = ROOT / "hasm_color_pattern"
SIZE = (1200, 720)
SUBTITLE = "Human Activity Structure Model"
APPLICATIONS = {
    "hasm": ("HASM", "hasm_logo_transparent.png"),
    "hasm_markdown": ("HASM Markdown", "hasm_markdown_logo_transparent.png"),
}


@dataclass(frozen=True)
class Theme:
    id: str
    text: str
    background: str
    accent: str


def load_themes() -> list[Theme]:
    entry = COLOR_REPOSITORY / "src" / "index.js"
    if not entry.is_file():
        raise FileNotFoundError(
            "Missing color submodule. Run: git submodule update --init"
        )
    # Execute the upstream public API rather than parsing JavaScript as text.
    program = (
        f"import {{ COLOR_PATTERNS }} from {json.dumps(entry.as_uri())};"
        "console.log(JSON.stringify(COLOR_PATTERNS));"
    )
    result = subprocess.run(
        ["node", "--input-type=module", "-e", program],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"Cannot load upstream color patterns:\n{result.stderr}")
    patterns = json.loads(result.stdout)
    if not isinstance(patterns, list) or len(patterns) < 2:
        raise ValueError("The color repository must export at least two patterns")
    themes = []
    for pattern in patterns:
        colors = pattern["colors"]
        theme = Theme(
            pattern["id"], colors["textColor"],
            colors["textBackgroundColor"], colors["mainColor"],
        )
        if not re.fullmatch(r"[a-z0-9-]+", theme.id):
            raise ValueError(f"Invalid theme id: {theme.id!r}")
        for color in (theme.text, theme.background, theme.accent):
            if not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
                raise ValueError(f"Invalid theme color: {color!r}")
        themes.append(theme)
    if len({theme.id for theme in themes}) != len(themes):
        raise ValueError("Duplicate color theme ids")
    return themes


def render_png(logo_path: Path, title: str, theme: Theme, output: Path) -> None:
    canvas = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    with Image.open(logo_path) as source:
        logo = source.convert("RGBA")
    logo.thumbnail((320, 320), Image.Resampling.LANCZOS)
    canvas.alpha_composite(logo, ((SIZE[0] - logo.width) // 2, 72))
    fonts = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    title_font = ImageFont.truetype(str(fonts / "DejaVuSans-Bold.ttf"), 64)
    subtitle_font = ImageFont.truetype(str(fonts / "DejaVuSans.ttf"), 28)
    draw = ImageDraw.Draw(canvas)
    draw.text((600, 463), title, font=title_font, fill=theme.text, anchor="mm")
    draw.text(
        (600, 535), SUBTITLE, font=subtitle_font, fill=theme.text, anchor="mm",
    )
    draw.rounded_rectangle((552, 582, 648, 586), radius=2, fill=theme.accent)
    canvas.save(output)


def generate_splashes(
    output_root: Path = ROOT / "logo", interval: float = 3.0,
) -> list[Path]:
    if not math.isfinite(interval) or not 1 <= interval <= 86400:
        raise ValueError("Theme interval must be between 1 and 86400 seconds")
    themes = load_themes()
    by_id = {theme.id: theme for theme in themes}
    dark_ink = by_id["classic-light"]
    light_ink = by_id["classic"]
    theme_json = json.dumps([
        {"id": theme.id, "text": theme.text, "background": theme.background,
         "accent": theme.accent}
        for theme in themes
    ], indent=2)
    license_text = (COLOR_REPOSITORY / "LICENSE").read_text(encoding="utf-8")
    script = (TEMPLATES / "animation.js").read_text(encoding="utf-8")
    script = f"/* Color palette license:\n{license_text}\n*/\n" + script
    script = script.replace("__THEMES__", theme_json)
    script = script.replace("__INTERVAL_MS__", str(round(interval * 1000)))
    stylesheet = (TEMPLATES / "style.css").read_text(encoding="utf-8")
    stylesheet = stylesheet.replace("__TEXT__", dark_ink.text)
    stylesheet = stylesheet.replace("__ACCENT__", dark_ink.accent)
    html_template = (TEMPLATES / "index.html").read_text(encoding="utf-8")
    outputs = []
    for family, (title, logo_name) in APPLICATIONS.items():
        destination = output_root / family
        destination.mkdir(parents=True, exist_ok=True)
        source = ROOT / "logo" / family / logo_name
        bundled_logo = destination / logo_name
        if source.resolve() != bundled_logo.resolve():
            shutil.copyfile(source, bundled_logo)
        for filename, theme in (
            ("sprash_transparent.png", dark_ink),
            ("sprash_transparent_light.png", light_ink),
        ):
            output = destination / filename
            render_png(source, title, theme, output)
            outputs.append(output)
        document = html_template.replace("__TITLE__", escape(title))
        document = document.replace("__SUBTITLE__", SUBTITLE)
        document = document.replace("__LOGO__", logo_name)
        for filename, content in (
            ("sprash_animation.html", document),
            ("sprash_animation.css", stylesheet),
            ("sprash_animation.js", script),
        ):
            output = destination / filename
            output.write_text(content, encoding="utf-8", newline="\n")
            outputs.append(output)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate transparent splash PNGs and animated Tauri pages."
    )
    parser.add_argument("--interval", type=float, default=3.0,
                        help="Theme change interval in seconds (1..86400; default: 3)")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "logo")
    args = parser.parse_args()
    for path in generate_splashes(args.output_dir, args.interval):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
