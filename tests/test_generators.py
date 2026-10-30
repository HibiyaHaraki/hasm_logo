from pathlib import Path
import py_compile

import matplotlib
import matplotlib.image as mpimg
import pytest

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parents[1]
HASM_OUTPUT_NAMES = (
    "hasm_logo_transparent.png",
    "hasm_logo_dark_bg.png",
    "hasm_logo_light_bg.png",
    "hasm_favicon.png",
)
MARKDOWN_OUTPUT_NAMES = (
    "hasm_markdown_logo_transparent.png",
    "hasm_markdown_logo_dark_bg.png",
    "hasm_markdown_logo_light_bg.png",
    "hasm_markdown_favicon.png",
)


@pytest.mark.parametrize(
    "script_name",
    (
        "scripts/hasm_logo.py",
        "scripts/generate_hasm_logo.py",
        "scripts/generate_hasm_markdown_logo.py",
    ),
)
def test_generator_script_compiles(script_name: str) -> None:
    py_compile.compile(str(ROOT / script_name), doraise=True)


@pytest.mark.parametrize("output_name", HASM_OUTPUT_NAMES + MARKDOWN_OUTPUT_NAMES)
def test_checked_in_logo_output_is_square(output_name: str) -> None:
    output_path = ROOT / "logo" / (
        "hasm_markdown" if output_name.startswith("hasm_markdown") else "hasm"
    ) / output_name
    assert output_path.is_file(), output_path
    image = mpimg.imread(output_path)
    assert image.shape[0] == image.shape[1], output_path
