# auth.md — Türksat Bulucu Agent Kimlik Doğrulama Rehberi

Bu site ağırlıklı olarak **herkese açık** (public) bir kaynaktır. Kimlik doğrulama gerektiren endpoint yoktur.

## Herkese açık kaynaklar

| Kaynak | URL | Kimlik doğrulama |
|--------|-----|------------------|
| Web arayüzü | `https://turksat.sercansolmaz.com/` | Gerekmez |
| Markdown sürümü | `Accept: text/markdown` ile aynı URL | Gerekmez |
| Trend aramalar | `GET https://turksat-trends.sercansolmaz.workers.dev/top` | Gerekmez |
| Favori/seçim istatistikleri | `GET https://turksat-trends.sercansolmaz.workers.dev/insights` | Gerekmez |
| MCP sunucusu | `POST https://turksat-trends.sercansolmaz.workers.dev/mcp` | Gerekmez |
| Kanal detay sayfaları | `https://turksat.sercansolmaz.com/kanal/<slug>/` | Gerekmez |

## Yazma endpoint'leri

`POST /track`, `POST /select`, `POST /fav` anonim sayaçlardır; yalnızca normalize edilmiş arama terimi ve kanal adı kabul eder. Kimlik bilgisi toplanmaz.

## Kayıt / API anahtarı

Şu anda API anahtarı dağıtılmamaktadır. Yüksek hacimli erişim gerektiren agent'lar için hız sınırı: ücretsiz Cloudflare Workers katmanı (günde ~100.000 istek).

## İletişim

Sorular için: https://x.com/sercansolmaz
