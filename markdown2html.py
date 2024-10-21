#!/usr/bin/python3
""" This script converts markdown to HTML.
"""
import sys
import re
import hashlib


def convert(markdownFile, htmlFile):
    """ Converts markdown to HTML.
    """
    try:
        with open(markdownFile, 'r') as r:
            with open(htmlFile, 'w') as w:
                text = r.read()

                # Basic Markdown to HTML replacements
                text = re.sub(
                        r'\*\*(.*?)\*\*', r'<b>\1</b>', text
                        )
                text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)

                #  [[string]] to md5 hash
                text = re.sub(r'\[\[(.*?)\]\]', lambda m: f'{hashlib.md5
                              (m.group(1).encode()).hexdigest()}', text)

                #  ((string)) to remove all occurrences of the character 'c'
                text = re.sub(r'\(\((.*?)\)\)', lambda m: f'{re.sub("c",
                              "", m.group(1), flags=re.IGNORECASE)}', text)
                textLines = text.splitlines()
                i = 0
                while i < len(textLines):
                    line = textLines[i]
                    if line == '':
                        i += 1
                        continue

                    # Headers
                    if line.startswith('###### '):
                        w.write('<h6>{}</h6>\n'.format(line[7:]))
                    elif line.startswith('##### '):
                        w.write('<h5>{}</h5>\n'.format(line[6:]))
                    elif line.startswith('#### '):
                        w.write('<h4>{}</h4>\n'.format(line[5:]))
                    elif line.startswith('### '):
                        w.write('<h3>{}</h3>\n'.format(line[4:]))
                    elif line.startswith('## '):
                        w.write('<h2>{}</h2>\n'.format(line[3:]))
                    elif line.startswith('# '):
                        w.write('<h1>{}</h1>\n'.format(line[2:]))

                    # Unordered list (- )
                    elif line.startswith('- '):
                        listStr = ""
                        for j in range(i, len(textLines)):
                            if textLines[j].startswith('-'):
                                listStr += "<li>{}</li>\n".format(
                                        textLines[j][2:])
                            else:
                                break
                        w.write("<ul>\n{}</ul>\n".format(listStr))
                        i = j

                    # Ordered list (* )
                    elif line.startswith('* '):
                        listStr = ""
                        for j in range(i, len(textLines)):
                            if textLines[j].startswith('*'):
                                listStr += "<li>{}</li>\n".format(
                                        textLines[j][2:])
                            else:
                                break
                        w.write("<ol>\n{}</ol>\n".format(listStr))
                        i = j

                    # Paragraphs
                    else:
                        listStr = ""
                        for j in range(i, len(textLines)):
                            if j+1 < len(textLines) and textLines[j + 1] == '':
                                listStr += "{}".format(textLines[j])
                                break
                            elif j+1 >= len(textLines):
                                listStr += "{}".format(textLines[j])
                                break
                            else:
                                listStr += "{}\n<br/>\n".format(textLines[j])
                        w.write("<p>\n{}\n</p>\n".format(listStr))
                        i = j
                    i += 1
    except Exception as e:
        print("Missing {}".format(markdownFile), file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
