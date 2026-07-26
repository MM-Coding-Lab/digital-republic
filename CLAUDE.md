# Digital Republic Manifest

Strona manifestu Cyfrowej Republiki: [thedigitalrepublic.org](https://thedigitalrepublic.org)

## Struktura projektu
- `index.html` — cały manifest w jednym pliku (HTML + CSS + JS + i18n PL/EN)
- `og-image-pl-v2.png` / `og-image-en-v2.png` — hero img 1200×630 dla podglądu w social mediach (PL i EN). Sufiks `-vN` używamy do cache-bust przy regeneracji obrazu — przy kolejnej regeneracji bump na `-v3` itd.

## Deployment (FTP)

Hosting: Cyberfolks (LiteSpeed)
Domena: thedigitalrepublic.org

### Dane FTP
- **Host:** `TheDigitalRepublic.org`
- **User:** `tyramomphf`
- **Hasło:** `2Lmz9EFZAhJd2K68htnW`

### Struktura na serwerze
```
/domains/thedigitalrepublic.org/public_html/
├── index.html             (PL — thedigitalrepublic.org)
├── og-image-pl-v2.png     (hero img PL — referowane przez og:image w wersji PL)
└── en/
    ├── index.html         (EN — thedigitalrepublic.org/en/)
    └── og-image-en-v2.png (hero img EN — referowane przez og:image w wersji EN)
```

Ten sam plik index.html w obu lokalizacjach — język wykrywany automatycznie po ścieżce `/en/`.

**Ważne dla OG / social preview:** crawlery social mediów (FB, LinkedIn, Twitter/X) nie wykonują JS, więc statyczne meta tagi w HTML muszą być właściwe dla danego URL. JS dynamicznie aktualizuje meta tagi dla użytkownika w przeglądarce, ale crawler dostanie to, co statycznie zapisane w pliku. Dlatego przy uploadzie do `/en/` podmieniamy w locie OG image i locale przez `sed`.

### Upload z CLI (HTML + obrazy)
```bash
# PL — root: index.html (statyczne OG = PL) + obraz PL
curl -s -T "index.html" --user 'tyramomphf:2Lmz9EFZAhJd2K68htnW' "ftp://TheDigitalRepublic.org/domains/thedigitalrepublic.org/public_html/index.html"
curl -s -T "og-image-pl-v2.png" --user 'tyramomphf:2Lmz9EFZAhJd2K68htnW' "ftp://TheDigitalRepublic.org/domains/thedigitalrepublic.org/public_html/og-image-pl-v2.png"

# EN — /en/: index.html z podmienionymi statycznymi OG na EN + obraz EN
EN_DESC='A vision of a state built on data, transparency, and accountability. How technology and AI can serve citizens, curb corruption, and strengthen individual freedom.'
EN_META_DESC="The Digital Republic Manifesto — ${EN_DESC}"
sed \
    -e 's|og-image-pl-v2.png|en/og-image-en-v2.png|g' \
    -e 's|<link rel="canonical" href="https://thedigitalrepublic.org/"|<link rel="canonical" href="https://thedigitalrepublic.org/en/"|' \
    -e 's|<title>Manifest Cyfrowej Republiki[^<]*</title>|<title>The Digital Republic Manifesto - TheDigitalRepublic.org</title>|' \
    -e "s|<meta name=\"description\" content=\"[^\"]*\">|<meta name=\"description\" content=\"${EN_META_DESC}\">|" \
    -e 's|<meta property="og:url" content="https://thedigitalrepublic.org/"|<meta property="og:url" content="https://thedigitalrepublic.org/en/"|' \
    -e 's|<meta property="og:title" content="Manifest Cyfrowej Republiki"|<meta property="og:title" content="The Digital Republic Manifesto"|' \
    -e "s|<meta property=\"og:description\" content=\"[^\"]*\">|<meta property=\"og:description\" content=\"${EN_DESC}\">|" \
    -e 's|<meta property="og:image:alt" content="Manifest Cyfrowej Republiki"|<meta property="og:image:alt" content="The Digital Republic Manifesto"|' \
    -e 's|<meta property="og:locale" content="pl_PL">|<meta property="og:locale" content="en_US">|' \
    -e 's|<meta property="og:locale:alternate" content="en_US">|<meta property="og:locale:alternate" content="pl_PL">|' \
    -e 's|<meta name="twitter:title" content="Manifest Cyfrowej Republiki"|<meta name="twitter:title" content="The Digital Republic Manifesto"|' \
    -e "s|<meta name=\"twitter:description\" content=\"[^\"]*\">|<meta name=\"twitter:description\" content=\"${EN_DESC}\">|" \
    index.html > /tmp/index-en.html
curl -s -T "/tmp/index-en.html" --user 'tyramomphf:2Lmz9EFZAhJd2K68htnW' "ftp://TheDigitalRepublic.org/domains/thedigitalrepublic.org/public_html/en/index.html"
curl -s -T "og-image-en-v2.png" --user 'tyramomphf:2Lmz9EFZAhJd2K68htnW' "ftp://TheDigitalRepublic.org/domains/thedigitalrepublic.org/public_html/en/og-image-en-v2.png"
rm /tmp/index-en.html
```

### Regeneracja obrazów OG
Dedykowany skrypt `generate_og.py` (Gemini 3.1 Flash Image Preview, typografia wbudowana w obraz):
```bash
/home/maciej/coding/wordpress-blog-agent/.venv/bin/python generate_og.py             # PL + EN
/home/maciej/coding/wordpress-blog-agent/.venv/bin/python generate_og.py --lang pl   # tylko PL
/home/maciej/coding/wordpress-blog-agent/.venv/bin/python generate_og.py --lang en   # tylko EN
```
Klucz API: `GOOGLE_AI_API_KEY` z `../wordpress-blog-agent/.env.blog-agent`. Prompt zawiera tytuł, podtytuł, kompozycję (klasyczne kolumny + sieć cyfrowa, granatowe tło). Po regeneracji upload przez `curl` jak wyżej.

**Cache crawlerów:** FB/LinkedIn/X aggressively cache'ują OG image po URL. Po podmianie obrazu (URL bez zmiany) wymuś re-scrape przez:
- LinkedIn Post Inspector: https://www.linkedin.com/post-inspector/
- Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/ (klik "Scrape Again")

### Deploy workflow
1. Zmodyfikuj `index.html`
2. Zweryfikuj zmiany lokalnie
3. Commit + push do repo
4. Upload na FTP komendą powyżej

## i18n
Strona ma wbudowany system tłumaczeń PL/EN w obiekcie `I18N` w `<script>` na dole pliku.
- Elementy z `data-i18n` — tłumaczenie przez `textContent`
- Elementy z `data-i18n-html` — tłumaczenie przez `innerHTML` (gdy zawierają tagi HTML)
- Przy zmianach treści zawsze aktualizuj OBA języki (PL i EN)

## Kontakt
- Email: mm@elementapp.ai
- Autor: Maciej Michalewski
