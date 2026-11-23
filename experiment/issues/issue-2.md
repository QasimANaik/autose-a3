<!-- title: url plugin cuts off Wikipedia links and grabs the question mark at the end -->
We use `plugins=["url"]` so plain URLs in user comments become links. Two problems keep coming up:

1. Wikipedia links with parentheses get cut:

```python
md = mistune.create_markdown(plugins=["url"])
md("see https://en.wikipedia.org/wiki/Python_(programming_language) for details")
```
gives
```html
<p>see <a href="https://en.wikipedia.org/wiki/Python_(programming_language">https://en.wikipedia.org/wiki/Python_(programming_language</a>) for details</p>
```
so the link goes to a 404 page.

2. When someone asks a question ending with a link, the `?` becomes part of the URL:

```python
md("did you try https://example.com/docs?")
# <a href="https://example.com/docs?">https://example.com/docs?</a>
```

Same with `!`. A period or comma at the end is already handled correctly, so I guess `?` and `!` were just missed. GitHub keeps balanced parentheses in the URL and drops trailing punctuation like `?` and `!`.
