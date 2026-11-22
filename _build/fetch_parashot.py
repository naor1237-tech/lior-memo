# -*- coding: utf-8 -*-
"""Collect all 54 parashot (aliyot, maftir, haftarot) from Hebcal and the maftir + Sephardi haftarah text
with cantillation from Sefaria (Tanach with Ta'amei Hamikra – Public Domain). Output: data/parashot.json"""
import json, os, re, subprocess, urllib.parse, time
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "parashot.json")

def get(url):
    return json.loads(subprocess.run(["curl", "-s", url], capture_output=True).stdout.decode("utf-8"))

# 1) parasha structure from Hebcal (Israel schedule), several years to catch every split parasha
par = {}
import calendar
for il in ("on", "off"):
 for y in list(range(2025, 2031)) + [2035]:
  for m in range(1, 13, 2):
    last = calendar.monthrange(y, m + 1)[1]
    d = get(f"https://www.hebcal.com/leyning?cfg=json&start={y}-{m:02d}-01&end={y}-{m+1:02d}-{last}&i={il}")
    for it in d.get("items", []):
        n = it.get("parshaNum")
        if it.get("type") != "shabbat" and n != 54: continue
        if not isinstance(n, int) or n in par: continue
        par[n] = it
print("parashot found:", len(par), sorted(set(range(1, 55)) - set(par)))

SEF = "Tanach with Ta'amei Hamikra"
def sef_text(ref):
    u = "https://www.sefaria.org/api/v3/texts/" + urllib.parse.quote(ref.replace(" ", "_")) + "?version=" + urllib.parse.quote("hebrew|" + SEF)
    try:
        d = get(u); t = d["versions"][0]["text"]
    except Exception as e:
        print("  sefaria fail", ref, e); return None
    flat = []
    def walk(x):
        if isinstance(x, list):
            for y in x: walk(y)
        elif isinstance(x, str): flat.append(x)
    walk(t)
    return [re.sub(r"<[^>]+>", "", s).replace("&nbsp;", " ").strip() for s in flat if s.strip()]

def ref_of(o):  # {'k':'Genesis','b':'32:4','e':'32:13'}
    b, e = o["b"], o["e"]
    return f'{o["k"]} {b}-{e}' if ":" in e else f'{o["k"]} {b}-{b.split(":")[0]}:{e}'

def haft_refs(s):  # 'II Kings 4:1-23' or 'Isaiah 54:1-10; 55:1-5'
    refs, book = [], None
    for part in [p.strip() for p in s.split(";") if p.strip()]:
        m = re.match(r"^([A-Za-z ]+?)\s+(\d+:\d+(?:-\d+(?::\d+)?)?)$", part)
        if m: book = m.group(1); refs.append(f"{book} {m.group(2)}")
        elif book: refs.append(f"{book} {part}")
    return refs

out = []
for n in sorted(par):
    it = par[n]; fk = it.get("fullkriyah", {})
    aliyot = [{"n": k, "k": v["k"], "b": v["b"], "e": v["e"], "v": v.get("v")} for k, v in fk.items() if k in "1234567M"]
    maftir = fk.get("M")
    seph = it.get("sephardic") or it.get("haftara")
    rec = {"num": n, "en": it["name"]["en"], "he": re.sub(r"[֑-ׇ]", "", it["name"]["he"]), "summary": it.get("summary"),
           "aliyot": aliyot, "haftara_ashk": it.get("haftara"), "haftara_seph": seph}
    rec["maftir_text"] = sef_text(ref_of(maftir)) if maftir else None
    ht = []
    for r in haft_refs(seph or ""):
        t = sef_text(r); ht += (t or []); time.sleep(0.2)
    rec["haftara_text"] = ht
    out.append(rec); print(n, rec["en"], len(rec["maftir_text"] or []), len(ht)); time.sleep(0.2)
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved", len(out))
