# -*- coding: utf-8 -*-
"""Vezot Haberakhah is read on Simchat Torah (no Shabbat entry in Hebcal's leyning feed), so fill its aliyot,
maftir and haftarah by hand (standard Simchat Torah reading) and fetch the texts with cantillation from Sefaria."""
import json, os, re, subprocess, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(HERE, "data", "parashot.json")
SEF = "Tanach with Ta'amei Hamikra"

def sef_text(ref):
    u = "https://www.sefaria.org/api/v3/texts/" + urllib.parse.quote(ref.replace(" ", "_")) + "?version=" + urllib.parse.quote("hebrew|" + SEF)
    d = json.loads(subprocess.run(["curl", "-s", u], capture_output=True).stdout.decode("utf-8"))
    flat = []
    def walk(x):
        if isinstance(x, list):
            for y in x: walk(y)
        elif isinstance(x, str): flat.append(x)
    walk(d["versions"][0]["text"])
    return [re.sub(r"<[^>]+>", "", s).replace("&nbsp;", " ").strip() for s in flat if s.strip()]

data = json.load(open(F, encoding="utf-8"))
p = next(x for x in data if x["num"] == 54)
p["aliyot"] = [
    {"n": "1", "k": "Deuteronomy", "b": "33:1", "e": "33:7", "v": 7},
    {"n": "2", "k": "Deuteronomy", "b": "33:8", "e": "33:12", "v": 5},
    {"n": "3", "k": "Deuteronomy", "b": "33:13", "e": "33:17", "v": 5},
    {"n": "4", "k": "Deuteronomy", "b": "33:18", "e": "33:21", "v": 4},
    {"n": "5", "k": "Deuteronomy", "b": "33:22", "e": "33:26", "v": 5},
    {"n": "6", "k": "Deuteronomy", "b": "33:27", "e": "33:29", "v": 3},
    {"n": "7", "k": "Deuteronomy", "b": "34:1", "e": "34:12", "v": 12},
    {"n": "M", "k": "Numbers", "b": "29:35", "e": "30:1", "v": 6},
]
p["haftara_ashk"] = "Joshua 1:1-18"
p["haftara_seph"] = "Joshua 1:1-9"
p["maftir_text"] = sef_text("Numbers 29:35-30:1")
p["haftara_text"] = sef_text("Joshua 1:1-9")
p["simchat_torah"] = True
json.dump(data, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("vezot fixed:", len(p["maftir_text"]), len(p["haftara_text"]))
