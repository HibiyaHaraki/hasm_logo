from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon

from hasm_logo import build_logo_geometry, LINE_WIDTH, DPI, PAD_INCHES

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "logo" / "hasm_markdown"

def generate_hasm_markdown_logo_variants():
    t, x, y, colors = build_logo_geometry()

    # --- 2. Calculate Pen Nib Matrix (2D Rotation) ---
    target_idx = int(len(t) * 0.85)
    pen_tip = np.array([x[target_idx], y[target_idx]])

    dx = x[target_idx + 1] - x[target_idx]
    dy = y[target_idx + 1] - y[target_idx]
    angle = np.arctan2(dy, dx)

    cos_a, sin_a = np.cos(angle), np.sin(angle)
    R_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])

    # Base shape for pen nib
    nib_local = np.array([
        [0.00,  0.00],    # Tip
        [0.35,  0.15],    # Upper shoulder
        [0.65,  0.12],    # Upper body
        [0.65, -0.12],    # Lower body
        [0.35, -0.15],    # Lower shoulder
    ])
    nib_world = (nib_local @ R_matrix.T) + pen_tip

    slit_local_end = np.array([0.42, 0.0])
    slit_world_end = (slit_local_end @ R_matrix.T) + pen_tip

    # --- 3. Output Patterns Definition ---
    # ペン先カラーをダーク/ライトともに統一（#161B22 & #8B949E）
    patterns = [
        {
            "filename": "hasm_markdown_logo_transparent.png",
            "bg": "none",
            "guide_alpha": 0.20,
            "nib_bg": "#161B22",
            "nib_edge": "#8B949E",
            "pad": 0
        },
        {
            "filename": "hasm_markdown_logo_dark_bg.png",
            "bg": "#0D1117",
            "guide_alpha": 0.15,
            "nib_bg": "#161B22",
            "nib_edge": "#8B949E",
            "pad": 0.1
        },
        {
            "filename": "hasm_markdown_logo_light_bg.png",
            "bg": "#FFFFFF",
            "guide_alpha": 0.12,
            "nib_bg": "#161B22",  # カラー統一
            "nib_edge": "#8B949E", # カラー統一
            "pad": 0.1
        },
        {
            "filename": "hasm_markdown_favicon.png",
            "bg": "none",
            "guide_alpha": 0.25,
            "nib_bg": "#161B22",
            "nib_edge": "#58A6FF",  # Accent border for high contrast at small scale
            "pad": -0.02
        },
    ]

    print("Generating HASM Markdown Logo Variants...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for p in patterns:
        fig, ax = plt.subplots(figsize=(8, 8), facecolor=p["bg"])
        ax.set_facecolor(p["bg"])

        # Trajectory
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, colors=colors[:-1], linewidths=LINE_WIDTH, antialiased=True)
        ax.add_collection(lc)

        # Guide Lines Motif
        line_color = (0.5, 0.5, 0.55, p["guide_alpha"])
        for y_line in [-0.5, -0.25, 0.0, 0.25, 0.5]:
            ax.plot([-0.6, 0.6], [y_line, y_line], color=line_color, lw=1.2, linestyle=':', zorder=1)

        # Pen Nib
        nib_patch = Polygon(nib_world, closed=True, facecolor=p["nib_bg"], edgecolor=p["nib_edge"], lw=2.2, zorder=10)
        ax.add_patch(nib_patch)

        # Slit & Hole
        ax.plot([pen_tip[0], slit_world_end[0]], [pen_tip[1], slit_world_end[1]], color='#F0F6FC', lw=1.8, zorder=11)
        circle = plt.Circle(slit_world_end, 0.035, color='#F0F6FC', zorder=12)
        ax.add_patch(circle)

        # Canvas bounds
        lim = 1.05 + p["pad"]
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect('equal')
        ax.axis('off')

        plt.tight_layout()
        plt.savefig(
            OUTPUT_DIR / p["filename"],
            dpi=DPI,
            transparent=True,  # すべての画像で背景を透明に指定
            bbox_inches='tight',
            pad_inches=PAD_INCHES,
        )
        plt.close(fig)
        print(f"  └─ Saved: {p['filename']}")

    print("All HASM Markdown logo variants successfully generated!")

if __name__ == "__main__":
    generate_hasm_markdown_logo_variants()