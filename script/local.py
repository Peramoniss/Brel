from pathlib import Path
from deep_translator import GoogleTranslator
from tqdm import tqdm
import argparse
from langdetect import detect
import time
import os

parser = argparse.ArgumentParser()

# 1. Aceita o valor logo após o nome do script (nargs='?' significa que é opcional)
parser.add_argument("pos_src", nargs="?", help="Input file name (inserted right after the code running)")
parser.add_argument("--src", help="Input file name (inserted with --src)")

parser.add_argument("--out", default="html/translated_song.html", help="Output file name")

parser.add_argument("--lang", default="en", help="Translated language. Ex: en (default), pt, es, fr, it, etc")

parser.add_argument("--strat", default="verse", help="Translation strategy. Can translate by verse, stanza, or the entire song as a whole. Options are verse (default), stanza, whole.")

parser.add_argument("--title", help="The title of the song.")

parser.add_argument("--open", default='True', help="Determine whether the program should open the HTML file in the end. True by default.")

args = parser.parse_args()

if args.pos_src != "" or args.src:
    INPUT_FILE = args.pos_src if args.pos_src else args.src
    OUTPUT_FILE = args.out
    TARGET_LANG = args.lang
    OPEN = True if args.open == "True" else False
    SONG_TITLE = args.title if args.title else INPUT_FILE
else:
    raise Exception("Please provide the input file. Use --help for more information.")

if (args.strat == "verse" or args.strat == "stanza" or args.strat == "whole"):
    STRATEGY = args.strat
else:
    raise Exception("Please provide a valid strategy. Use --help for more information.")

# -----------------------------
# Read input
# -----------------------------
lyrics = Path(INPUT_FILE).read_text(encoding="utf-8")

# -----------------------------
# Translator (auto-detect source)
# -----------------------------
src_lang = detect(lyrics)
translator = GoogleTranslator(
    source=src_lang,
    target=TARGET_LANG
)

def translate(text: str) -> str:
    if not text.strip():
        return ""
    try:
        return translator.translate(text)
    except Exception as e:
        # fallback: keep original if translation fails
        return text

# -----------------------------
# Translate lines
# -----------------------------
rows = []
if STRATEGY == "verse":
    for line in tqdm(lyrics.splitlines(), unit='verses', desc='Translating...'):
        translated = translate(line)
        rows.append((line, translated))
elif STRATEGY == "stanza":
    for stanza in tqdm(lyrics.split("\n\n"), unit='stanzas', desc='Translating...'):
        translated_stanza = translate(stanza)
        for line, translated in zip(stanza.splitlines(), translated_stanza.splitlines()):
            rows.append((line, translated))
        rows.append(("", ""))
elif STRATEGY == "whole":
    translated_lyrics = translate(lyrics)
    for line, translated in zip(lyrics.splitlines(), translated_lyrics.splitlines()):
        rows.append((line, translated))

