#!/usr/bin/python3
""" this script converts markdown to HTML
"""
import sys


def convert(markdownFile, htmlFile):
    """ Cinverts markdown to HTML
    """
    try:
        with open(markdownFile, 'r') as r:
            with open(htmlFile, 'w') as w:
                text = r.read()
                w.write(text)
    except Exception as e:
        print("Missing {}".format(markdownFile), file=sys.stderr
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html",
          file=sys.stderr)
        sys.exit(1)

    markdownFile = sys.argv[1]
    htmlFile = sys.argv[2]
    convert(markdownFile, htmlFile)
