import json
import os
import re
from pprint import pprint

INPUT_DIR="1320989187-ocr"
OUTPUT_FILE="nebel.txt"


def pad_filename(filename):
    # Regular expression to match the pattern 'output-x-to-y.json'
    pattern = r'output-(\d+)-to-(\d+).json'
    basename = os.path.basename(filename)
    match = re.match(pattern, basename)
    if match:
        num1 = int(match.group(1))
        num2 = int(match.group(2))
        new_basename = f'output-{num1:03d}-to-{num2:03d}.json'
        new_filename = os.path.join(os.path.dirname(filename),
                                    new_basename)
        return new_filename
    return filename


def rename_padded_for_sort(files):
    for filename in files:
        new_filename = pad_filename(filename)
        if new_filename != filename:
            os.rename(filename, new_filename)
            print(f'Renamed: {filename} -> {new_filename}')


def load_text(files: list[str]) -> str:
    content = ""
    for filename in sorted(files):
        #print(f"\n:: {filename}")

        with open(filename) as f:
            payload = json.load(f)

        for response in payload['responses']:
            try:
                text = response['fullTextAnnotation']['text']
            except KeyError as e:
                # no text recognized on page
                continue

            #print(f"{len(text)=}")
            #print(text[:2*47] + '…')
            content += text
    return content


def clean_text(text: str) -> str:
    # remove preamble
    text = text[text.find("I. A K T"):]
    # remove page numbers
    text = re.sub(r'- ?\d+ ?-?', r'', text)
    # restore hyphenated words
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    # resolve typewriter linebreaks
    text = text.replace('\n', '')
    # ever speaker on its own line
    text = re.sub(r'([A-Z ]{3,}: )', r'\n\1', text)
    # common typos
    text = re.sub(r'\wAe', r'Ä', text)
    text = re.sub(r'\wOe', r'Ö', text)
    text = re.sub(r'\wUe', r'Ü', text)
    text = text.replace('KATERINE', 'KATHERINE')
    text = text.replace('Katerine', 'Katherine')
    text = text.replace('BARAARA', 'BARBARA')
    text = text.replace('Baraara', 'Barbara')
    text = re.sub(r'(?<!GENERAL)DIREKTOR', r'GENERALDIREKTOR', text)
    text = re.sub(r'^\W* ?DIREKTOR', r'GENERALDIREKTOR', text)
    text = re.sub(r'[^T]HOMSEN', r'THOMSEN', text)
    text = text.replace('Homsen', 'Thomsen')
    text = re.sub(r'[^A]LEXIS', r'ALEXIS', text)
    text = text.replace('DIE KINDER:', 'KINDER:')
    text = text.replace('Die KINDER:', 'KINDER:')
    text = text.replace("Ein grosser Junge:", "JUNGE1:")
    text = text.replace("Der erste grosse Junge:", "JUNGE1:")
    text = text.replace("Erster grosser Junge:", "JUNGE1:")
    text = text.replace("Ein ganz kleiner Junge:", "JUNGE2:")
    text = text.replace("Ein kleiner Junge:", "JUNGE3:")
    text = text.replace("Der kleine Junge:", "JUNGE3:")
    text = text.replace("Zweiter grosser Junge: ", "JUNGE4:")
    text = text.replace("Ein zweiter grosser Junge:", "JUNGE4:")
    text = text.replace("Ein kleines Mädchen:", "MAEDCHEN1:")
    text = text.replace("Das erste kleine Mädchen:", "MAEDCHEN1:")
    text = text.replace("Das kleine Mädchen:", "MAEDCHJEN1:")
    text = text.replace("Ein zweites kleines Mädchen:" , "MAEDCHEN2:")
    text = text.replace("Zweites kleines Mädchen:", "MEADCHEN2:")
    text = text.replace("Ein grösseres Mädchen:", "MAEDCHEN3:")
    text = text.replace("Ein grosses Mädchen:" , "MAEDCHEN3:")
    text = text.replace("Das erste grosse Mädchen:", "MAEDCHEN3:")
    text = text.replace("Erstes grosses Mädchen:", "MAEDCHEN3:")
    text = text.replace("Das erste grosse Mädchen::", "MAEDCHEN3:")
    text = text.replace("Zweites grosses Mädchen:" , "MAEDCHEN4:")
    text = text.replace("Das zweite grosse Mädchen:", "MAEDCHEN4:")
    text = text.replace("Zweites grosses Mädchen:", "MAEDCHEN4:")
    return text


def texify(text: str) -> str:
    # SPEAKER: -> \Speaker\n
    # while modifying, the already generated matches are becoming
    # outdated. first title-case then texify later
    # TODO loop with start and do all transformations in one place
    for match in re.finditer('([A-Z0-9 ]{3,}):', text):
        name = match.group(1)
        start, end = match.span(1)
        text = text[:start] + name.title() + text[end:]
    text = re.sub(r'((([A-Z][a-z0-9]+) ?)+): ?', r'\n\\\1\n', text)
    text = text.replace(r'\Erster Mann', r'\ErsterMann')
    text = text.replace(r'\Zweiter Mann', r'\ZweiterMann')
    text = text.replace(r'\Die Kinder', r'\Kinder')
    text = re.sub(r'\\Maedchen([0-9]+)', r'\n\\Maedchen{\1}', text)
    text = re.sub(r'\\Junge([0-9]+)', r'\n\\Junge{\1}', text)

    text = text.replace(r'\Die Beiden Maenner',
                        ('\\ErsterMann \\direction{gemeinsam}\n'
                         '\\ZweiterMann'))
    text = text.replace(r'\Die Leute', r'\Leute')


    # (...) -> \direction{...}
    text = re.sub(r'\(([^(]+)\)', r'\\direction{\1}', text)

    # I. A K T -> \end{play}\n\begin{play}
    text = re.sub(r'([IV]+)\. A K T',
                  r'\n\\end{play}\n\n\\scene{\1}\n\\begin{play}\n',
                  text)

    text = text.replace('...', r'\ldots{}')
    text = text.replace(' - ', ' --- ')

    return text


def main():
    # damn gcloud names it `output-1-to-1.json` and python doesn't
    # know how to sort that
    filenames = os.listdir(INPUT_DIR)
    files = [os.path.join(INPUT_DIR, f) for f in filenames]
    rename_padded_for_sort(files)
    text = load_text(files)
    raw_file = os.path.splitext(OUTPUT_FILE)[0] + '.ocr.txt'
    with open(raw_file, 'w') as f:
        f.write(text)


    text = clean_text(text)
    # print(text[:750])
    with open(OUTPUT_FILE, 'w') as f:
        f.write(text)

    print("\n\n- tex -------\n")
    latex = texify(text)
    print(latex[:750])
    latex_file = os.path.splitext(OUTPUT_FILE)[0] + '.ocr.tex'
    with open(latex_file, 'w') as f:
        f.write(latex)



if __name__== '__main__':
    main()
