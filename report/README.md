# Report source

`report.html` is the source of `../report.pdf` (A4). Rebuild after editing:

```bash
google-chrome --headless=new --disable-gpu --no-sandbox --no-pdf-header-footer \
  --print-to-pdf=report.pdf "file://$PWD/report/report.html"
```

Rows marked PENDING are filled from `results/results.csv` once the remaining runs exist.
Boxes marked "✎ draft reasoning" must be rewritten in the author's own words (course AI policy).
