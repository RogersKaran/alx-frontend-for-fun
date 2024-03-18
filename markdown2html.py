#!/usr/bin/python3
"""
Markdown to HTML Converter
"""

import sys
import re

def parse_headings(line):
    """
    Parse Markdown headings to HTML
    """
    headings = ["#", "##", "###", "####", "#####", "######"]
    for i, heading in enumerate(headings, start=1):
        if line.startswith(heading):
            return f"<h{i}>{line[len(heading):].strip()}</h{i}>"
    return line

def parse_unordered_listing(line):
    """
    Parse Markdown unordered listing to HTML
    """
    if line.startswith("- "):
        return "<ul>" + f"<li>{line[2:].strip()}</li>"
    elif line.strip() == "":
        return "</ul>"
    return line

def parse_ordered_listing(line):
    """
    Parse Markdown ordered listing to HTML
    """
    if line.startswith("* "):
        return "<ol>" + f"<li>{line[2:].strip()}</li>"
    elif line.strip() == "":
        return "</ol>"
    return line

def parse_paragraph(line):
    """
    Parse Markdown paragraph to HTML
    """
    if line.strip() != "":
        return f"<p>{line}</p>"
    return line

def parse_bold_and_emphasis(line):
    """
    Parse Markdown bold and emphasis to HTML
    """
    line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
    line = re.sub(r"__(.*?)__", r"<em>\1</em>", line)
    return line

def parse_md5_and_remove_c(line):
    """
    Parse markdown [[Hello]] to MD5 hash and ((Hello Chicago)) to remove all c
    """
    line = re.sub(r"\[\[(.*?)\]\]", lambda x: hashlib.md5(x.group(1).encode()).hexdigest(), line)
    line = re.sub(r"\(\((.*?)\)\)", lambda x: x.group(1).replace('c', '').replace('C', ''), line)
    return line

def convert_markdown_to_html(markdown_file, html_file):
    """
    Converts Markdown to HTML
    """
    try:
        with open(markdown_file, 'r') as md_file:
            lines = md_file.readlines()
    except FileNotFoundError:
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    with open(html_file, 'w') as html_file:
        for line in lines:
            line = parse_headings(line)
            line = parse_unordered_listing(line)
            line = parse_ordered_listing(line)
            line = parse_bold_and_emphasis(line)
            line = parse_md5_and_remove_c(line)
            line = parse_paragraph(line)
            html_file.write(line + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]
    convert_markdown_to_html(markdown_file, html_file)

