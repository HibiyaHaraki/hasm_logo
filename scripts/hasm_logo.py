from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

# --- Configuration Constants ---
P1, P2, P3 = 2026, 8, 14
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[1] / "logo" / "hasm"

LINE_WIDTH = 10.21
DPI = 300
PAD_INCHES = 0.02

LOGO_VARIANTS = (
    {"filename": "hasm_logo_transparent.png", "bg": "none", "pad": 0},
    {"filename": "hasm_logo_dark_bg.png", "bg": "#0D1117", "pad": 0.1},
    {"filename": "hasm_logo_light_bg.png", "bg": "#FFFFFF", "pad": 0.1},
    {"filename": "hasm_favicon.png", "bg": "none", "pad": -0.02},
)


def build_logo_geometry() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    phi = P1 * np.pi / 180.0
    p1_digit_sum = sum(int(digit) for digit in str(P1))
    c_base = min(P2, P3) / ((P1 % (P2 + P3)) + p1_digit_sum)
    c_scale = (P3 - P2) / ((P3 - P2) + (np.sqrt(P1) / 2.0))

    t = np.linspace(0, 2 * np.pi, 2000)
    norm_factor = 1.0 + (P2 / P3)
    x = (np.cos(P2 * t) + (P2 / P3) * np.cos(P3 * t + phi)) / norm_factor
    y = (np.sin(P2 * t) - (P2 / P3) * np.sin(P3 * t + phi)) / norm_factor

    red = c_base + c_scale * (np.cos(P2 * t + phi) ** 2)
    green = c_base + c_scale * (np.cos(P3 * t) ** 2)
    blue = c_base + c_scale * (np.sin((P2 + P3) * t + phi) ** 2)
    colors = np.column_stack((red, green, blue))
    return t, x, y, colors


def render_logo_variant(
    x: np.ndarray,
    y: np.ndarray,
    colors: np.ndarray,
    output_path: Path,
    background: str,
    padding: float,
) -> None:
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    line_collection = LineCollection(
        segments,
        colors=colors[:-1],
        linewidths=LINE_WIDTH,
        antialiased=True,
    )

    figure, axis = plt.subplots(figsize=(8, 8), facecolor=background)
    axis.set_facecolor(background)
    axis.add_collection(line_collection)
    limit = 1.05 + padding
    axis.set_xlim(-limit, limit)
    axis.set_ylim(-limit, limit)
    axis.set_aspect("equal")
    axis.axis("off")
    figure.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        output_path,
        dpi=DPI,
        transparent=True,  # すべての画像で背景を透明に指定
        bbox_inches="tight",
        pad_inches=PAD_INCHES,
    )
    plt.close(figure)


def generate_hasm_logo_variants(output_dir: Path = DEFAULT_OUTPUT_DIR) -> list[Path]:
    print("Generating HASM Logo Variants...")
    _, x, y, colors = build_logo_geometry()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths = []
    for variant in LOGO_VARIANTS:
        output_path = output_dir / variant["filename"]
        render_logo_variant(
            x,
            y,
            colors,
            output_path,
            variant["bg"],
            variant["pad"],
        )
        output_paths.append(output_path)
        print(f"  └─ Saved: {variant['filename']}")

    print("All HASM Logo variants successfully generated!")
    return output_paths


if __name__ == "__main__":
    generate_hasm_logo_variants()