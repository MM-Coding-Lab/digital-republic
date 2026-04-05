# Digital Republic Manifest

Strona manifestu Cyfrowej Republiki: [thedigitalrepublic.org](https://thedigitalrepublic.org)

## Struktura projektu
- `index.html` — cały manifest w jednym pliku (HTML + CSS + JS + i18n PL/EN)

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
├── index.html          (PL — thedigitalrepublic.org)
└── en/
    └── index.html      (EN — thedigitalrepublic.org/en/)
```

Ten sam plik index.html w obu lokalizacjach — język wykrywany automatycznie po ścieżce `/en/`.

### Upload z CLI (oba pliki!)
```bash
curl -s -T "index.html" --user 'tyramomphf:2Lmz9EFZAhJd2K68htnW' "ftp://TheDigitalRepublic.org/domains/thedigitalrepublic.org/public_html/index.html"
curl -s -T "index.html" --user 'tyramomphf:2Lmz9EFZAhJd2K68htnW' "ftp://TheDigitalRepublic.org/domains/thedigitalrepublic.org/public_html/en/index.html"
```

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
