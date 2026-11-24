# test_report.md (issue #5)

**Full suite:** FAIL: `5 failed, 1334 passed, 158 subtests passed in 5.43s`

## Workers (this round)
| Worker | Criteria | Status | File | Tests | Alone | Tokens |
|---|---|---|---|---|---|---|
| c1r1 | AC-FR-001-1, AC-FR-002-1 | complete | `tests/test_autose_issue_5_fr001.py` | 2 | 2 passed in 0.02s | 820,783 |
| c2r1 | AC-FR-003-1, AC-FR-004-1 | complete | `tests/test_autose_issue_5_fr003.py` | 2 | 2 passed in 0.02s | 2,176,528 |
| c3r1 | AC-FR-005-1 | complete | `tests/test_autose_issue_5_fr005.py` | 2 | 2 passed in 0.02s | 381,954 |
| c4r1 | AC-NFR-001-1 | complete | `tests/test_autose_issue_5_nfr001.py` | 1 | 1 passed in 0.03s | 743,084 |
| e2er1 | e2e (regression) | complete | `tests/test_autose_issue_5_e2e.py` | 5 | 5 passed in 0.03s | 608,975 |

## Acceptance criteria → tests
| AC | Tests |
|---|---|
| AC-FR-001-1 | tests/test_autose_issue_5_e2e.py::test_inline_double_dollar_math_and_nfr<br>tests/test_autose_issue_5_fr001.py::test_math_inline_rendering |
| AC-FR-002-1 | tests/test_autose_issue_5_e2e.py::test_block_math_and_single_dollar_math<br>tests/test_autose_issue_5_fr001.py::test_math_block_rendering |
| AC-FR-003-1 | tests/test_autose_issue_5_e2e.py::test_block_math_and_single_dollar_math<br>tests/test_autose_issue_5_fr003.py::test_ac_fr_003_1<br>tests/test_autose_issue_5_fr003.py::test_ac_fr_003_1 |
| AC-FR-004-1 | tests/test_autose_issue_5_e2e.py::test_backtick_math_and_currency_rejection<br>tests/test_autose_issue_5_fr003.py::test_ac_fr_004_1<br>tests/test_autose_issue_5_fr003.py::test_ac_fr_004_1 |
| AC-FR-005-1 | tests/test_autose_issue_5_e2e.py::test_backtick_math_and_currency_rejection<br>tests/test_autose_issue_5_fr005.py::test_ac_fr_005_1<br>tests/test_autose_issue_5_fr005.py::test_ac_fr_005_1<br>tests/test_autose_issue_5_fr005.py::test_ac_fr_005_1_markdown_renderer<br>tests/test_autose_issue_5_fr005.py::test_ac_fr_005_1_markdown_renderer |
| AC-NFR-001-1 | tests/test_autose_issue_5_e2e.py::test_inline_double_dollar_math_and_nfr<br>tests/test_autose_issue_5_nfr001.py::test_inline_double_dollar_math_html_validation |

## Stage 4 check (orchestrator)

**FAIL**

- test suite failed: 5 failed, 1334 passed, 158 subtests passed in 5.43s


## Failing output

