#!/usr/bin/env bash
# Türksat frekans değişiklik izleyici — KingOfSat 42E (4A/5B/6A) karşılaştırma + Telegram bildirimi (hermes send)
set -euo pipefail

KV_NS="3433250e02c7445a84fd385fcbec30f1"
KV_API="https://api.cloudflare.com/client/v4/accounts/1960d5e4651acc4079574e18e05610fa/storage/kv/namespaces/$KV_NS/values"
OAUTH=$(grep oauth_token "$HOME/Library/Preferences/.wrangler/config/default.toml" | cut -d'"' -f2)

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"
TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT

# 3 uydu sayfasini indir (4A + 5B + 6A) — 42E'deki tüm Türksat transponderleri
: > "$TMP"
for sat in turksat4a turksat5b turksat6a; do
  curl -sL "https://en.kingofsat.net/sat-$sat" -A "$UA" --max-time 40 >> "$TMP" 2>/dev/null || true
  echo >> "$TMP"
done
[ -s "$TMP" ] || { echo "kaynak alinamadi"; exit 1; }

cd "$HOME/Documents/CURSOR_PRJ/turksat-kanal-bulucu"

python3 - "$TMP" > /tmp/freq_diff.txt <<'PYEOF'
import re, sys, json

kos_html = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
kos_freqs = set()
for m in re.finditer(r'class="bld">(\d{5})(?:\.\d+)?</td>', kos_html):
    kos_freqs.add(m.group(1))

src = open("index.html", encoding="utf-8").read()
data = json.loads(re.search(r'const SITE_DATA = (\{.*?\});', src, re.DOTALL).group(1))
site_freqs = set(m["frequency"] for m in data["muxes"])
site_alts = set(m["alternate"] for m in data["muxes"] if m.get("alternate"))
site_all = site_freqs | site_alts

def near(f, s): return any(abs(int(f)-int(k)) <= 1 for k in s)
new = [f for f in sorted(kos_freqs - site_all, key=int) if not near(f, site_all)]
gone = [f for f in sorted(site_freqs - kos_freqs, key=int) if not near(f, kos_freqs)]

out = []
if new: out.append("NEW:" + ",".join(new))
if gone: out.append("GONE:" + ",".join(gone))
print(";".join(out) if out else "NOCHANGE")
PYEOF

DIFF=$(cat /tmp/freq_diff.txt)
LAST_STATE=$(curl -s -H "Authorization: Bearer $OAUTH" "$KV_API/monitor:last" 2>/dev/null || echo "")
TODAY=$(date +%F)

if [ "$DIFF" != "NOCHANGE" ] && [ "$DIFF" != "$LAST_STATE" ]; then
  NEW=$(echo "$DIFF" | grep -oE 'NEW:[0-9,]+' | cut -d: -f2 | tr ',' ' ')
  GONE=$(echo "$DIFF" | grep -oE 'GONE:[0-9,]+' | cut -d: -f2 | tr ',' ' ')
  MSG=""
  [ -n "$NEW" ] && MSG="🛒 KingOfSat'ta yeni transponder: $NEW"
  [ -n "$GONE" ] && MSG="${MSG:+$MSG
}⚠️ Kaynakta bulunamayan (kalkmış olabilir): $GONE"

  # Telegram via hermes send (gateway credentials)
  hermes send -t "telegram:Sercan Solmaz" "🛰 Türksat Frekans İzleyici ($TODAY)
$MSG

Kaynak: kingofsat.net 42°E (4A/5B/6A) · Site: turksat.sercansolmaz.com" > /dev/null 2>&1 || true

  curl -s -X PUT "$KV_API/monitor:last" -H "Authorization: Bearer $OAUTH" --data "$DIFF" > /dev/null 2>&1 || true
  echo "($TODAY) bildirim gonderildi: $DIFF"
else
  echo "($TODAY) degisiklik yok"
fi
