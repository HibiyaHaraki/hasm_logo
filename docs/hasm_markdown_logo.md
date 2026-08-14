# HASM Markdown Brand Identity & Logo Specification

## Concept: The Act of Structuring & Writing

The `hasm_markdown` logo represents the **dynamic act of editing, structuring, and capturing activity logs**. 

While retaining the core mathematical identity derived from the inception date (**August 14, 2026**: $P_1 = 2026, P_2 = 8, P_3 = 14$), this logo introduces two distinct visual elements that highlight the context of text editing and documentation:

1. **Fountain Pen Nib / Editor Cursor:** Overlaid directly onto the geometric curve, mathematically aligned via 2D rotation matrix along the trajectory's tangent vector $\left(\frac{dx}{dt}, \frac{dy}{dt}\right)$. This symbolizes human thought continuously drawing and structuring activity into data.
2. **Document Guide Lines:** Subtle dashed background lines reflecting text margins, structured layout, and Markdown syntax formatting.

## Mathematical Alignment & Formulation

### 1. Trajectory Tangent & Pen Nib Orientation
To ensure natural alignment without shape distortion, the pen nib's vertex orientation is determined dynamically using the tangent angle $\theta$ at index $i$ on the trajectory:

$$\theta = \operatorname{atan2}\left(\frac{dy}{dt}, \frac{dx}{dt}\right)$$

Applying the 2D Rotation Matrix $R(\theta)$:

$$R(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$$

The local pen nib vertices $\mathbf{v}_{\text{local}}$ are translated to world coordinates $\mathbf{v}_{\text{world}}$ on the curve tip $\mathbf{p}_{\text{tip}}$:

$$\mathbf{v}_{\text{world}} = \mathbf{v}_{\text{local}} \cdot R(\theta)^T + \mathbf{p}_{\text{tip}}$$

### 2. Embedded Document Motif
Horizontal guide lines are placed at regular intervals $y \in \{-0.5, -0.25, 0.0, 0.25, 0.5\}$ within the bounding box $[-1, 1] \times [-1, 1]$, providing a subtle editor grid background without obscuring the primary artwork.

## ── Asset Guidelines

| File Name | Purpose | Background |
| :--- | :--- | :--- |
| `hasm_markdown_logo_transparent.png` | Primary Repository Logo / App Header | Transparent |
| `hasm_markdown_logo_dark_bg.png` | Dark Mode Pitch Decks / Documentation | `#0D1117` |
| `hasm_markdown_logo_light_bg.png` | Light Mode / Print Documents | `#FFFFFF` |
| `hasm_markdown_favicon.png` | Editor Extension Icon / Browser Favicon | Transparent (Accent Border) |

### Usage Rules
* **Prominence:** The pen nib is enlarged to maintain high visual clarity even at smaller icon sizes (e.g., $16 \times 16$ or $32 \times 32$ favicons).
* **Frame Boundary:** Fits strictly within a 1:1 square aspect ratio aligned with the core `hasm` ecosystem.