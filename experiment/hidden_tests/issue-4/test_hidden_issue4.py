"""Hidden acceptance tests for issue 4 (render_toc_ul ordered=True)."""
from mistune.toc import render_toc_ul

ITEMS = [(1, "a", "A"), (2, "b", "B"), (2, "c", "C"), (1, "d", "D")]


def test_ordered_uses_ol_at_top_level():
    html = render_toc_ul(ITEMS, ordered=True)
    assert html.startswith("<ol>")
    assert "<ul>" not in html


def test_ordered_nested_levels_use_ol():
    html = render_toc_ul(ITEMS, ordered=True)
    assert html.count("<ol>") == 2 and html.count("</ol>") == 2
    assert '<a href="#b">B</a>' in html


def test_ordered_same_structure_as_unordered():
    a = render_toc_ul(ITEMS, ordered=True)
    b = render_toc_ul(ITEMS)
    assert a.replace("<ol>", "<ul>").replace("</ol>", "</ul>") == b


def test_default_unchanged():
    assert render_toc_ul(ITEMS).startswith("<ul>")
