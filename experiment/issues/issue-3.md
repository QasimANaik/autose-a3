<!-- title: Option to add rel="nofollow" to rendered links -->
We render user-generated content (forum posts) with mistune. For SEO-spam reasons we need every link to carry `rel="nofollow ugc"`. Right now we post-process the HTML with a regex, which is fragile.

Could the HTML renderer get an option for this? Something like:

```python
renderer = mistune.HTMLRenderer(link_rel="nofollow ugc")
md = mistune.create_markdown(renderer=renderer, plugins=["url"])
md("[site](https://example.com)")
# <p><a href="https://example.com" rel="nofollow ugc">site</a></p>
```

It should apply to every `<a>` the renderer produces (normal links, `<https://...>` autolinks, plain URLs from the url plugin). Images shouldn't be affected. Default behaviour (no option) should stay exactly as it is today.

Happy to test a PR. Thanks for the great library!
