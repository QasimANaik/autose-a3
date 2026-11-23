"""Hidden acceptance tests for issue 1 (table rows with missing/extra cells). Kept outside the fork."""
import re

import mistune

md = mistune.create_markdown(plugins=["table"])


def test_short_row_padded_with_empty_cell():
    html = md("| Name | Role |\n|------|------|\n| Ana |")
    assert "<table>" in html
    assert "<td>Ana</td>" in html
    assert len(re.findall(r"<td[^>]*>", html)) == 2
    assert re.search(r"<td[^>]*></td>", html)


def test_extra_cell_is_dropped():
    html = md("| Name | Role |\n|------|------|\n| Ana | Dev | extra |")
    assert "<table>" in html
    assert "<td>Ana</td>" in html and "<td>Dev</td>" in html
    assert "extra" not in html


def test_one_bad_row_keeps_whole_table():
    src = "| a | b |\n|---|---|\n| 1 | 2 |\n| 3 |\n| 5 | 6 |"
    html = md(src)
    assert html.count("<table>") == 1
    assert html.count("<tr>") == 4  # header + 3 body rows
    assert "<td>6</td>" in html


def test_padded_cell_keeps_column_alignment():
    html = md("| a | b |\n|:--|--:|\n| x |")
    assert '<td style="text-align:right"></td>' in html
