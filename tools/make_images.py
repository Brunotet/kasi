#!/usr/bin/env python3
"""Renders the PNG images (logo, social share image, app icon) with a headless browser.
Run once: python3 tools/make_images.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

MARK = ('<svg viewBox="0 0 32 32" width="{s}" height="{s}"><rect x="1.5" y="1.5" width="29" height="29" rx="5" fill="#ffd21f" '
        'stroke="#0d1b3e" stroke-width="3"/><path d="M11 7v18M11 17.5 20 8.5M14.5 14.5 21 25" fill="none" stroke="#0d1b3e" '
        'stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')

FONT = '<style>@font-face{font-family:Archivo;src:url("file://' + str(Path(__file__).resolve().parent.parent / 'assets/fonts/archivo-wdth.woff2') + '") format("woff2");font-weight:100 900;font-stretch:62% 125%}</style>'
BASE = "<style>*{box-sizing:border-box}body{margin:0;font-family:Archivo,Arial,sans-serif}</style>"

LOGO = f"<!doctype html><meta charset=utf-8>{FONT}{BASE}<body style='width:512px;height:512px;background:#ffd21f;display:grid;place-items:center'>{MARK.format(s=380)}</body>"
ICON = f"<!doctype html><meta charset=utf-8>{BASE}<body style='width:180px;height:180px;background:#ffd21f;display:grid;place-items:center'>{MARK.format(s=130)}</body>"
OG = f"""<!doctype html><meta charset=utf-8>{FONT}{BASE}
<body style="width:1200px;height:630px;background:#ffd21f;color:#0d1b3e;position:relative;overflow:hidden">
<div style="position:absolute;left:70px;top:60px;display:flex;align-items:center;gap:18px;font-stretch:62%;font-weight:900;font-size:64px">{MARK.format(s=70)}kasisite</div>
<div style="position:absolute;left:70px;top:175px;width:700px;font-stretch:62%;font-weight:900;text-transform:uppercase;font-size:100px;line-height:.92">Websites that bring customers to your door</div>
<div style="position:absolute;right:60px;top:150px;width:350px;background:#fff;border:6px solid #0d1b3e;border-radius:22px;box-shadow:12px 12px 0 #0d1b3e;padding:56px 28px 28px;transform:rotate(-4deg)">
<div style="position:absolute;top:22px;left:50%;margin-left:-16px;width:32px;height:32px;border:6px solid #0d1b3e;border-radius:50%;background:#ffd21f"></div>
<div style="font-weight:700;font-stretch:85%;font-size:26px">Websites from</div>
<div style="font-stretch:62%;font-weight:900;font-size:104px;line-height:.9;color:#d8382a;white-space:nowrap">R1 499</div></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:70px;background:#1f4fff;border-top:6px solid #0d1b3e;color:#fff;display:flex;align-items:center;padding-left:70px;font-stretch:70%;font-weight:800;font-size:34px;text-transform:uppercase">Fast, fixed-price websites for South African businesses</div>
</body>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, html, w, h in [("logo.png", LOGO, 512, 512), ("apple-touch-icon.png", ICON, 180, 180), ("og.png", OG, 1200, 630)]:
        pg = b.new_page(viewport={"width": w, "height": h})
        tmp = OUT.parent.parent / "tools" / f"_tmp_{name}.html"
        tmp.write_text(html, encoding="utf-8")
        pg.goto(tmp.as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(600)
        pg.screenshot(path=str(OUT / name))
        pg.close()
        tmp.unlink()
        print("wrote", OUT / name)
    b.close()