# -----------------------------
# Build HTML
# -----------------------------
CSS = """
:root {
    --font-family: Georgia, 'Times New Roman', serif;
    --font-size: 21px;
    --line-height: 1.8;

    --bg: #faf8f3;
    --text: #20261f;
    --muted: #8a8f7d;
    --accent: #3f6b52;          /* softer, muted green for translated lines */
    --divider: #ddd7c5;
    --stripe: rgba(63, 107, 82, 0.07);   /* faint band, interleaved mode only */
    --panel-bg: rgba(255, 255, 255, 0.9);
    --panel-border: #e4dfd0;
    --control-text: #4d5347;
    --input-bg: #fff;
    --input-border: #cfc9b6;
}

[data-theme="dark"] {
    --bg: #1c1e1a;
    --text: #e7e5dd;
    --muted: #8d9286;
    --accent: #8fbfa1;          /* desaturated mint, legible on dark bg */
    --divider: #3a3d35;
    --stripe: rgba(143, 191, 161, 0.08);
    --panel-bg: rgba(34, 36, 31, 0.88);
    --panel-border: #3a3d35;
    --control-text: #c7cbbf;
    --input-bg: #2a2c26;
    --input-border: #454841;
}

* { box-sizing: border-box; }

body {
    font-family: var(--font-family);
    font-size: var(--font-size);
    line-height: var(--line-height);
    max-width: 1080px;
    margin: 0 auto;
    padding: 32px 20px 80px;
    background: var(--bg);
    color: var(--text);
    transition: background 0.2s ease, color 0.2s ease;
}

h1 {
    text-align: center;
    font-size: 1.8em;
    margin: 0 0 2px;
    color: var(--text);
    letter-spacing: 0.01em;
}

.subtitle {
    text-align: center;
    font-family: Arial, sans-serif;
    font-size: 13px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 28px;
}

/* ---------- controls ---------- */

.controls {
    position: sticky;
    top: 12px;
    z-index: 10;
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    align-items: center;
    justify-content: center;
    background: var(--panel-bg);
    backdrop-filter: blur(8px);
    border: 1px solid var(--panel-border);
    border-radius: 14px;
    padding: 12px 20px;
    margin-bottom: 36px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
    font-family: Arial, sans-serif;
    font-size: 13px;
    transition: background 0.2s ease, border-color 0.2s ease;
}

.control-group {
    display: flex;
    align-items: center;
    gap: 8px;
}

.control-group label {
    color: var(--control-text);
    font-weight: 600;
}

select {
    font-family: Arial, sans-serif;
    font-size: 13px;
    padding: 6px 10px;
    border-radius: 8px;
    border: 1px solid var(--input-border);
    background: var(--input-bg);
    color: var(--text);
    cursor: pointer;
}

.size-control { gap: 6px; }

.step-btn, .icon-btn {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    border: 1px solid var(--input-border);
    background: var(--input-bg);
    font-size: 14px;
    line-height: 1;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text);
}

.step-btn:hover, .icon-btn:hover { background: var(--stripe); }

input[type="range"] {
    width: 110px;
    accent-color: var(--accent);
}

#size-label {
    min-width: 38px;
    text-align: center;
    color: var(--control-text);
    font-variant-numeric: tabular-nums;
}

#layout-toggle {
    font-family: Arial, sans-serif;
    font-size: 13px;
    font-weight: 700;
    padding: 8px 18px;
    border-radius: 9px;
    border: none;
    background: var(--accent);
    color: #fff;
    cursor: pointer;
    transition: opacity 0.15s ease;
}

#layout-toggle:hover { opacity: 0.85; }
#layout-toggle:active { transform: translateY(1px); }

/* ---------- lyrics ---------- */

.lyrics { margin-top: 8px; }

.original {
    white-space: pre-wrap;
    color: var(--text);
}

.translated {
    white-space: pre-wrap;
    color: var(--accent);
}

/* translation style variants — chosen via the "Translation style" control.
   Color is always applied above; these add an optional second cue. */
[data-translation-style="caps"] .translated {
    font-variant: small-caps;
    letter-spacing: 0.03em;
}

[data-translation-style="light"] .translated {
    font-weight: 300;
}

[data-translation-style="small"] .translated {
    font-size: 0.85em;
}

[data-translation-style="italic"] .translated {
    font-style: italic;
}

[data-translation-style="bold"] .translated {
    font-weight: 700;
}

.blank { height: 25px; }

/* side-by-side: two plain columns, single vertical rule, no per-row blocks
   or alternating colors — just clean, even typography */
.lyrics.side-by-side .row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    padding: 4px 0;
    border-radius: 6px;
    transition: background 0.15s ease;
}

.lyrics.side-by-side .row:hover {
    background: var(--stripe);
}

.lyrics.side-by-side .translated {
    padding-left: 32px;
    border-left: 1px solid var(--divider);
}

/* interleaved: original above its translation, each couplet getting a
   faint alternating band so the eye can track pairs — this is the only
   mode with alternating color */
.lyrics.interleaved .row {
    display: block;
    padding: 9px 14px;
    margin: 0 -14px 2px;
    border-radius: 6px;
    transition: background 0.15s ease;
}

.lyrics.interleaved .row:nth-of-type(even) {
    background: var(--stripe);
}

.lyrics.interleaved .original,
.lyrics.interleaved .translated {
    display: block;
}

.lyrics.interleaved .translated {
    margin-top: 2px;
}

@media (max-width: 640px) {
    .lyrics.side-by-side .row {
        grid-template-columns: 1fr;
        gap: 2px;
    }
    .lyrics.side-by-side .translated {
        border-left: none;
        padding-left: 0;
        padding-top: 4px;
        font-size: 0.92em;
    }
    .controls { gap: 10px; padding: 10px 14px; }
}
"""

