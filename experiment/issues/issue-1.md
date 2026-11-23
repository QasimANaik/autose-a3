<!-- title: Table disappears completely if one row has a missing or extra cell -->
Hi, I'm using mistune 3 with the `table` plugin to render README-style docs in our internal wiki.

When one of the rows in a table has fewer cells than the header (someone forgot a trailing `|` value), or has one cell too many, the **whole table** is not rendered. Instead the raw pipes are dumped into a paragraph:

```python
import mistune
md = mistune.create_markdown(plugins=["table"])
print(md("| Name | Role |\n|------|------|\n| Ana |"))
```

Output:

```html
<p>| Name | Role |
|------|------|
| Ana |</p>
```

Same thing with `| Ana | Dev | extra |` as the row.

GitHub renders both of these as a normal table (the short row just gets an empty cell, the extra cell is dropped), and so do the other Markdown tools we used before. Our docs are edited by many people, so one sloppy row breaking a 40-row table is pretty painful.

Python 3.12, mistune from main. Thanks!
