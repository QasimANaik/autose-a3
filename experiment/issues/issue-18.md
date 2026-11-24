<!-- title: Some links in our chat logs are not clickable -->
We render our team chat logs to HTML with mistune (`plugins=["url"]`) and people keep complaining that "some links are dead text".

For example this log line:

```
alice: docs are at www.example.com/docs, or the old page https://example.com/old
```

The second link is clickable, the first one isn't, even though it is clearly an address. Our users paste addresses all kinds of ways and expect them to work like on GitHub or in Slack.

Could the url plugin be smarter about this? Not sure what the right rules are, but we'd like the obvious ones to just work without breaking the links that already work.
