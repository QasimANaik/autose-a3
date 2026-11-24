"""Hidden acceptance tests for issue #18 (vague: 'some links in our chat logs are not clickable').

Reasonable interpretation (GitHub's extended autolinks): with plugins=["url"], an address starting with
`www.` becomes a link with an http(s) scheme added; trailing sentence punctuation is not part of it;
links that already work, inline code and non-addresses are unchanged.
"""
import re

import mistune

md = mistune.create_markdown(plugins=["url"])


def test_www_address_becomes_link():
    html = md("docs are at www.example.com/docs now")
    assert re.search(r'<a href="https?://www\.example\.com/docs">www\.example\.com/docs</a> now', html), html


def test_www_trailing_punctuation_excluded():
    html = md("see www.example.com/docs, or later.")
    assert re.search(r'href="https?://www\.example\.com/docs">www\.example\.com/docs</a>,', html), html


def test_existing_https_links_unchanged():
    assert md("the old page https://example.com/old") == (
        '<p>the old page <a href="https://example.com/old">https://example.com/old</a></p>\n')


def test_code_and_non_addresses_unchanged():
    assert md("`www.example.com` and wwwexample.com") == (
        "<p><code>www.example.com</code> and wwwexample.com</p>\n")
