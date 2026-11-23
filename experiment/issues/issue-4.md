<!-- title: render_toc_ul: allow a numbered (ordered) table of contents -->
I'm generating a manual with `add_toc_hook` + `render_toc_ul`. Our style guide wants the table of contents numbered (1, 1.1, 1.2, 2 …), which in HTML/CSS means `<ol>` lists, but `render_toc_ul` always produces `<ul>`.

Right now I copy the whole function into my project just to change `ul` to `ol`, and that copy has already drifted from upstream.

Proposal: an optional keyword, e.g.

```python
from mistune.toc import render_toc_ul
html = render_toc_ul(state.env["toc_items"], ordered=True)
```

which renders exactly the same structure but with `<ol>` instead of `<ul>` at every nesting level. Without the keyword nothing changes.