CONTROLS_HTML = """
<div class="controls">
    <div class="control-group">
        <label for="font-select">Font</label>
        <select id="font-select">
            <option value="Georgia, 'Times New Roman', serif" selected>Georgia</option>
            <option value="Arial, Helvetica, sans-serif">Arial</option>
            <option value="Verdana, Geneva, sans-serif">Verdana</option>
            <option value="Tahoma, Geneva, sans-serif">Tahoma</option>
            <option value="'Trebuchet MS', sans-serif">Trebuchet MS</option>
            <option value="'Times New Roman', Times, serif">Times New Roman</option>
            <option value="'Courier New', Courier, monospace">Courier New</option>
            <option value="'Comic Sans MS', cursive, sans-serif">Comic Sans MS</option>
        </select>
    </div>

    <div class="control-group">
        <label for="translation-style">Translation</label>
        <select id="translation-style">
            <option value="" selected>Color only</option>
            <option value="caps">Small caps</option>
            <option value="light">Lighter weight</option>
            <option value="small">Smaller size</option>
            <option value="italic">Italic</option>
            <option value="bold">Bold</option>
        </select>
    </div>

    <div class="control-group size-control">
        <label for="size-slider">Size</label>
        <button type="button" class="step-btn" id="size-down" aria-label="Decrease font size">&minus;</button>
        <input type="range" id="size-slider" min="13" max="32" value="21" step="1">
        <button type="button" class="step-btn" id="size-up" aria-label="Increase font size">+</button>
        <span id="size-label">21px</span>
    </div>

    <button type="button" id="layout-toggle">&#8644; Interleave Lines</button>

    <button type="button" class="icon-btn" id="theme-toggle" aria-label="Switch to dark mode">&#127769;</button>
</div>
"""

SCRIPT_JS = """
(function () {
    var layoutBtn = document.getElementById('layout-toggle');
    var lyricsEl = document.getElementById('lyrics');
    var fontSelect = document.getElementById('font-select');
    var translationStyleSelect = document.getElementById('translation-style');
    var sizeSlider = document.getElementById('size-slider');
    var sizeLabel = document.getElementById('size-label');
    var sizeDown = document.getElementById('size-down');
    var sizeUp = document.getElementById('size-up');
    var themeToggle = document.getElementById('theme-toggle');
    var root = document.documentElement;

    var interleaved = false;
    var dark = false;

    layoutBtn.addEventListener('click', function () {
        interleaved = !interleaved;
        lyricsEl.classList.toggle('interleaved', interleaved);
        lyricsEl.classList.toggle('side-by-side', !interleaved);
        layoutBtn.innerHTML = interleaved ? '&#8644; Side by Side' : '&#8644; Interleave Lines';
    });

    themeToggle.addEventListener('click', function () {
        dark = !dark;
        if (dark) {
            root.setAttribute('data-theme', 'dark');
            themeToggle.innerHTML = '&#9728;';
            themeToggle.setAttribute('aria-label', 'Switch to light mode');
        } else {
            root.removeAttribute('data-theme');
            themeToggle.innerHTML = '&#127769;';
            themeToggle.setAttribute('aria-label', 'Switch to dark mode');
        }
    });

    fontSelect.addEventListener('change', function () {
        root.style.setProperty('--font-family', fontSelect.value);
    });

    translationStyleSelect.addEventListener('change', function () {
        var v = translationStyleSelect.value;
        if (v) {
            root.setAttribute('data-translation-style', v);
        } else {
            root.removeAttribute('data-translation-style');
        }
    });

    function setSize(px) {
        px = Math.min(32, Math.max(13, px));
        root.style.setProperty('--font-size', px + 'px');
        sizeSlider.value = px;
        sizeLabel.textContent = px + 'px';
    }

    sizeSlider.addEventListener('input', function () {
        setSize(parseInt(sizeSlider.value, 10));
    });

    sizeDown.addEventListener('click', function () {
        setSize(parseInt(sizeSlider.value, 10) - 1);
    });

    sizeUp.addEventListener('click', function () {
        setSize(parseInt(sizeSlider.value, 10) + 1);
    });
})();
"""


def build_lyrics_html(song_title, rows):
    """
    song_title: string, used in <title> and the subtitle under the heading
    rows: list of (original, translated) tuples
    """
    parts = []

    parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Translated Lyrics for {song_title}</title>
<style>
{CSS}
</style>
</head>
<body>

<h1>{song_title}</h1>
<div class="subtitle">Translated from {src_lang} to {TARGET_LANG}</div>
{CONTROLS_HTML}
<div id="lyrics" class="lyrics side-by-side">
""")

    for original, translated in rows:
        if not original.strip():
            parts.append('<div class="blank"></div>\n')
            continue

        parts.append(f"""
    <div class="row">
        <div class="original">{original}</div>
        <div class="translated">{translated}</div>
    </div>
""")

    parts.append(f"""
</div>

<script>
{SCRIPT_JS}
</script>

</body>
</html>
""")

    return "".join(parts)

html = build_lyrics_html(SONG_TITLE, rows)

output_path = Path(OUTPUT_FILE).resolve()
output_path.write_text(html, encoding="utf-8")

print(f"Saved: {output_path}")

if OPEN:
    time.sleep(1)

    if os.name == "posix":  # macOS / Linux
        if "darwin" in os.sys.platform:
            subprocess.run(["open", str(output_path)])
        else:
            subprocess.run(["xdg-open", str(output_path)])
    else:  # Windows
        os.startfile(output_path)