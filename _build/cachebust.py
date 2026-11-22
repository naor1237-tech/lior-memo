# -*- coding: utf-8 -*-
"""Post-process every HTML page:
1) append ?v=<content-hash> to local CSS/JS references so browsers fetch fresh files after deploy;
2) load Google Fonts without blocking rendering (preload + onload swap, with <noscript> fallback)."""
import os, re, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_RE = re.compile(r'<link href="(https://fonts\.googleapis\.com/css2\?[^"]+)" rel="stylesheet">')
ASSET_RE = re.compile(r'(/(?:css|js)/[\w-]+\.(?:css|js))(\?v=\w+)?"')

def h(path):
    return hashlib.md5(open(os.path.join(ROOT, path.lstrip("/")), "rb").read()).hexdigest()[:8]

def font_swap(m):
    url = m.group(1)
    return ('<link rel="preload" as="style" href="' + url + '" onload="this.onload=null;this.rel=\'stylesheet\'">'
            '<noscript><link rel="stylesheet" href="' + url + '"></noscript>')

def run():
    n = 0
    for dp, dn, fn in os.walk(ROOT):
        if "_build" in dp or ".git" in dp: continue
        for f in fn:
            if not f.endswith(".html"): continue
            p = os.path.join(dp, f); s = open(p, encoding="utf-8").read()
            s2 = FONT_RE.sub(font_swap, s)
            s2 = ASSET_RE.sub(lambda m: m.group(1) + "?v=" + h(m.group(1)) + '"', s2)
            if s2 != s: open(p, "w", encoding="utf-8").write(s2); n += 1
    print("post-processed", n, "pages")

if __name__ == "__main__": run()
