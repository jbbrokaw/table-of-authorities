#!/usr/bin/env python
from __future__ import unicode_literals
import re

ALLOWED_SYMBOLS = {'&'}
ABBREVIATIONS = {'Co.',
                 'U.S.',
                 'Corp.',
                 'Inc.',
                 'Dist.'}
LOWERCASE_WORDS = {'the', 'a', 'an', 'and', 'of'}
CLAUSE_ENDERS = {'.', ';'}


def title_word(word):
    if word[0].isupper() and (word[-1] not in CLAUSE_ENDERS):
        return True
    if word in ALLOWED_SYMBOLS:
        return True
    if word in LOWERCASE_WORDS:
        return True
    if word in ABBREVIATIONS:
        return True
    return False


def find_v_cites(text):
    words = text.split()
    date_re = re.compile('\d{4}\)')

    while 'v.' in words:
        v_index = words.index('v.')
        begin_index = v_index - 1
        while (begin_index >= 0) and title_word(words[begin_index]):
            begin_index -= 1
        begin_index = min(v_index - 1, begin_index + 1)
        end_index = v_index + 1
        while (end_index < len(words)) and \
                (date_re.search(words[end_index]) is None):
            end_index += 1
        cite_string = " ".join(words[begin_index:end_index + 1])
        if date_re.search(cite_string):
            print cite_string
        words = words[v_index + 1:]


def find_in_re_cites(text):
    words = text.split()
    date_re = re.compile('\d{4}\)')
    while 're' in words:
        re_index = words.index('re')
        if (re_index < 1) or (words[re_index - 1] != 'In'):
            words = words[re_index + 1:]
            continue
        end_index = re_index + 1
        while (end_index < len(words)) and \
                (date_re.search(words[end_index]) is None):
            end_index += 1
        cite_string = " ".join(words[re_index - 1:end_index + 1])
        if date_re.search(cite_string):
            print cite_string
        words = words[re_index + 1:]


def main():
    from sys import argv
    from docx import Document

    if len(argv) < 2:
        print "Usage: python parse.py [file.docx]"
        return

    filename = argv[1]
    file_name_parts = filename.split('.')
    if (len(file_name_parts) < 2) or (file_name_parts[1] != 'docx'):
        print "Only .docx files supported currently"

    doc = Document(filename)
    for paragraph in doc.paragraphs:
        find_v_cites(paragraph.text)
        find_in_re_cites(paragraph.text)


if __name__ == '__main__':
    main()
