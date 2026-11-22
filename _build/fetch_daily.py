# -*- coding: utf-8 -*-
"""Fetch the daily prayers (Siddur Edot HaMizrach, Torat Emet – Public Domain) from Sefaria and merge into data/prayers.json.
Each prayer is a list of (section title, Sefaria ref). Run: python _build/fetch_daily.py"""
import json, os, subprocess, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "prayers.json")
B = "Siddur Edot HaMizrach, "
DAILY = {
 "birkot-hashachar": [("מודה אני", B+"Preparatory Prayers, Modeh Ani"), ("ברכות השחר", B+"Preparatory Prayers, Morning Blessings"), ("ברכות התורה", B+"Preparatory Prayers, Torah Blessings")],
 "shacharit": [("סדר עטיפת ציצית", B+"Weekday Shacharit, Order of Talit"), ("סדר הנחת תפילין", B+"Weekday Shacharit, Order of Tefillin"),
               ("תפילת שחרית", B+"Weekday Shacharit, Morning Prayer"), ("פטום הקטורת", B+"Weekday Shacharit, Incense Offering"), ("הודו", B+"Weekday Shacharit, Hodu"),
               ("פסוקי דזמרה", B+"Weekday Shacharit, Pesukei D'Zimra"), ("קריאת שמע וברכותיה", B+"Weekday Shacharit, The Shema"), ("עמידה", B+"Weekday Shacharit, Amida"),
               ("וידוי", B+"Weekday Shacharit, Vidui"), ("אשרי", B+"Weekday Shacharit, Ashrei"), ("ובא לציון", B+"Weekday Shacharit, Uva LeSion"),
               ("בית יעקב", B+"Weekday Shacharit, Beit Yaakov"), ("שיר של יום", B+"Weekday Shacharit, Song of the Day"), ("קוה", B+"Weekday Shacharit, Kaveh"), ("עלינו", B+"Weekday Shacharit, Alenu")],
 "mincha": [("קרבנות ואשרי", B+"Weekday Mincha, Offerings"), ("עמידה", B+"Weekday Mincha, Amida"), ("וידוי", B+"Weekday Mincha, Vidui"), ("עלינו", B+"Weekday Mincha, Alenu")],
 "arvit": [("ברכו", B+"Weekday Arvit, Barchu"), ("קריאת שמע וברכותיה", B+"Weekday Arvit, The Shema"), ("עמידה", B+"Weekday Arvit, Amidah"), ("עלינו", B+"Weekday Arvit, Alenu")],
}
def fetch(ref):
    u = "https://www.sefaria.org/api/v3/texts/" + urllib.parse.quote(ref.replace(" ", "_")) + "?version=" + urllib.parse.quote("hebrew|Torat Emet 357")
    d = json.loads(subprocess.run(["curl", "-s", u], capture_output=True).stdout.decode("utf-8"))
    v = (d.get("versions") or [{}])[0]
    return v.get("text"), v.get("license")

data = json.load(open(DATA, encoding="utf-8"))
for slug, parts in DAILY.items():
    text, lic = [], set()
    for title, ref in parts:
        t, l = fetch(ref)
        if not t: print("MISSING", slug, ref); continue
        lic.add(l); text.append(f"<big><b>{title}</b></big>"); text.append(t)
    data[slug] = {"ref": parts[0][1].rsplit(",", 1)[0] if slug != "birkat-hamazon" else parts[0][1], "version": "Torat Emet 357",
                  "license": "/".join(sorted(x for x in lic if x)), "text": text, "sections": [p[0] for p in parts]}
    print(slug, data[slug]["license"], sum(len(str(x)) for x in text))
json.dump(data, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
