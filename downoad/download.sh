#!/bin/bash

BOOK="1320989187"
PAGES=117

mkdir -p "$BOOK"
for PAGE in $(seq 1 "$PAGES"); do
    FILE="${BOOK}/$(printf '%03d' $PAGE).jpg"
    if [[ ! -f "$FILE" ]]; then
        wget \
            "https://portal.dnb.de/bookviewer/ui/view/${BOOK}/img/page/${PAGE}/p.jpg" \
            --output-document="$FILE"
    fi
done

magick convert "${BOOK}/*.jpg" "${BOOK}.pdf"

# TODO correct oage numbers (roman cover etc)

# PDF /Type /Catalog
# /PageLabels << /Nums [ 0 << /P (cover) >>
#                        % labels 1st page with the string "cover"
#                        1 << /S /r >>
#                        % numbers pages 2-7 in small roman numerals
#                        8 << /S /D >>
#                        % numbers pages 8-x in decimal arabic numerals
#                      ]
#             >>
