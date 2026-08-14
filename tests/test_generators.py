from pathlib import Path
import py_compile
import os
import shutil
import subprocess
import sys

import matplotlib.image as mpimg


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


def test_generator_scripts_compile() -> None:
    for script_name in (
        "scripts/hasm_logo.py",
        "scripts/generate_hasm_logo.py",
        "scripts/generate_hasm_markdown_logo.py",
    ):
        py_compile.compile(str(ROOT / script_name), doraise=True)


def test_checked_in_logo_outputs_are_square() -> None:
    output_paths = expected_outputs()
    assert len(HASM_OUTPUT_NAMES) == len(MARKDOWN_OUTPUT_NAMES) == 4
    assert len(output_paths) == 8
    for output_path in output_paths:
        assert output_path.is_file(), output_path
        image = mpimg.imread(output_path)
        assert image.shape[0] == image.shape[1], output_path


def test_generators_output_all_expected_files_and_match_repository_bytes(tmp_path: Path) -> None:
    temp_scripts = tmp_path / "scripts"
    temp_scripts.mkdir()
    for script_name in (
        "hasm_logo.py",
        "generate_hasm_logo.py",
        "generate_hasm_markdown_logo.py",
    ):
        shutil.copy2(ROOT / "scripts" / script_name, temp_scripts / script_name)

    environment = os.environ.copy()
    environment["MPLBACKEND"] = "Agg"
    for script_name in (
        "generate_hasm_logo.py",
        "generate_hasm_markdown_logo.py",
    ):
        subprocess.run(
            [sys.executable, str(temp_scripts / script_name)],
            check=True,
            env=environment,
            capture_output=True,
            text=True,
        )

    for expected_output in expected_outputs():
        generated_output = tmp_path / expected_output.relative_to(ROOT)
        assert generated_output.is_file(), expected_output
        assert generated_output.read_bytes() == expected_output.read_bytes(), expected_output
