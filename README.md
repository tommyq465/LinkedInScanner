# LinkedInScanner

Turns a four-part search brief into the boolean strings and search URLs that
actually find people on LinkedIn.

## Why a query builder

LinkedIn has no people-search API and blocks automated access, so nothing can
scrape it for you. What moves the needle instead is synonym coverage: someone
doing restructuring work often never writes "restructuring" in their headline,
but does write "turnaround", "distressed", or "Chapter 11". This expands your
brief across those variants, then hands you links to open.

## Usage

```
python3 scan.py --industry restructuring \
                --role "managing director" \
                --company Deloitte \
                --school "Notre Dame" \
                --city Chicago
```

Only `--industry` is required. Drop `--company` to search any employer, drop
`--city` to search every geography.

| Flag | Meaning |
| --- | --- |
| `--industry` | field of work (required) |
| `--role` | seniority or title |
| `--company` | specific firm, or omit for any |
| `--school` | required alma mater |
| `--city` | metro area, or omit for anywhere |
| `--json` | machine-readable output |

## What comes back

Four search paths, ordered by hit rate:

1. **Company People tab** — employees LinkedIn has already confirmed work
   there, filterable by school and city natively. Highest yield when you named
   a firm.
2. **School Alumni tab** — filters by employer, city, and field of study at
   once, and shows shared-connection paths.
3. **LinkedIn people search** — the full boolean in the search bar. Apply
   location and current-company as native facets once results load.
4. **Google X-ray** — `site:linkedin.com/in` against public profiles. Sees
   people outside your network and past the commercial-use limit, at the cost
   of staleness.

## Extending the vocabulary

`linkedin_scanner/taxonomy.py` holds the industry, seniority, school, firm, and
metro mappings. Unmapped inputs pass through as literal search terms and the
output says so, so adding an entry is an optimization, never a prerequisite.

## Limits worth knowing

- Company and school URLs are built from slugs that LinkedIn occasionally
  renames; a stale slug 404s quietly. Verify before trusting an empty result.
- X-ray keeps the top 3 terms per group because Google truncates long queries
  silently. To widen, run a dropped term as its own search.
- Free LinkedIn accounts hit a monthly commercial-use search limit. X-ray does
  not count against it.
