# Calgary Health Facilities — Reverse-Engineering & Documentation

A small portfolio project that takes an undocumented public dataset and works it end to end: extract from a REST API, decipher the structure, model it into an ERD, and translate it into a data dictionary, data-flow documentation, and a requirements register.

**Data source:** City of Calgary Open Data — *Calgary Health Clinics and Hospitals* (dataset `tsqf-wjr5`), Socrata SODA REST API. Public, Open Government Licence.

## How to run
```bash
pip install requests pandas
python etl.py
```
This extracts the data from the API, prints a column profile, and loads the tables into `calgary_health.db` (SQLite).

## Deliverables
- `etl.py` — extract, profile, load (and a normalization template)
- `erd.png` / dbdiagram link — the inferred data model
- `data_dictionary.md` — field-level definitions, types, valid values, sources
- `requirements_register.md` — requirements with IDs and traceability
- `data_flow.md` — who inputs the data, who consumes it, and the flow end to end
- this `README.md`

## How I deciphered the structure
The dataset arrived as a single flat CSV with no documentation. I profiled every column — its data type, how many distinct values it held, and sample values — to work out what each meant. **"name"** and **"address"** were nearly unique per row, so they describe individual facilities. **"type"** had only 9 repeating values and **"comm_code"** held repeating 3-letter community codes, so I treated both as categories. **"point"** stored a WKT coordinate. From that I designed a normalized model: a **"facility"** table holding the per-facility fields, with foreign keys to a **"type_lookup"** and a **"community_lookup"**, so each category is defined once and referenced by ID.

## Data flow & roles
The City of Calgary maintains this facilities list and publishes it as open data, them being the data inputters. The consumers are the public and any application or report built on the data. My ETL sits in the middle: it extracts the export, cleans and standardizes it, defines each field, and models it into linked tables. My role is to define the data, document its structure, flag quality gaps, and map how it flows from source to consumer. If the platform were maintained by an external vendor, I would give the vendor these definitions and validate their data against them.

## How to run
```bash
pip install pandas
python etl.py
```
The script reads the CSV, prints a column profile, loads the raw flat table into `calgary_health.db` (SQLite), and normalizes the data into three tables: `facility`, `type_lookup`, and `community_lookup`.

## Deliverables
- `etl.py` — extract, profile, load, and normalize
- `erd.png` — the relational model
- `data_dictionary.md` — field-level definitions, types, valid values, sources
- `requirements_register.md` — requirements with IDs and traceability
- `example_queries.sql` — sample queries against the model
- `README.md` — this file

## How I deciphered the structure
The dataset arrived as a single flat CSV with no documentation. I profiled every column — its data type, how many distinct values it held, and sample values — to work out what each one meant. `name` and `address` were nearly unique per row, so they describe individual facilities. `type` had only 9 repeating values and `comm_code` held repeating 3-letter community codes, so I treated both as categories. `point` stored a geographic coordinate in WKT format. From that I designed a normalized model: a `facility` table holding the per-facility fields, with foreign keys to a `type_lookup` and a `community_lookup`, so each category is defined once and referenced by ID.

## Data flow & roles
The City of Calgary maintains this facilities list and publishes it as open data — they are the data inputters. The consumers are the public and any application or report built on the data. My ETL sits in the middle: it extracts the export, cleans and standardizes it, defines each field, and models it into linked tables. My role is to define the data, document its structure, flag quality gaps, and map how it flows from source to consumer. If the platform were maintained by an external vendor, I would provide the vendor these definitions and validate their data against them.

## Open questions & inconsistencies found
- 7 facilities are missing an address and 10 are missing a community code — I'd confirm with the data owner whether these are genuinely unknown or data-entry gaps.
- `comm_code` is a code, not a readable name; I'd confirm the code-to-name mapping with the City.
- `point` stores coordinates as longitude then latitude (WKT order) — worth flagging so consumers don't reverse them.
- I'd confirm the exact definitions of the 9 facility types with whoever maintains the list.

## What I'd do next
I'd validate the open questions above with the data owner, join a community-name reference so codes are human-readable, and treat the data dictionary as a living document so definitions stay consistent as the data changes.

## Tech stack
Python (pandas), SQLite, dbdiagram.io.

---
*Built from public City of Calgary open data as a personal portfolio project.*
