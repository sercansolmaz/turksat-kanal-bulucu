#!/usr/bin/env python3
"""Generate static channel detail pages for ALL channels in SITE_DATA."""
import json, re, os, html as htmlmod

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(ROOT, "index.html")

src = open(INDEX, encoding="utf-8").read()
m = re.search(r'const SITE_DATA = (\{.*?\});\n', src, re.DOTALL)
data = json.loads(m.group(1))

def slugify(name):
    s = name.lower()
    tr_map = {"ç":"c","ğ":"g","ı":"i","ö":"o","ş":"s","ü":"u","â":"a","î":"i","û":"u"}
    for k, v in tr_map.items(): s = s.replace(k, v)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s

def esc(s): return htmlmod.escape(str(s), quote=True)

# Build channel -> mux list map (a channel can be on multiple muxes)
ch_map = {}
for mux in data["muxes"]:
    for svc in mux.get("services", []):
        ch_map.setdefault(svc["name"], []).append((svc, mux))

# Generate pages for ALL unique channel names
selected = list(ch_map.keys())

TMPL = """<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <meta name="description" content="__DESC__">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://turksat.sercansolmaz.com/kanal/__SLUG__/">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <script async src="https://scripts.simpleanalyticscdn.com/latest.js"></script>
  <noscript><img src="https://queue.simpleanalyticscdn.com/noscript.gif" alt="" referrerpolicy="no-referrer-when-downgrade"></noscript>
  <style>
    :root {--ink:#071938;--muted:#60708a;--blue:#0b57c7;--line:#dbe5f2;--paper:#f7f9fc;--lime:#c9f35b;}
    * { box-sizing: border-box; }
    body { margin:0; background:var(--paper); color:var(--ink); font-family:Arial,Helvetica,sans-serif; }
    .wrap { width:min(860px, calc(100% - 32px)); margin:0 auto; padding:40px 0 60px; }
    a.back { display:inline-flex; align-items:center; gap:8px; color:var(--blue); text-decoration:none; font-weight:800; font-size:14px; margin-bottom:26px; }
    h1 { font-size:clamp(28px,5vw,44px); letter-spacing:-.04em; margin:0 0 6px; }
    .sub { color:var(--muted); font-size:15px; margin:0 0 28px; }
    .card { background:white; border:1px solid var(--line); border-radius:20px; padding:28px; margin-bottom:18px; }
    .card h2 { font-size:15px; letter-spacing:.06em; color:var(--blue); text-transform:uppercase; margin:0 0 18px; }
    table { width:100%; border-collapse:collapse; font-size:14.5px; }
    th { text-align:left; color:var(--muted); font-size:11px; text-transform:uppercase; letter-spacing:.07em; padding:9px 10px; border-bottom:2px solid var(--line); }
    td { padding:13px 10px; border-bottom:1px solid var(--line); font-weight:700; }
    td.small { font-weight:400; color:var(--muted); }
    .freq { font-size:22px; color:var(--blue); }
    .howto { background:var(--ink); color:white; border:0; border-radius:20px; padding:28px; }
    .howto h2 { color:#8dbbff; }
    .howto ol { margin:16px 0 0; padding-left:20px; line-height:1.9; color:#c9d9ee; font-size:14px; }
    .badge { display:inline-block; background:#e8f1ff; color:#0755c7; border-radius:6px; padding:3px 8px; font-size:10px; font-weight:900; letter-spacing:.06em; margin-left:10px; vertical-align:middle; }
    .aka { color:var(--muted); font-weight:700; font-size:.6em; letter-spacing:0; }
    .note { color:var(--muted); font-size:12px; line-height:1.6; }
  </style>
</head>
<body>
  <div class="wrap">
    <a class="back" href="/">← Türksat Kanal ve Frekans Bulucu</a>
    <h1>__H1__</h1>
    <p class="sub">__SUB__</p>
    __CARDS__
    <div class="card howto">
      <h2>Televizyona nasıl girilir?</h2>
      <ol>
        <li>Kurulum menüsünden <strong>uydu/kanal ayarlarına</strong> girin.</li>
        <li><strong>Türksat 42° Doğu</strong> uydusunu seçip manuel (TP) aramayı açın.</li>
        <li>Yukarıdaki <strong>frekans, polarizasyon (V/H) ve sembol oranı</strong> değerlerini girin.</li>
        <li>Taramayı başlatın; bulununca kanalı kaydedin.</li>
      </ol>
    </div>
    <p class="note">Veriler 18.08.2026 tarihinde resmî kaynaklarla karşılaştırılarak derlenmiştir. Frekanslar zamanla değişebilir; kritik kurulumlarda <a href="https://www.turksat.com.tr/uydu/yayincilik-hizmetleri/turksat-frekans-listesi" rel="noreferrer" target="_blank">resmî Türksat listesini</a> kontrol edin.</p>
  </div>
  <script type="application/ld+json">__LDJSON__</script>
</body>
</html>
"""

