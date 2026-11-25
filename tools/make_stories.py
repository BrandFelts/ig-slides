"""Render the newsletter story variants (1080x1920) into stories/story1.png ... storyN.png."""
import pathlib, html
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
AVATAR = ROOT / "assets" / "avatar.jpg"
LINES = [
    "I send out a free newsletter every Monday. Fitness, business and whatever cool sh*t I'm into",
    "Toolkits & Cool Sh*t drops Monday at noon. It's free",
    "If you liked today's post, the newsletter goes deeper. Free every Monday",
    "Fitness, confidence, business, watches, travel. One email a week. Free",
    "Want the stuff I don't post here? It's in the newsletter",
    "Sign up for my newsletter. It's free and it's not boring",
    "Stop scrolling and read something useful. Free newsletter every Monday",
]

def page(text):
    t = html.escape(text)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0}}</style></head><body>
<div style="width:1080px;height:1920px;background:#16181C;font-family:Inter,Arial,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding-top:330px;box-sizing:border-box">
<div style="width:900px;box-sizing:border-box;background:#FFFFFF;color:#0F1419;border-radius:44px;padding:72px 72px 80px;box-shadow:0 30px 80px rgba(0,0,0,.35)">
<div style="display:flex;align-items:center;gap:26px">
<img src="file://{AVATAR}" style="width:110px;height:110px;border-radius:55px;object-fit:cover">
<div style="display:flex;flex-direction:column;gap:6px"><div style="font-size:42px;font-weight:700">Brand Felts</div><div style="font-size:36px;color:#536471">Brand Felts Approach</div></div></div>
<p style="margin:52px 0 0 0;font-size:64px;line-height:1.25;font-weight:700">{t}</p>
</div>
<div style="margin-top:90px;color:#FFFFFF;font-size:52px;font-weight:700;text-align:center">Tap the link to sign up</div>
<div style="margin-top:24px;color:#FFFFFF;font-size:90px;line-height:1">↓</div>
</div></body></html>"""

out = ROOT / "stories"; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    for i, line in enumerate(LINES, 1):
        tmp = out / "_tmp.html"; tmp.write_text(page(line))
        pg.goto("file://" + str(tmp)); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out / f"story{i}.png"))
    tmp.unlink(); b.close()
print(f"{len(LINES)} stories -> {out}")
