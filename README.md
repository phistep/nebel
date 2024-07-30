# Der Nebel von Dybern

_Ein Drama von Maria Lazar_

[**PDF herunterladen**][pdf-original]


## Download

Das Stück steht in der [Deutschen Nationialbibliothek][dnb] als Scan
[IDN 3D1320989187][dnb-nebel] bereit und kann
[online eingesehen][dnb-nebel-viewer] werden.

Leider kann auf der Seite nur einzelne Seiten drucken, aber nicht den gesamten
Scan herunterladen. In `download/` befindet sich ein Script um mit `wget(1)`
und ImageMagick `convert(1)` das ganze Buch herunterzuladen und in ein PDF
umzuwandeln.

```bash
download/download.sh
```

Dabei erhält man dann eine Datei `1320989187.pdf`.



## OCR

Um den Text zu extrahieren wurde [Google Cloud Vision OCR][glcoud-ocr]
verwendet, da die Qualität des mit Schreibmaschine geschriebenen Textes recht
schlecht ist (imperfektionen im Druck, durchscheinende Seiten, alte
Rechtschreibung, handschriftliche Ergänzungen, ...).


1. Erstelle einen _Bucket_ auf Google Cloud Storage und lade das PDF hoch
2. Passe die Buckt-ID in `ocr/requst.json` an.
3. Verwende `ocr/ocr.sh` um den Request an die Google Cloud API zu schicken.
4. Nach einiger Zeit sollte in dem entsprechenden Bucket das Resultat in Form
   von einer JSON-Datei pro PDF Seite zur Verfügung stellen
5. Den gesamten Resultat-Ordner herunderladen
6. In lesbaren Text `nebel.ocr.txt` umwandeln mit
   ```bash
   cd ocr
   python3 convert.py
   ```
   Dies lädt den erkannten Text aus den einzelnen Dateien und bereinigt den
   Text etwas, sodass jeder Sprechteil auf einer einzelnen Zeile landet und
   der oder die Sprecherin in Großbuchstaben gesetzt ist.

Als open-source Alternative könnte man auch [OCRmyPDF][ocrmypdf] (mit deutschem
[`tesseract-lang`][tesseract-lang]) testen.


## Typesetting

Das `ocr/convert.py` erzeugt außerdem eine Datei `nebel.ocr.tex`. Diese kann
mit einer speziellen LaTeX Klasse gesetzt werden, um ein praktisches PDF für
Theaterproduktionen zu erhalten. Dabei werden weitere Textersetzungen und
umformatierungen vorgenommen.

Um den Text zu setzen, benötigt man [LaTeX][latex], mit
[`ebgaramond`][ebgaramond] und [KOMA-Script][komascript]. Am einfachsten geht
das mit [`latexmk`][latexmk].

```bash
latexmk -pdflua nebel.tex
```

Dann erhält man die Datie `nebel.tex`. Die noch nicht überarbeitete Version
liegt unter [`nebel.original.pdf`](./nebel.original.pdf)


[pdf-original]: https://github.com/phistep/nebel/blob/main/nebel.original.pdf?raw=true
[dnb]: https://dnb.de/
[dnb-nebel]: https://portal.dnb.de/opac.htm?method=simpleSearch&cqlMode=true&query=idn%3D1320989187
[dnb-nebel-viewer]: https://portal.dnb.de/bookviewer/ui/view/1320989187/
[gcloud-ocr]: https://cloud.google.com/vision/docs/ocr
[ocrmypf]: https://ocrmypdf.readthedocs.io/
[tesseract-lang]: https://formulae.brew.sh/formula/tesseract-lang
[latex]: https://www.latex-project.org
[komascript]: https://komascript.de
[ebgaramond]: https://ctan.org/tex-archive/fonts/ebgaramond
[latexmk]: https://www.cantab.net/users/johncollins/latexmk/
