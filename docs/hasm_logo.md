# HASM Brand Identity & Mathematical Logo Specification

## Concept: Mathematical Harmony & Structure

The HASM logo is a deterministically generated geometric mandala representing **collaboration, continuity, and structural harmony**. 

Unlike conventional static graphic designs, every curve, frequency, phase shift, and color scaling within this logo is mathematically derived from a single anchor point in time: **August 14, 2026** ($P_1 = 2026, P_2 = 8, P_3 = 14$).

The interplay between the fundamental frequency ($P_2 = 8$) and the harmonic frequency ($P_3 = 14$) forms a **7-fold symmetrical rosette**, symbolizing distinct human activities intertwining seamlessly into a structured whole.

## Mathematical Formulation

### 1. Parametric Trajectory (Coordinates)
The geometric curve is bounded strictly within a $[-1, 1] \times [-1, 1]$ square box:

$$x(t) = \frac{\cos(P_2 t) + \frac{P_2}{P_3} \cos\left(P_3 t + \phi\right)}{1 + \frac{P_2}{P_3}}$$

$$y(t) = \frac{\sin(P_2 t) - \frac{P_2}{P_3} \sin\left(P_3 t + \phi\right)}{1 + \frac{P_2}{P_3}}$$

Where:
* $t \in [0, 2\pi]$
* $\phi = \frac{P_1 \pi}{180} \quad (\text{Phase Shift Angle})$

### 2. Deterministic Color Gradient (Muted Squared Model)
The RGB channels map dynamically to trigonometric frequencies squared to eliminate magic numbers while maintaining a calm, elegant tone visible across light and dark backgrounds:

$$\begin{aligned}
R(t) &= C_{\text{base}} + C_{\text{scale}} \cdot \cos^2\left(P_2 t + \phi\right) \\
G(t) &= C_{\text{base}} + C_{\text{scale}} \cdot \cos^2\left(P_3 t\right) \\
B(t) &= C_{\text{base}} + C_{\text{scale}} \cdot \sin^2\left((P_2 + P_3) t + \phi\right)
\end{aligned}$$

Where the scaling constants are dynamically bounded:
* $C_{\text{base}} = \frac{\min(P_2, P_3)}{(P_1 \bmod (P_2 + P_3)) + \text{sum\_digits}(P_1)} \approx 0.211$
* $C_{\text{scale}} = \frac{P_3 - P_2}{(P_3 - P_2) + \frac{\sqrt{P_1}}{2}} \approx 0.210$

## Asset Guidelines

| File Name | Purpose | Background |
| :--- | :--- | :--- |
| `hasm_logo_transparent.png` | Web / App Header, General Use | Transparent |
| `hasm_logo_dark_bg.png` | Dark Mode Canvas / Pitch Decks | `#0D1117` |
| `hasm_logo_light_bg.png` | Light Mode / Print Documents | `#FFFFFF` |
| `hasm_favicon.png` | Desktop App Icon / Browser Favicon | Transparent (Bold Stroke) |

### Usage Rules
* **Aspect Ratio:** Always maintain a strict 1:1 square aspect ratio.
* **Padding:** Allow at least 10% clear space around the geometry to prevent visual clutter.