generated = 0
slugs = []
for name in selected:
    entries = ch_map[name]
    slug = slugify(name)
    if not slug or slug in slugs: continue
    slugs.append(slug)
    svc0 = entries[0][0]
    type_label = "Radyo" if svc0.get("type") == "Radyo" else "TV kanalı"
    qual = svc0.get("quality", "")
    aka = svc0.get("aka", "")
    rows = []
    for svc, mux in entries:
        rows.append({
            "frekans_mhz": mux["frequency"] + (" / " + mux["alternate"] if mux.get("alternate") else ""),
            "polarizasyon": mux["polarization"] + " (" + ("Dikey" if mux["polarization"]=="V" else "Yatay") + ")",
            "sembol_orani": mux["symbolRate"],
            "fec": mux["fec"],
            "uydu": mux["satellite"],
            "kapsama": mux["coverage"],
        })
    trs = ""
    for r in rows:
        trs += "<tr><td class='freq'>" + esc(r["frekans_mhz"]) + " MHz</td><td>" + esc(r["polarizasyon"]) + "</td><td>" + esc(r["sembol_orani"]) + "</td><td class='small'>" + esc(r["fec"]) + "</td><td class='small'>" + esc(r["uydu"]) + "</td><td class='small'>" + esc(r["kapsama"]) + "</td></tr>"
    cards = ('<div class="card"><h2>Frekans ayarları — Türksat 42° Doğu</h2>'
             '<table><tr><th>Frekans</th><th>Polarizasyon</th><th>Sembol oranı</th><th>FEC</th><th>Uydu</th><th>Kapsama</th></tr>'
             + trs + '</table></div>')
    h1 = esc(name) + ('<span class="badge">' + esc(qual) + '</span>' if qual else '') + (' <span class="aka">(' + esc(aka) + ')</span>' if aka else '')
    title = name + (" (" + aka + ") " if aka else " ") + "Frekansı 2026 — Türksat Ayarları | 42°Doğu"
    desc = ("{} frekansı: {}. Televizyonunuza manuel girmek için polarizasyon, sembol oranı ve FEC değerleri tablosu. Türksat 42° doğu güncel 2026 listesi.".format(
        name + (" (" + aka + ")" if aka else ""), "; ".join("{} MHz {}".format(r["frekans_mhz"], r["polarizasyon"].split()[0]) for r in rows[:2])))
    ld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type":"WebPage","name": name + " frekansı","url":"https://turksat.sercansolmaz.com/kanal/"+slug+"/","inLanguage":"tr-TR"},
            {"@type":"Table","name": name + " frekans bilgileri","about": name, "table": rows}
        ]}, ensure_ascii=False)
    page = TMPL.replace("__TITLE__", esc(title)).replace("__DESC__", esc(desc)).replace("__SLUG__", slug) \
               .replace("__H1__", h1).replace("__SUB__", esc("Türksat 42° Doğu " + type_label + " — güncel yayın ayarları")) \
               .replace("__CARDS__", cards).replace("__LDJSON__", ld)
    outdir = os.path.join(ROOT, "kanal", slug)
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(page)
    generated += 1

print("generated:", generated, "pages")
with open(os.path.join(ROOT, ".channel-slugs.json"), "w", encoding="utf-8") as f:
    json.dump(slugs, f, ensure_ascii=False)
