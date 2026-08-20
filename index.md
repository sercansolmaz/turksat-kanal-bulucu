# Türksat Kanal ve Frekans Bulucu (Türksat Bükücü)

Türksat 42° Doğu uydu yayınları için kanal frekansı arama aracı. Kanal adını yazın; frekans (MHz), polarizasyon (V/H), sembol oranı ve FEC değerini anında görün.

**Üst veri:** 182 kanal · 146 TV · 36 radyo · Türksat 4A / 5B / 6A uyduları · Veriler 18.08.2026 tarihinde doğrulandı.

## Genel şebeke (ağ) arama ayarları

| Frekans | Polarizasyon | Sembol oranı | FEC |
|---------|--------------|--------------|-----|
| 12380 MHz | V (Dikey) | 27500 | 3/4 |
| 12423 MHz | H (Yatay) | 27500 | 3/4 |

Alternatif frekans notu: bazı alıcılar 12379 / 12422 gösterir.

## Öne çıkan kanal frekansları

- **Show TV HD** — 12302 MHz · V · 27500 · FEC 3/4 (Türksat 4A)
- **TRT 1 HD** — 11794 MHz · V · 30000 · FEC 3/4 (Türksat 4A)
- **Kanal D HD** — 12245 MHz · H · 27500 · FEC 5/6 (Türksat 4A)
- **ATV HD** — 12206 MHz · H · 27500 · FEC 3/4 (Türksat 4A)
- **Star TV HD** — 12015 MHz · H · 27500 · FEC 3/4 (Türksat 4A)
- **Habertürk HD** — 12302 MHz · V · 27500 · FEC 3/4 (Türksat 4A)
- **SZC (Sözcü)** — 12111 MHz · V · 27500 · FEC 3/4 (Türksat 6A)

## Manuel tarama (4 adım)

1. Televizyonunuzun kurulum menüsünden uydu/kanal ayarlarına girin.
2. Türksat 42° Doğu'yu seçip manuel (TP) aramayı açın.
3. Bulduğunuz frekans, V/H ve sembol oranı değerlerini girin.
4. Taramayı başlatın ve sonuçları kaydedin.

## Araçlar

- Web arayüzü: https://turksat.sercansolmaz.com/
- Trend aramalar API: https://turksat-trends.sercansolmaz.workers.dev/top
- Frekans sorgulama (MCP): turksat-trends worker'ının `search_channel` aracı

Kaynak: veriler resmî Türksat frekans listesiyle karşılaştırılarak derlendi; kritik kurulumlarda resmî listeyi teyit edin.
