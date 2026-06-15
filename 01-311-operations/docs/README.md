# Calgary 311 Service Operations Dashboard

An operational Power BI dashboard on the City of Calgary's 311 service requests,
covering request volume, resolution performance, geographic distribution, and a
threshold-based alert.

**Built in Power BI Desktop; designed for publish-to-web and daily scheduled refresh**

## Problem
311 generates a high volume of service requests across dozens of categories and
all city communities. This dashboard turns the raw feed into an operational view:
what's coming in, how fast it's resolved, where it concentrates, and when volume
spikes warrant attention.

## Data
- Source: City of Calgary Open Data — 311 Service Requests (`iahh-g8bj`), via the
  Socrata SODA API.
- Scope: Jan 1, 2025 – present (~696,982 rows).
- License: Open Government Licence – City of Calgary.

## Tools
Power BI Desktop (model + report), Power BI Service (publish + refresh),
Power Automate (threshold alert), Socrata SODA API (ingestion).

## Architecture
API (scoped SoQL, server-side date filter, paged)
  -> Power Query (clean, type, derive Category + ResolutionDays)
  -> Star schema (FactServiceRequest + DimDate/Service/Community/Agency)
  -> DAX measures
  -> 4-page report -> published -> Power Automate alert

## What it does
- KPIs: total requests, % closed, avg/median days to close, open backlog.
- Trends: monthly volume with a rolling 3-month line; month-over-month %.
- Operations: resolution time and % closed by category and by responsible agency.
- Geography: request map by location + top communities.
- Category deep-dive: decomposition tree + drillthrough to category detail.
- Alert: Power BI data alert -> Power Automate flow on volume spikes.

## Reproduce
1. Get a free Socrata app token (data.calgary.ca -> Developer Settings).
2. Open the .pbix, edit the `Token` parameter in Power Query, refresh.
3. Publish to your own workspace; set the web source credentials to Anonymous.

## Refresh & access
Designed for daily scheduled refresh in the Power BI Service; published via
Publish-to-web using open-licensed data only.

## Limitations
- `address` is frequently blank (privacy); geography relies on point coordinates.
- Resolution time excludes still-open requests and any records with inconsistent
  close dates.

## Screenshots
See `docs/screenshots/`.