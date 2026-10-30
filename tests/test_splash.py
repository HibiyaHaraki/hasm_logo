import json
from pathlib import Path
import subprocess

from PIL import Image
import pytest

from scripts import generate_splash as splash


@pytest.fixture(scope="module")
def generated(tmp_path_factory: pytest.TempPathFactory) -> Path:
    output = tmp_path_factory.mktemp("splash")
    splash.generate_splashes(output)
    return output


def test_upstream_themes() -> None:
    themes = splash.load_themes()
    assert len(themes) == 24
    by_id = {theme.id: theme for theme in themes}
    assert by_id["classic"].text == "#f8fafc"
    assert by_id["classic-light"].text == "#0f172a"


@pytest.mark.parametrize("family", splash.APPLICATIONS)
@pytest.mark.parametrize(
    "filename", ("sprash_transparent.png", "sprash_transparent_light.png"),
)
def test_transparent_png(generated: Path, family: str, filename: str) -> None:
    path = generated / family / filename
    with Image.open(path) as image:
        assert image.mode == "RGBA"
        assert image.size == (1200, 720)
        assert image.getpixel((0, 0))[3] == 0
        assert image.getpixel((1199, 719))[3] == 0
        alpha = image.getchannel("A")
        # Logo, application name, and full model name must all be visible.
        for box in ((440, 72, 760, 392), (100, 420, 1100, 505),
                    (100, 510, 1100, 565)):
            assert alpha.crop(box).getbbox() is not None
        left, top, right, bottom = alpha.getbbox()
        assert left > 20 and top > 20 and right < 1180 and bottom < 700


@pytest.mark.parametrize("family", splash.APPLICATIONS)
def test_generated_bundle(generated: Path, family: str) -> None:
    title, logo = splash.APPLICATIONS[family]
    directory = generated / family
    document = (directory / "sprash_animation.html").read_text(encoding="utf-8")
    assert f"<h1>{title}</h1>" in document
    assert "Human Activity Structure Model" in document
    assert f'src="{logo}"' in document
    assert (directory / logo).read_bytes() == (
        splash.ROOT / "logo" / family / logo
    ).read_bytes()
    for filename in ("sprash_animation.css", "sprash_animation.js"):
        assert filename in document
        assert "__" not in (directory / filename).read_text(encoding="utf-8")


def test_splash_generation_is_reproducible(generated: Path, tmp_path: Path) -> None:
    splash.generate_splashes(tmp_path)
    for family in splash.APPLICATIONS:
        for path in (generated / family).glob("sprash_*"):
            assert path.read_bytes() == (tmp_path / family / path.name).read_bytes()


@pytest.mark.parametrize("interval", (0, -1, 0.9, float("nan"), float("inf"), 86401))
def test_invalid_interval(tmp_path: Path, interval: float) -> None:
    with pytest.raises(ValueError, match="interval"):
        splash.generate_splashes(tmp_path, interval)
    assert not list(tmp_path.iterdir())


def test_missing_submodule(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(splash, "COLOR_REPOSITORY", tmp_path)
    with pytest.raises(FileNotFoundError, match="git submodule update --init"):
        splash.load_themes()


@pytest.mark.parametrize("background", ("", "?background=theme"))
@pytest.mark.parametrize("reduced", (False, True))
def test_animation_runtime(generated: Path, background: str, reduced: bool) -> None:
    script = generated / "hasm" / "sprash_animation.js"
    # A virtual clock verifies timing and media changes without waiting in real time.
    program = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const assert = require("node:assert/strict");
const values = {};
const events = {};
const media = { matches: REDUCED, addEventListener: (_, fn) => events.media = fn };
const root = { dataset: {}, style: { setProperty: (k, v) => values[k] = v } };
const document = {
  documentElement: root, hidden: false,
  addEventListener: (key, fn) => events[key] = fn
};
let tick;
let delay;
const context = {
  document, location: { search: BACKGROUND }, URLSearchParams, Math,
  matchMedia: () => media,
  addEventListener: (key, fn) => events[key] = fn,
  setInterval: (fn, ms) => { tick = fn; delay = ms; return 1; },
  clearInterval: () => { tick = undefined; }
};
vm.runInNewContext(fs.readFileSync(SCRIPT, "utf8"), context);
assert.equal(root.dataset.theme, "classic-light");
assert.equal(values["--splash-text"], "#0f172a");
assert.equal(values["--splash-background"],
  BACKGROUND ? "#f8fafc" : "transparent");
if (REDUCED) {
  assert.equal(tick, undefined);
  media.matches = false;
  events.media();
}
assert.equal(delay, 3000);
const expected = EXPECTED;
for (let i = 0; i < 200; i++) {
  const previous = root.dataset.theme;
  tick();
  assert.notEqual(root.dataset.theme, previous);
  const theme = expected.find(t => t.id === root.dataset.theme);
  assert.ok(theme);
  assert.equal(values["--splash-text"], theme.text);
  assert.equal(values["--splash-accent"], theme.accent);
  assert.equal(values["--splash-background"],
    BACKGROUND ? theme.background : "transparent");
}
document.hidden = true;
events.visibilitychange();
assert.equal(tick, undefined);
document.hidden = false;
events.visibilitychange();
assert.equal(typeof tick, "function");
media.matches = true;
events.media();
assert.equal(tick, undefined);
media.matches = false;
events.media();
events.pagehide();
assert.equal(tick, undefined);
events.pageshow();
assert.equal(typeof tick, "function");
"""
    expected = [
        {"id": theme.id, "text": theme.text, "background": theme.background,
         "accent": theme.accent}
        for theme in splash.load_themes()
    ]
    program = (
        program.replace("REDUCED", json.dumps(reduced))
        .replace("BACKGROUND", json.dumps(background))
        .replace("SCRIPT", json.dumps(str(script)))
        .replace("EXPECTED", json.dumps(expected))
    )
    result = subprocess.run(
        ["node", "-e", program], capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
