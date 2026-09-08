# USGS-DAILY-001: observed daily-discharge contract

Initial case/window chosen in V1-CONTRACT.md before retrieval: USGS-01646500, January 1, 2021 through December 31, 2024; compare calendar 2021–2022 with 2023–2024. This is a demonstration convenience sample, not a representative basin sample or a climate trend experiment. Current scope is descriptive observed data; synthetic model scopes A0–A4 are not assigned to measurements.

## Source admission

- Provider: U.S. Geological Survey. [Official API](https://api.waterdata.usgs.gov/ogcapi/v0/?f=html) states that data provided by the service is US Government work in the public domain. Accessed September 8, 2026. Attribution follows [USGS citation guidance](https://waterdata.usgs.gov/citation/), database DOI 10.5066/F7P55KJN. This applies to the admitted USGS API data, not every linked webpage or image.
- Endpoint: current OGC daily collection; parameter `00060`, statistic `00003`. Frozen source snapshot stores exact response bytes, URL, request date, hash, station metadata and metadata hash. Each observation keeps time-series identity, source units, original string value, approval/qualifier and revision metadata.
- API documentation/schema and returned data differ on qualifier shape: the actual September 8 response uses null or string lists (`ESTIMATED`, `REVISED`). The adapter supports only null or a bounded list of known codes and rejects other types/codes. This is explicit adapter scope, not a claim about every possible USGS qualifier.
- API approval means USGS publication approval, not scientific approval of this analysis. [Provisional conditions](https://waterdata.usgs.gov/provisional-data-statement/) remain visible. Data revisions create a distinct snapshot.
- Runtime uses Python's standard library, reviewed built-in code and passive public-data requests. No third-party software, credential, installation, telemetry or paid service is adopted. Fetching is optional and bounded; normal study execution uses the pinned local bytes offline. Official rate limits remain respected; no concurrent harvesting.

## Quality policy and support

Schema/profile inspection preceded statistical calculation. Primary summaries include finite nonnegative daily means with USGS `Approved` status and no qualifier except `REVISED`. A separately named sensitivity includes approved `ESTIMATED` values. Provisional values remain visible and are excluded from both. Null and absent dates are distinct. Negative values are retained as excluded, because signed/reverse flows may exist but lie outside this simple nonnegative-flow analysis. Zero is valid and never used as a missing sentinel. The initial profile observed 30 estimated and 116 revised values, including four bearing both labels; these are overlapping counts, not disjoint populations.

Input is one daily mean per date at one point station and one time series. Dates are civil observation labels, not inferred UTC instants. Site timezone metadata is retained; no daylight-saving interpolation, instantaneous peak or exact volumetric integral is inferred. The exact international-foot conversion uses `1 ft = 0.3048 m`, so `ft^3/s * 0.028316846592 = m^3/s`, with original strings retained. [NIST units table](https://www.nist.gov/document/2026-hb-133-appendix-e) supports this conversion. Extra displayed digits do not add measurement precision.

## Descriptive outputs

- Complete day table with one row per requested calendar day, source record or explicit absence, inclusion flags, source value and SI value.
- Dataset, calendar-year, calendar-month and predeclared-period summaries: requested days, received rows, valid primary and sensitivity counts, coverage, arithmetic mean, minimum/maximum daily mean and linearly interpolated empirical p10/p50/p90 (index `(n-1)*p`). These are ordinary quantiles, not exceedance quantiles.
- Monthly and period comparisons show excluded-day count and coverage beside values. The period mean difference is a descriptive difference between two preselected finite records. No hypothesis test, climate attribution, uncertainty interval, future forecast or intervention effectiveness is inferred.
- Zero accepted days yields null statistics and `NO_ACCEPTED_OBSERVATIONS`; partial support yields `PARTIAL_COVERAGE`. No gap filling, time rescaling or synthetic value substitution.
- No discharge sum is called total water volume, and no particle/pollutant concentration or load is inferred from discharge.

## Integrity and independent checks

Maximum 10 calendar years / 3660 days, 16 MB per admitted raw response, at most one complete daily response with no next-page link, unique feature IDs and unique dates. Multiple time-series identities or mismatched location/parameter/statistic/unit are errors. Reject nonfinite numeric encodings, booleans, malformed dates, ambiguous date-times, unknown quality semantics, conflicting or identical duplicate grain, future/out-of-window dates and unexpected item counts. Reject an empty source; an explicit sparse source is permitted with visible absent days.

Each completed bundle retains raw source, site metadata, source record, study specification, normalized day table, summary JSON/CSV, offline report, attempts and completion manifest. Inspection checks hashes and independently re-parses raw input, recomputes normalized rows and statistics, and compares presentation outputs. Hashes establish consistency, not provider authenticity against an author controlling every file. Reproduction requires the matching source runtime and creates a fresh directory. Interrupted runs retain partial evidence; retries use a fresh directory without overwriting it.

Falsifiers: hand-calculated 1/2/3/4 sequence and constant/zero controls; leap-day and sparse record; provisional/estimated/revised overlap; local-date identity; duplicate grain and series/site/unit/statistic swaps; malformed and huge input; changed raw data/hash; forged summary and table after manifest regeneration; HTML escaping; interrupted activation and output collision. These must pass before promoting the increment.
