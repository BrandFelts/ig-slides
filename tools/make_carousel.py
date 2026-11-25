"""Render one tweet-style Instagram carousel to PNGs.

Usage: python3 tools/make_carousel.py spec.json
spec.json: {"folder": "2026-11-30-morning", "slides": ["hook text", "slide 2", ...]}
The first slide is the hook (bold, with "Swipe ->"). A newsletter CTA slide is added last.
Output: <repo>/<folder>/slide1.png ... slideN.png (1080x1350).
"""
import json, sys, pathlib, html
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
AVATAR = ROOT / "assets" / "avatar.jpg"
FULL = ROOT / "assets" / "full.jpg"
NAME, HANDLE = "Brand Felts", "Brand Felts Approach"
BG, INK, MUTED, FRAME = "#FFFFFF", "#0F1419", "#536471", "#16181C"

HEAD = f"""<div style="display:flex;align-items:center;gap:28px">
<img src="file://{AVATAR}" style="width:120px;height:120px;border-radius:60px;object-fit:cover">
<div style="display:flex;flex-direction:column;gap:6px">
<div style="font-size:44px;font-weight:700">{NAME}</div>
<div style="font-size:38px;color:{MUTED}">{HANDLE}</div></div></div>"""

def frame(inner):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0}}</style></head><body>
<div style="width:1080px;height:1350px;background:{FRAME};display:flex;align-items:center;justify-content:center;overflow:hidden">
<div style="width:1080px;height:1350px;flex-shrink:0;transform:scale(0.86);border-radius:44px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.35)">
{inner}</div></div></body></html>"""

def text_slide(text, i, n, hook):
    t = html.escape(text).replace("\n", "<br>")
    size, weight = (84, 700) if hook else (66, 400)
    if hook and len(text) > 90: size = 70
    left = "<span>Swipe →</span>" if hook else "<span></span>"
    return frame(f"""<div style="width:1080px;height:1350px;box-sizing:border-box;padding:110px 100px;background:{BG};color:{INK};font-family:Inter,Arial,sans-serif;display:flex;flex-direction:column;justify-content:center;position:relative">
{HEAD}
<p style="margin:56px 0 0 0;font-size:{size}px;line-height:1.25;font-weight:{weight}">{t}</p>
<div style="position:absolute;left:100px;right:100px;bottom:80px;display:flex;justify-content:space-between;font-size:32px;color:{MUTED}">{left}<span>{i} / {n}</span></div></div>""")

def cta_slide(i, n):
    return frame(f"""<div style="width:1080px;height:1350px;background:{BG};color:{INK};font-family:Inter,Arial,sans-serif;display:flex">
<div style="width:560px;height:1350px;box-sizing:border-box;padding:110px 56px 80px 90px;display:flex;flex-direction:column;justify-content:center;position:relative">
<div style="display:flex;align-items:center;gap:22px">
<img src="file://{AVATAR}" style="width:100px;height:100px;border-radius:50px;object-fit:cover">
<div style="display:flex;flex-direction:column;gap:4px"><div style="font-size:36px;font-weight:700">{NAME}</div><div style="font-size:30px;color:{MUTED}">{HANDLE}</div></div></div>
<p style="margin:56px 0 0 0;font-size:64px;line-height:1.15;font-weight:700">Want more?</p>
<p style="margin:36px 0 0 0;font-size:40px;line-height:1.35">I send out a free newsletter every Monday called Toolkits &amp; Cool Sh*t. Fitness, business, growth and whatever cool sh*t I'm into</p>
<div style="margin-top:56px;align-self:flex-start;background:{INK};color:{BG};border-radius:999px;padding:26px 44px;font-size:36px;font-weight:700">Sign up free, link in bio</div>
<div style="position:absolute;left:90px;bottom:80px;font-size:32px;color:{MUTED}">{i} / {n}</div></div>
<div style="width:520px;height:1350px;box-sizing:border-box;padding:40px 40px 40px 0">
<img src="file://{FULL}" style="width:480px;height:1270px;border-radius:32px;object-fit:cover;display:block"></div></div>""")

spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
out = ROOT / spec["folder"]; out.mkdir(parents=True, exist_ok=True)
slides = spec["slides"]; n = len(slides) + 1
pages = [text_slide(s, i + 1, n, i == 0) for i, s in enumerate(slides)] + [cta_slide(n, n)]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, h in enumerate(pages, 1):
        tmp = out / "_tmp.html"; tmp.write_text(h)
        pg.goto("file://" + str(tmp)); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out / f"slide{i}.png"))
    tmp.unlink(); b.close()
print(f"{n} slides -> {out}")
