# 🏠 UK Property Watch

An export of the [example ChatGPT scheduled watch for Reading](chatgpt-automation.md) and a standalone Python evaluator. It ranks normalized listings, keeps persistent review history, suppresses unchanged properties, creates a clickable Excel rejection workbook, and can send a concise email through SMTP.

**Important distinction:** the ChatGPT automation is a hosted prompt. This repository snapshot does not deploy, synchronize, or trigger that hosted task. The Python program does not scrape Rightmove, Zoopla, OnTheMarket, auction sites, police.uk, flood maps, schools, or journey planners. Supply lawful listing data and verified assessments in the input JSON. Do not treat the example properties as real listings.

## Quick start

Requires Python 3.10+.

```bash
cd uk-property-watch-2026-09-28
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python watch.py --config examples/reading-config.json --input examples/candidates.json --history state/history.json --output output
python -m unittest discover -s tests -v
```

The command creates `output/report.txt`, `output/ledger.json`, `output/Property_Watch_Newly_Reviewed_Rejected_YYYY-MM-DD.xlsx`, and `state/history.json`. Run it again with the same history to suppress unchanged properties. Keep `state/history.json` on persistent storage and back it up; an ephemeral CI runner without restored history cannot deliver reliable cross-run deduplication. The program marks history unavailable on its initial run.

## Feed real properties

Create your own configuration using [`examples/reading-config.json`](examples/reading-config.json) for area order and thresholds. Produce a JSON array like [`examples/candidates.json`](examples/candidates.json). Each object represents one listing from a permitted feed, export, or human review. For reliable matching, supply a full `address` and `postcode`, otherwise a stable `url` and `agent`. The Reading example searches Caversham, Caversham Heights, Emmer Green, Earley, Lower Earley, Woodley, Shinfield, and Tilehurst. Replace these with any UK areas in your configuration. Collect from authorized property sources and validate their terms before automating access.

For a primary match supply `detached`, numeric `price`, `bedrooms`, `bathrooms` (including family-use WCs), `sqft`, `bedroom_dimensions` as metre pairs, `large_kitchen`, `garage`, `garden`, `station_minutes`, `crime_risk`, `flood_risk`, `road_noise_risk`, and `school_access_weak`. Set the four risk flags from current verified checks, not guesses. Add evidence in `crime_note`, `school_note`, `flood_note`, `environment_note`, plus `station`. Set all eleven `scores` using the component maxima in `watch.py`; incomplete scores produce an unassessed property. `highlights` accepts up to five short strings. For a renovation candidate supply `outlier_reason`; a qualifying detached property with no material crime, flood, or road risk can enter the capped outlier lane.

The evaluator applies the hard filters, ranks by area then score then price, and limits outliers to five. It tracks price, status, floorplan/listing versions, auction deadline, and core measurements for material change detection. The workbook contains only newly reviewed rejected or unassessed properties, with actual Excel hyperlinks. A repeated property with changed details is counted as previously reviewed changed, not newly reviewed. The technical footer is derived from the current-run ledger.

## Email and scheduling

Email is optional. Set `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_TO`, optionally `EMAIL_FROM` and `SMTP_PORT` (default 465), then run:

```bash
python watch.py --config my-config.json --input candidates.json --history state/history.json --output output --send-email
```

By default it sends a no-match email with an empty or populated workbook. Use `--no-send-empty-email` or `--no-attach-rejected-xlsx` to disable those features. Store credentials outside the repository. Schedule the command at 08:00 `Europe/London` on a machine with durable state and an upstream listing collection process. For example, set the host timezone and use cron `0 8 * * *`; cron DST behavior depends on the host. Do not run concurrent jobs against the same history file.

## Re-create the ChatGPT task

In ChatGPT Tasks/Automations, create a daily task at 08:00 Europe/London and adapt the [Reading example prompt](chatgpt-automation.md) to your chosen areas, thresholds, and delivery address. Connect Gmail if using its email delivery instruction. A prompt alone does not guarantee persistent files, access to listing sites, Excel creation, or sending attachments. Validate each integration and the run ledger before relying on that task. Changes here do not alter the existing saved task.

## Known limits

- Data collection, crime, school, flood, noise, and station verification require upstream integrations or manual review. Scores are supplied by that review, then range checked; they are not computed from independent external evidence here.
- Cross-portal matches without a common address/postcode may survive deduplication. Listing URL identity is the fallback.
- History is updated after successful report creation and requested SMTP delivery. Retrying after an email was delivered but before history was written could send a duplicate.
- The outlier lane is a screening tool. Auction guide price is not an expected purchase price.
