"""Render the newsletter story variants (1080x1920) into stories/story1.png ... storyN.png.
Each story: a photo of Brand on top, the tweet-style card overlapping it, then the sign-up prompt.
The bottom area is left clear for Instagram's link sticker."""
import pathlib, html
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
AVATAR = ROOT / "assets" / "avatar.jpg"
P = ROOT / "assets" / "photos"
# (line, photo, object-position focusing on Brand)
STORIES = [
    ("I send out a free newsletter every Monday. Fitness, business and whatever cool shit I'm into", "mirror.jpg", "50% 22%"),
    ("Toolkits & Cool Shit drops Monday at noon. It's free", "yard.jpg", "32% 40%"),
    ("If you liked today's post, the newsletter goes deeper. Free every Monday", "gymfull.jpg", "50% 42%"),
    ("Fitness, confidence, business, watches, travel. One email a week. Free", "dinner.jpg", "50% 40%"),
    ("Want the stuff I don't post here? It's in the newsletter", "festival.jpg", "50% 30%"),
    ("Sign up for my newsletter. It's free and it's not boring", "mirror.jpg", "50% 30%"),
    ("Stop scrolling and read something useful. Free newsletter every Monday", "gymfull.jpg", "50% 30%"),
]

def page(text, photo, pos):
    t = html.escape(text)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0}}</style></head><body>
<div style="width:1080px;height:1920px;background:#16181C;font-family:Inter,Arial,sans-serif;position:relative;overflow:hidden">
<img src="file://{P / photo}" style="position:absolute;left:0;top:0;width:1080px;height:1180px;object-fit:cover;object-position:{pos}">
<div style="position:absolute;left:90px;top:1000px;width:900px;box-sizing:border-box;background:#FFFFFF;color:#0F1419;border-radius:40px;padding:52px 60px 58px;box-shadow:0 24px 70px rgba(0,0,0,.45)">
<div style="display:flex;align-items:center;gap:22px">
<img src="file://{AVATAR}" style="width:92px;height:92px;border-radius:46px;object-fit:cover">
<div style="display:flex;flex-direction:column;gap:4px"><div style="font-size:36px;font-weight:700">Brand Felts</div><div style="font-size:31px;color:#536471">Brand Felts Approach</div></div></div>
<p style="margin:34px 0 0 0;font-size:50px;line-height:1.25;font-weight:700">{t}</p>
</div>
<div style="position:absolute;left:0;right:0;top:1560px;text-align:center;color:#FFFFFF;font-size:46px;font-weight:700">Tap the link to sign up ↓</div>
</div></body></html>"""

out = ROOT / "stories"; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    for i, (line, photo, pos) in enumerate(STORIES, 1):
        tmp = out / "_tmp.html"; tmp.write_text(page(line, photo, pos))
        pg.goto("file://" + str(tmp)); pg.wait_for_timeout(400)
        pg.screenshot(path=str(out / f"story{i}.png"))
    tmp.unlink(); b.close()
print(f"{len(STORIES)} stories -> {out}")
