import json, urllib.request, urllib.parse, sys
REFS = {
 "birkat-hamazon":"Siddur Edot HaMizrach, Post Meal Blessing",
 "meein-shalosh":"Siddur Edot HaMizrach, Al Hamihya",
 "tefilat-haderech":"Siddur Edot HaMizrach, Assorted Blessings and Prayers, Traveler's Prayer",
 "kiddush-leil-shabbat":"Siddur Edot HaMizrach, Shabbat Evening, Kiddush",
 "shalom-aleichem":"Siddur Edot HaMizrach, Shabbat Evening, Shalom Alekhem",
 "eshet-chayil":"Siddur Edot HaMizrach, Shabbat Evening, Eshet Hayil",
 "birkat-habanim":"Siddur Edot HaMizrach, Shabbat Evening, Blessing of Children",
 "havdala":"Siddur Edot HaMizrach, Havdalah, Havdala",
 "hadlakat-nerot":"Siddur Edot HaMizrach, Shabbat Candle Lighting",
 "sheva-brachot":"Siddur Edot HaMizrach, Assorted Blessings and Prayers, Sheva Berachot",
 "kriat-shema-al-hamita":"Siddur Edot HaMizrach, Bedtime Shema",
 "birkot-hanehenin":"Siddur Edot HaMizrach, Blessings on Enjoyments",
}
out = {}
for slug, ref in REFS.items():
    for ver in ["Torat Emet 357", " Shaliehsaboo Edition"]:
        u = "https://www.sefaria.org/api/v3/texts/" + urllib.parse.quote(ref.replace(" ","_")) + "?version=" + urllib.parse.quote("hebrew|"+ver)
        try:
            import subprocess
            d = json.loads(subprocess.run(["curl","-s",u],capture_output=True).stdout.decode("utf-8"))
            vs = d.get("versions") or []
            if vs and vs[0].get("text"):
                t = vs[0]["text"]
                out[slug] = {"ref": ref, "version": vs[0].get("versionTitle"), "license": vs[0].get("license"), "source": vs[0].get("versionSource"), "text": t}
                break
        except Exception as e:
            print(slug, ver, "ERR", e)
    if slug in out:
        t = out[slug]["text"]; flat = t if isinstance(t, list) else [t]
        print(slug, out[slug]["version"], out[slug]["license"], len(flat), "chars", sum(len(x) if isinstance(x,str) else 0 for x in flat))
    else: print(slug, "MISSING")
json.dump(out, open("prayers.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
