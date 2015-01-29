#!/usr/bin/env python
from __future__ import unicode_literals
import re

ALLOWED_SYMBOLS = {'&'}
ABBREVIATIONS = {'Co.',
                 'U.S.',
                 'Corp.',
                 'Inc.',
                 'Dist.'}


def find_full_cites(doc):
    date_re = re.compile('\d{4}\)')
    for (pnum, paragraph) in enumerate(doc.paragraphs):
        for (rnum, run) in enumerate(paragraph.runs):
            if ('v.' in run.text):
                run_start = rnum
                while (run_start >= 0) and \
                        (paragraph.runs[run_start].italic or
                            paragraph.runs[run_start].style == "Emphasis"):
                    run_start -= 1
                run_start = min(rnum, run_start + 1)
                run_end = rnum
                while (run_end < len(paragraph.runs)) and \
                        (date_re.search(paragraph.runs[run_end].text) is None):
                    run_end += 1
                cite_string = "".join(
                    [run.text for run in paragraph.runs[run_start:run_end + 1]]
                )
                if date_re.search(cite_string):
                    print cite_string


def find_cites_by_word(text):
    words = text.split()
    date_re = re.compile('\d{4}\)')
    if 'v.' not in words:
        return

    v_index = words.index('v.')
    begin_index = v_index - 1
    while (words[begin_index][-1] != '.') or \
            (words[begin_index] in ABBREVIATIONS):
        begin_index += 1
    begin_index = min(v_index - 1, begin_index + 1)
    end_index = v_index + 1
    while (end_index < len(words)) and \
            (date_re.search(words[end_index]) is None):
        end_index += 1
    cite_string = " ".join(words[begin_index:end_index + 1])
    if date_re.search(cite_string):
        print cite_string
