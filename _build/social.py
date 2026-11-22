# -*- coding: utf-8 -*-
"""Lior's verified social profiles: icons in the sprite, links in footer / mobile menu / contact, and schema.org sameAs."""
import os, re, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

SOCIAL = [
    ("facebook", "פייסבוק", "https://www.facebook.com/mmolior"),
    ("instagram", "אינסטגרם", "https://www.instagram.com/liormamo9725/"),
    ("youtube", "יוטיוב", "https://www.youtube.com/@liormamo405"),
]
SYMBOLS = {
    "facebook": '<symbol id="i-facebook" viewBox="0 0 24 24"><path fill="currentColor" d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21h3.1z"/></symbol>',
    "instagram": '<symbol id="i-instagram" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" d="M7.5 3h9A4.5 4.5 0 0 1 21 7.5v9a4.5 4.5 0 0 1-4.5 4.5h-9A4.5 4.5 0 0 1 3 16.5v-9A4.5 4.5 0 0 1 7.5 3z"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.3" cy="6.7" r="1.2" fill="currentColor"/></symbol>',
    "youtube": '<symbol id="i-youtube" viewBox="0 0 24 24"><path fill="currentColor" d="M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.5 2.5 0 0 0 2.4 7.2 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8zM10 15V9l5.2 3L10 15z"/></symbol>',
}

def icons(cls="soc"):
    return f'<div class="{cls}">' + "".join(
        f'<a href="{u}" target="_blank" rel="noopener me" aria-label="ליאור ממו ב{n}"><svg aria-hidden="true"><use href="#i-{k}"/></svg><span>{n}</span></a>'
        for k, n, u in SOCIAL) + '</div>'

def patch(s):
    # sprite symbols
    if 'id="i-facebook"' not in s:
        s = re.sub(r'(<svg width="0" height="0"[^>]*>)', lambda m: m.group(1) + "\n" + "\n".join(SYMBOLS.values()), s, count=1)
    # footer + mobile menu
    s = re.sub(r'<div class="soc[^"]*">.*?</div>', '', s, flags=re.S)
    s = s.replace('<nav class="legal-links"', icons("soc soc-foot") + '\n    <nav class="legal-links"', 1)
    s = re.sub(r'(<div class="mnav-cta">.*?</div>)', lambda m: m.group(1) + icons("soc soc-menu"), s, count=1, flags=re.S)
    # sameAs on the business + person
    urls = [u for _, _, u in SOCIAL]
    def ld(m):
        try: d = json.loads(m.group(1))
        except Exception: return m.group(0)
        for node in (d.get("@graph") or [d]):
            if isinstance(node, dict) and node.get("@id") == B.BUSINESS_ID:
                node["sameAs"] = urls
                if isinstance(node.get("founder"), dict): node["founder"]["sameAs"] = urls
        return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, s, flags=re.S)
    return s

def run():
    n = 0
    for f in glob.glob(os.path.join(B.ROOT, "**", "*.html"), recursive=True):
        if os.sep + "_" in f.replace(B.ROOT, "") or "google" in os.path.basename(f): continue
        s = open(f, encoding="utf-8").read()
        if '<footer>' not in s and 'mnav' not in s: continue
        t = patch(s)
        if t != s: open(f, "w", encoding="utf-8").write(t); n += 1
    print("social links in", n, "pages")

if __name__ == "__main__": run()
