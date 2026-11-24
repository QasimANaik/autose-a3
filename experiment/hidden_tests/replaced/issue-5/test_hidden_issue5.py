"""Hidden acceptance tests for issue 5 (vague: 'math breaks my page layout').

Reasonable interpretation: `$$...$$` written inside a sentence must not produce a
block element (<div>) inside a <p>; the paragraph stays one paragraph and the
equation is still emitted for MathJax. Display math on its own lines is unchanged.
"""
import re

import mistune

md = mistune.create_markdown(plugins=["math"])
SRC = "The famous relation $$E=mc^2$$ changed physics."


def test_no_block_element_inside_paragraph():
    html = md(SRC)
    for p in re.findall(r"<p>.*?</p>", html, re.S):
        assert "<div" not in p, html


def test_sentence_stays_one_paragraph_with_equation():
    html = md(SRC)
    assert html.count("<p>") == 1
    assert "E=mc^2" in html
    assert "changed physics.</p>" in html


def test_block_math_on_own_lines_unchanged():
    assert md("$$\nE=mc^2\n$$") == '<div class="math">$$\nE=mc^2\n$$</div>\n'


def test_single_dollar_inline_unchanged():
    assert md("inline $x^2$ ok") == '<p>inline <span class="math">\\(x^2\\)</span> ok</p>\n'
