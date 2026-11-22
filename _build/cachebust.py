# -*- coding: utf-8 -*-
"""Append ?v=<content-hash> to local CSS/JS references in every HTML page so browsers fetch fresh files after deploy."""
import os, re, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def h(path):
    return hashlib.md5(open(os.path.join(ROOT, path.lstrip("/")), "rb").read()).hexdigest()[:8]
def run():
    n = 0
    for dp, dn, fn in os.walk(ROOT):
        if "_build" in dp or ".git" in dp: continue
        for f in fn:
            if not f.endswith(".html"): continue
            p = os.path.join(dp, f); s = open(p, encoding="utf-8").read()
            s2 = re.sub(r'(/(?:css|js)/[\w-]+\.(?:css|js))(\?v=\w+)?"', lambda m: f'{m.group(1)}?v={h(m.group(1))}"', s)
            if s2 != s: open(p, "w", encoding="utf-8").write(s2); n += 1
    print("cache-busted", n, "pages")
if __name__ == "__main__": run()
