# Observed daily-flow studies

The current development workbench adds a real, pinned USGS daily-flow record. It uses Python 3.12's standard library. The public v0.5 package predates this increment; use the matching development package or checkout containing `observations`.

## Run the bundled real case offline

```sh
python3 earth.py observations run --out runs/potomac
python3 earth.py observations inspect runs/potomac
```

Open `runs/potomac/report.html`. The complete 2021–2024 USGS response and source record are bundled under `scenarios/observations/potomac-2021-2024`. No account, network access or new library is needed for this workflow. The report includes quality counts, original daily values, monthly/yearly/preselected-period comparisons and downloadable CSV/JSON.

The source contains 1,461 requested daily records, including 30 approved estimates. Primary comparisons exclude the estimates and retain them in a separately displayed sensitivity. Revised, provisional, missing, absent and negative observations have explicit rules in [USGS-DAILY-001](benchmarks/observations/USGS-DAILY-001.md). This is descriptive observed discharge, not a calibrated pollutant model or an intervention effect.

## Change a comparison and preserve its parent

```sh
python3 earth.py observations run --split-date 2022-01-01 --out runs/potomac-other-periods
```

This changes the first day of the second period; the two contiguous periods still cover the requested dates. The question and period labels update, and the original study identity is retained as parent provenance. Changing a comparison after examining results is exploratory analysis, not a new blinded confirmation.

For explicit questions or date subsets, copy the snapshot's `study.json`, change its fields and use `--study YOUR_STUDY.json`. The two periods must partition its declared dates and lie within the source snapshot. Original data remains unchanged.

## Export, reopen and reproduce

```sh
python3 earth.py observations export runs/potomac --out runs/potomac-exported
python3 earth.py observations inspect runs/potomac-exported
python3 earth.py observations reproduce runs/potomac --out runs/potomac-reproduced
```

Inspection verifies the retained raw data, source identities, quality decisions, arithmetic, report and CSV. A separate decimal-arithmetic reference checks all summaries directly against raw records. Hashes establish consistency, not provider authenticity against a person who rewrites every file. Reproduction requires the exact matching runtime source digest. Keep published source packages to reproduce their older bundles.

Each output must be new and outside its source directory. An interrupted attempt keeps its raw inputs and partial evidence. It cannot pass inspection without the final completion record. Preserve it, then retry in a new directory. Export and reproduction refuse nested outputs that would change the original bundle.

## Fetch a different bounded public record

Fetching is the only observation command that uses the network. It makes two unauthenticated HTTPS requests to the official USGS API and retains a failed request attempt if retrieval or admission fails.

```sh
python3 earth.py observations fetch --site 01646500 --start 2024-01-01 --end 2024-01-31 --split-date 2024-01-16 --out runs/new-source
python3 earth.py observations run --snapshot runs/new-source --out runs/new-study
```

This adapter supports at most 3,660 days and 16 MB per raw response, one complete response page, one station/time series and USGS parameter 00060/statistic 00003 in ft³/s. An unsupported qualifier, changed schema, pagination, duplicated day or mixed identity fails explicitly. Narrow the request or review the adapter; do not silently discard records to get a pass. Retain USGS attribution and its provisional-data conditions. No credentials or rate-limit bypass are supported.

## Inspect the calculations

[The executed notebook](../notebooks/observed-potomac.ipynb) contains the raw-data profile, exact conversion, separate period arithmetic and quality sensitivity. Its code uses only the standard library and original project modules. Jupyter is optional; the complete study works through the CLI without it. Notebook code cells can also be checked with `python3 tools/verify_observed_notebook.py`.

The product's native offline report exposes all methods and source records. CSV text cells beginning with a spreadsheet formula prefix are escaped with a leading apostrophe; original source strings remain unchanged in JSON.
