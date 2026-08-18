#!/usr/bin/env python3
"""Build the blog page from /tmp/blog_clean.html into kanal-style standalone page."""
import re, json

ROOT = "/Users/sercansolmaz/Documents/CURSOR_PRJ/turksat-kanal-bulucu"

body = open("/tmp/blog_clean.html", encoding="utf-8").read()

TITLE = "Türksat Frekansları 16 Ağustos 2026'da Güncellendi: Yeni Uydu Ayarları ve Kanal Arama Rehberi"
SLUG = "turksat-frekanslari-guncellendi"
DESC = ("16 Ağustos 2026 Türksat güncellemesi: 3A uydusundan geçiş, yeni frekanslar 12380 ve 12423, "
        "TKGS ve şebeke arama rehberi. Anten yönü değişir mi, sinyal yoksa ne yapmalı — adım adım anlatım.")
CANONICAL = f"https://turksat.sercansolmaz.com/blog/{SLUG}/"

ld = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Article", "headline": TITLE, "description": DESC,
         "url": CANONICAL, "inLanguage": "tr-TR",
         "datePublished": "2026-08-16", "dateModified": "2026-08-18",
         "author": {"@type": "Person", "name": "Sercan Solmaz"},
         "publisher": {"@type": "Organization", "name": "Türksat Bulucu"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Türksat Bulucu", "item": "https://turksat.sercansolmaz.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://turksat.sercansolmaz.com/blog/"},
            {"@type": "ListItem", "position": 3, "name": TITLE, "item": CANONICAL}]}
    ]
}, ensure_ascii=False)

page = f"""<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{TITLE} | Türksat Bulucu</title>
  <meta name="description" content="{DESC}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{CANONICAL}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <script async src="https://scripts.simpleanalyticscdn.com/latest.js"></script>
  <noscript><img src="https://queue.simpleanalyticscdn.com/noscript.gif" alt="" referrerpolicy="no-referrer-when-downgrade"></noscript>
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Türksat Bulucu">
  <meta property="og:locale" content="tr_TR">
  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="{DESC}">
  <meta property="og:url" content="{CANONICAL}">
  <meta property="og:image" content="https://turksat.sercansolmaz.com/og.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{TITLE}">
  <meta name="twitter:description" content="{DESC}">
  <meta name="twitter:image" content="https://turksat.sercansolmaz.com/og.png">
  <style>
    :root {{--ink:#071938;--muted:#60708a;--blue:#0b57c7;--blue-dark:#073985;--ice:#edf5ff;--line:#dbe5f2;--paper:#f7f9fc;--lime:#c9f35b;--white:#fff;}}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; background:var(--paper); color:var(--ink); font-family:Arial,Helvetica,sans-serif; line-height:1.7; }}
    .topbar {{ width:min(1180px, calc(100% - 40px)); height:78px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; }}
    .brand {{ display:inline-flex; align-items:center; gap:11px; text-decoration:none; font-size:15px; font-weight:800; letter-spacing:-.02em; color:var(--ink); }}
    .brand-mark {{ width:34px; height:34px; display:grid; place-items:center; border-radius:11px; background:var(--ink); color:#fff; font-size:17px; }}
    .source-link {{ font-size:13px; font-weight:700; color:var(--muted); text-decoration:none; border-bottom:1px solid #bcc8d8; padding-bottom:3px; }}
    .source-link .x-logo {{ width:12px; height:12px; margin-left:5px; vertical-align:-1.5px; }}
    .wrap {{ width:min(760px, calc(100% - 40px)); margin:0 auto; padding:20px 0 70px; }}
    .breadcrumb {{ color:var(--muted); font-size:12px; margin:0 0 14px; }}
    .breadcrumb a {{ color:var(--blue); text-decoration:none; }}
    h1 {{ font-size:clamp(30px,5vw,48px); line-height:1.12; letter-spacing:-.045em; margin:0 0 14px; }}
    .meta {{ color:var(--muted); font-size:13px; margin:0 0 30px; }}
    .hero-card {{ background:linear-gradient(135deg,#061b3d,#0d54b6); color:#fff; border-radius:24px; padding:28px; margin:0 0 30px; }}
    .hero-card p {{ margin:0; color:#d6e4f5; font-size:15px; }}
    .hero-card a {{ color:var(--lime); font-weight:700; }}
    .content h2 {{ font-size:26px; letter-spacing:-.03em; margin:38px 0 12px; }}
    .content h3 {{ font-size:19px; margin:28px 0 8px; }}
    .content h4 {{ font-size:16px; margin:22px 0 6px; color:var(--blue-dark); }}
    .content p {{ margin:12px 0; color:#22324a; }}
    .content ul, .content ol {{ margin:12px 0; padding-left:24px; color:#22324a; }}
    .content li {{ margin:6px 0; }}
    .content table {{ width:100%; border-collapse:collapse; margin:20px 0; background:#fff; border:1px solid var(--line); border-radius:14px; overflow:hidden; font-size:14px; }}
    .content th {{ background:var(--ink); color:#fff; text-align:left; padding:12px 14px; font-size:12px; text-transform:uppercase; letter-spacing:.06em; }}
    .content td {{ padding:12px 14px; border-top:1px solid var(--line); }}
    .content strong {{ color:var(--ink); }}
    .callout {{ background:var(--ice); border-left:4px solid var(--blue); border-radius:0 14px 14px 0; padding:16px 20px; margin:22px 0; }}
    .callout strong {{ display:block; margin-bottom:4px; color:var(--blue-dark); }}
    .back {{ display:inline-block; margin-top:40px; color:var(--blue); text-decoration:none; font-weight:800; font-size:14px; }}
  </style>
</head>
<body>
  <header class="topbar">
    <a class="brand" href="/">
      <span class="brand-mark" aria-hidden="true">T</span>
      <span>Türksat Bulucu</span>
    </a>
    <a class="source-link" href="https://x.com/sercansolmaz" target="_blank" rel="noreferrer">
      Sercan Solmaz
      <svg class="x-logo" viewBox="0 0 24 24" width="13" height="13" fill="currentColor" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
    </a>
  </header>
  <div class="wrap">
    <p class="breadcrumb"><a href="/">Türksat Bulucu</a> › <a href="/blog/">Blog</a> › Türksat frekans güncellemesi</p>
    <h1>Türksat Frekansları 16 Ağustos 2026'da Güncellendi</h1>
    <p class="meta">18 Ağustos 2026 · Sercan Solmaz tarafından hazırlandı · ~3 dk okuma</p>
    <div class="hero-card">
      <p>Bu rehberde 16 Ağustos 2026 gecesi yapılan uydu geçişinden sonra <strong>yeni Türksat kanal arama frekanslarını</strong>, TKGS kullanıyorsanız ya da kullanmıyorsanız ne yapmanız gerektiğini ve "sinyal yok" durumunda izlenecek adımları bulacaksınız. Kanal adını yazıp frekansı görmek için <a href="/">kanal ve frekans bulucuyu</a> kullanabilirsiniz.</p>
    </div>
    <article class="content">
{body}
    </article>
    <a class="back" href="/">← Kanal ve frekans bulucuya dön</a>
  </div>
  <script type="application/ld+json">{ld}</script>
</body>
</html>
"""

import os
outdir = os.path.join(ROOT, "blog", SLUG)
os.makedirs(outdir, exist_ok=True)
open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(page)
print("blog page written:", outdir)
