"""Hidden acceptance tests for issue 2 (url plugin: balanced parens, trailing ? and !)."""
import mistune

md = mistune.create_markdown(plugins=["url"])
WIKI = "https://en.wikipedia.org/wiki/Python_(programming_language)"


def test_balanced_parentheses_kept():
    html = md(f"see {WIKI} for details")
    assert f'href="{WIKI}"' in html
    assert f">{WIKI}</a> for details" in html


def test_trailing_question_mark_excluded():
    html = md("did you try https://example.com/docs?")
    assert 'href="https://example.com/docs"' in html
    assert "</a>?" in html


def test_trailing_exclamation_excluded():
    html = md("look at https://example.com/new!")
    assert 'href="https://example.com/new"' in html
    assert "</a>!" in html


def test_unbalanced_closing_paren_still_excluded():
    # regression guard: prose parentheses around a URL must not be swallowed
    html = md("(see https://example.com/page)")
    assert 'href="https://example.com/page"' in html
    assert "</a>)" in html
