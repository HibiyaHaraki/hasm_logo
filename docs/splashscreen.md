# Animated splash screens for Tauri 2

## Feasibility

Animation is supported in a **desktop WebView splash window**. The official
[Tauri splashscreen guide](https://v2.tauri.app/learn/splashscreen/) implements
the splash as a separate window serving HTML, with the main window initially
hidden. That HTML can use CSS animations and JavaScript timers just like the
main frontend.

This is not animation inside a native OS launch image, and does not cover the
native Android/iOS launch screen or the period before the WebView exists.
No Tauri application is included in this asset repository: browser rendering and
timer behavior are tested here, but native window integration must be tested
in the consuming application.

Runtime HTML is preferable to a video here: it can choose new random themes
on every run, needs no video decoding or autoplay permissions, and preserves
transparency without special video codecs. The logo geometry stays unchanged.
Text, loading dots, and optional background use matching color tokens from
the pinned color submodule's `COLOR_PATTERNS` API.

## Generate and preview

From the repository root, after installing the Python development dependencies
and Node.js 22.7 or newer:

```powershell
git submodule update --init
python scripts/generate_splash.py
Start-Process ".\logo\hasm\sprash_animation.html"
Start-Process ".\logo\hasm_markdown\sprash_animation.html"
```

Both pages start with `classic-light` and then select another palette every
three seconds, using a 600 ms color transition. Configure the interval with
`--interval` (1 to 86400 seconds). A page with reduced motion enabled stays on
its current theme; changes resume when that preference is disabled. Hidden
pages pause the timer. The loading dots are decorative and not a progress meter.

The default background is transparent. To animate opaque background colors too,
open `sprash_animation.html?background=theme`. This uses each palette's
`textBackgroundColor` alongside its `textColor`. On a transparent page the
underlying surface is outside the page's control; use the themed-background
mode when contrast must be guaranteed as light and dark themes alternate.

Static alternatives are `sprash_transparent.png` (dark text) and
`sprash_transparent_light.png` (light text). Both are RGBA PNGs with a 1200 x 720
canvas and contain the original app logo, **HASM** or **HASM Markdown**, and
**Human Activity Structure Model**. PNG text uses Matplotlib's bundled DejaVu
Sans; HTML uses the platform's system sans-serif font. No remote font is loaded.

## Integrate into a desktop app

1. Copy the chosen application's `sprash_animation.html`,
   `sprash_animation.css`, `sprash_animation.js`, and original
   `hasm_logo_transparent.png` or `hasm_markdown_logo_transparent.png` into one
   directory in your frontend's static/public assets. For example, make them
   available at `splash/` in both the development server and the built frontend.
   The color license notice is embedded in the generated JavaScript; retain it.
2. Merge these window definitions into `app.windows` in your Tauri 2
   configuration, preserving any other application settings:

   ```json
   {
     "app": {
       "windows": [
         {
           "label": "main",
           "visible": false
         },
         {
           "label": "splashscreen",
           "url": "splash/sprash_animation.html",
           "width": 900,
           "height": 540,
           "center": true,
           "decorations": false,
           "resizable": false,
           "transparent": true,
           "backgroundColor": "#00000000"
         }
       ]
     }
   }
   ```

   For an opaque theme-coordinated window, use
   `"url": "splash/sprash_animation.html?background=theme"` and remove
   `transparent` / `backgroundColor`. An opaque window is also a fallback on
   platforms where transparent windows are unavailable.
3. Keep expensive initialization off the UI/event-loop thread so animation
   can run. When real initialization completes, close `splashscreen` and show
   `main` from Rust using `tauri::Manager`, as in the official guide. Do not
   use the color timer as an application-readiness timer. Report initialization
   failures explicitly instead of leaving the splash open forever.
4. Include the files in the actual frontend build, not only Tauri's
   `bundle.resources`. No network requests or inline scripts/styles are needed.
   Preserve the app's existing CSP and allow these local scripts, styles, and
   images under its `script-src`, `style-src`, and `img-src` directives.
5. Test the packaged app, including its initial background, native transparency,
   startup errors, actual readiness handoff, and reduced-motion behavior.

HTML transparency alone does not make the native window transparent. The
[Tauri window transparency API](https://docs.rs/tauri/latest/tauri/webview/struct.WebviewWindowBuilder.html#method.transparent)
documents platform restrictions. On macOS, transparency requires the
`macos-private-api` Cargo feature and `app.macOSPrivateApi`; that private API
prevents Mac App Store acceptance. Use the opaque variant for that distribution.