```
= "Start with $a+b$.\n\n$$\n\\sum_{i=1}^n i = \\frac{n(n+1)}{2}\n$$\n\nMiddle with $$x^2 + y^2 = z^2$$ and end."
        result = md(text)
        self.assertIn(r'<span class="math">\(a+b\)</span>', result)
        self.assertIn('<div class="math">$$', result)
>       self.assertIn(r'<span class="math">\(x^2 + y^2 = z^2\)</span>', result)
E       AssertionError: '<span class="math">\\(x^2 + y^2 = z^2\\)</span>' not found in '<p>Start with <span class="math">\\(a+b\\)</span>.</p>\n<div class="math">$$\n\\sum_{i=1}^n i = \\frac{n(n+1)}{2}\n$$</div>\n<p>Middle with <div class="math">$$\nx^2 + y^2 = z^2\n$$</div>\n and end.</p>\n'

tests/test_autose_issue_5_e2e.py:84: AssertionError
__________________________ test_math_inline_rendering __________________________

    def test_math_inline_rendering():
        r"""AC-FR-001-1: Given Markdown input 'The famous relation $$E=mc^2$$ changed physics.', when parsed with Markdown renderer using the math plugin, then exact observable output is '<p>The famous relation <span class="math">\(E=mc^2\)</span> changed physics.</p>\n'."""
        md = create_markdown(plugins=["math"])
        text = "The famous relation $$E=mc^2$$ changed physics."
        expected = r'<p>The famous relation <span class="math">\(E=mc^2\)</span> changed physics.</p>'+'\n'
>       assert md(text) == expected
E       assert '<p>The famou...hysics.</p>\n' == '<p>The famou...hysics.</p>\n'
E         
E         - <p>The famous relation <span class="math">\(E=mc^2\)</span> changed physics.</p>
E         + <p>The famous relation <div class="math">$$
E         + E=mc^2
E         + $$</div>
E         +  changed physics.</p>

tests/test_autose_issue_5_fr001.py:9: AssertionError
___ TestNFR001MathValidation.test_inline_double_dollar_math_html_validation ____

self = <tests.test_autose_issue_5_nfr001.TestNFR001MathValidation testMethod=test_inline_double_dollar_math_html_validation>

    def test_inline_double_dollar_math_html_validation(self) -> None:
        """AC-NFR-001-1: Metric: HTML validation errors | Threshold: 0 validation errors on pages with inline double-dollar math | Conditions: Parsed output rendered in HTML document | Method: HTML parser inspection"""
        md = create_markdown(plugins=["math"])
    
        markdown_texts = [
            "Here is some text with $$x^2 + y^2 = z^2$$ inline math.",
            "$$a + b$$ is at the beginning of a paragraph.",
            "At the end of a paragraph: $$c + d$$",
            "Multiple expressions: $$1 + 1 = 2$$ and $$2 + 2 = 4$$ in one line.",
        ]
    
        for text in markdown_texts:
            html_output = md(text)
            full_doc = f"<!DOCTYPE html><html><head><title>Math Test</title></head><body>{html_output}</body></html>"
    
            # Verify that inline math is rendered as span.math, not div.math
>           self.assertIn('<span class="math">', html_output)
E           AssertionError: '<span class="math">' not found in '<p>Here is some text with <div class="math">$$\nx^2 + y^2 = z^2\n$$</div>\n inline math.</p>\n'

tests/test_autose_issue_5_nfr001.py:44: AssertionError
=========================== short test summary info ============================
FAILED tests/test_autose_issue_5_e2e.py::TestAutoseIssue5E2E::test_inline_double_dollar_math_and_nfr - AssertionError: '<p>T[15 chars]ion <div class="math">$$\nE=mc^2\n$$</div>\n c[17 chars]p>\n' != '<p>T[15 chars]ion <span class="math">\\(E=mc^2\\)</span> cha[15 chars]p>\n'
+ <p>The famous relation <span class="math">\(E=mc^2\)</span> changed physics.</p>
- <p>The famous relation <div class="math">$$
- E=mc^2
- $$</div>
-  changed physics.</p>
FAILED tests/test_autose_issue_5_e2e.py::TestAutoseIssue5E2E::test_regression_combined_plugins_and_lists - AssertionError: '<span class="math">\\(E=mc^2\\)</span>' not found in '<ul>\n<li>Formula: <div class="math">$$\nE=mc^2\n$$</div>\n</li>\n<li>Price: $51,300</li>\n<li><del>Strikethrough</del></li>\n</ul>\n'
FAILED tests/test_autose_issue_5_e2e.py::TestAutoseIssue5E2E::test_regression_complex_document_mixed_math - AssertionError: '<span class="math">\\(x^2 + y^2 = z^2\\)</span>' not found in '<p>Start with <span class="math">\\(a+b\\)</span>.</p>\n<div class="math">$$\n\\sum_{i=1}^n i = \\frac{n(n+1)}{2}\n$$</div>\n<p>Middle with <div class="math">$$\nx^2 + y^2 = z^2\n$$</div>\n and end.</p>\n'
FAILED tests/test_autose_issue_5_fr001.py::test_math_inline_rendering - assert '<p>The famou...hysics.</p>\n' == '<p>The famou...hysics.</p>\n'
  
  - <p>The famous relation <span class="math">\(E=mc^2\)</span> changed physics.</p>
  + <p>The famous relation <div class="math">$$
  + E=mc^2
  + $$</div>
  +  changed physics.</p>
FAILED tests/test_autose_issue_5_nfr001.py::TestNFR001MathValidation::test_inline_double_dollar_math_html_validation - AssertionError: '<span class="math">' not found in '<p>Here is some text with <div class="math">$$\nx^2 + y^2 = z^2\n$$</div>\n inline math.</p>\n'
5 failed, 1334 passed, 158 subtests passed in 5.43s

```


## Why this stage stopped

test suite failed: 5 failed, 1334 passed, 158 subtests passed in 5.43s (after 1 attempt(s))

Run: https://github.com/QasimANaik/mistune/actions/runs/45374180590
