"""Hidden acceptance tests for issue 3 (HTMLRenderer link_rel option)."""
import re

import mistune


def _md(**kw):
    return mistune.create_markdown(renderer=mistune.HTMLRenderer(**kw), plugins=["url"])


def _rel_of_first_a(html):
    m = re.search(r"<a\b[^>]*>", html)
    assert m, html
    r = re.search(r'rel="([^"]*)"', m.group(0))
    return r.group(1) if r else None


def test_inline_link_gets_rel():
    html = _md(link_rel="nofollow ugc")("[site](https://example.com)")
    assert 'href="https://example.com"' in html
    assert _rel_of_first_a(html) == "nofollow ugc"


def test_autolink_and_plain_url_get_rel():
    md = _md(link_rel="nofollow")
    assert _rel_of_first_a(md("<https://example.com>")) == "nofollow"
    assert _rel_of_first_a(md("go to https://example.com now")) == "nofollow"


def test_images_unaffected():
    html = _md(link_rel="nofollow")("![logo](https://example.com/a.png)")
    assert "rel=" not in html


def test_default_output_unchanged():
    html = _md()("[site](https://example.com)")
    assert html == '<p><a href="https://example.com">site</a></p>\n'
