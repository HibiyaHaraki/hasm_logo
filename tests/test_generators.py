from pathlib import Path
import py_compile

import matplotlib
import matplotlib.image as mpimg
import pytest

matplotlib.use("Agg")

from scripts.generate_hasm_logo import generate_hasm_logo_variants
from scripts.generate_hasm_markdown_logo import generate_hasm_markdown_logo_variants


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


def expected_outputs() -> list[Path]:
    return [
        *(ROOT / "logo" / "hasm" / name for name in HASM_OUTPUT_NAMES),
        *(ROOT / "logo" / "hasm_markdown" / name for name in MARKDOWN_OUTPUT_NAMES),
    ]


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


@pytest.mark.parametrize(
    ("generate", "output_names", "relative_output_dir"),
    (
        (generate_hasm_logo_variants, HASM_OUTPUT_NAMES, Path("logo") / "hasm"),
        (
            generate_hasm_markdown_logo_variants,
            MARKDOWN_OUTPUT_NAMES,
            Path("logo") / "hasm_markdown",
        ),
    ),
)
def test_generator_outputs_match_repository_bytes(
    tmp_path: Path,
    generate,
    output_names: tuple[str, ...],
    relative_output_dir: Path,
) -> None:
    output_dir = tmp_path / relative_output_dir
    generate(output_dir)

    for output_name in output_names:
        generated_output = output_dir / output_name
        expected_output = ROOT / relative_output_dir / output_name
        assert generated_output.is_file(), expected_output
        assert generated_output.read_bytes() == expected_output.read_bytes(), expected_output
