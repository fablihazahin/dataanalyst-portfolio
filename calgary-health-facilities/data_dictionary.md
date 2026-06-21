# Data Dictionary — Calgary Public Service Facilities
**Source:** City of Calgary Open Data (exported CSV) · **Prepared by:** Fabliha Zahin · **Date:** 20.06.26

| Field | Definition (business meaning) | Data type | Allowed / valid values | Source | Transformation applied | Data-quality notes |
|---|---|---|---|---|---|---|
| `type` | The category of public facility | text | 9 categories incl. Community Centre, Attraction, Court, Library, Visitor Info, PHS Clinic (full list below) | Source dataset | Moved into `type_lookup`; `facility` references it by `type_id` | No missing values |
| `name` | Name of the facility | text | Free text; nearly all unique | Source dataset | None | No missing values |
| `address` | Street address of the facility | text | Free text (Calgary street addresses) | Source dataset | None | 7 of 211 rows missing an address |
| `comm_code` | Calgary 3-letter community code (e.g., CAP, COP, MID) | text | 133 distinct community codes | Source dataset | Moved into `community_lookup`; referenced by `comm_code_id` | 10 of 211 rows missing a code |
| `point` | Geographic location of the facility | text (WKT geometry) | `POINT (longitude latitude)` | Source dataset | None | No missing values; order is **longitude then latitude** |
| `facility_id` | Unique identifier for each facility (primary key) | integer | 1–211 | Derived in ETL | Generated sequentially | Unique |
| `type_id` | Foreign key linking a facility to its type | integer | Matches `type_lookup.type_id` | Derived in ETL | Created by joining to `type_lookup` | None |
| `comm_code_id` | Foreign key linking a facility to its community | integer | Matches `community_lookup.comm_code_id` | Derived in ETL | Created by joining to `community_lookup` | Null where `comm_code` was missing (10 rows) |

## Notes
- Full list of the 9 `type` values: ['Attraction', 'Commercial', 'Community Centre', 'Court', 'Hospital', 'Library', 'PHS Clinic', 'Social Dev Ctr', 'Visitor Info']
- `comm_code` is a code, not a readable name. Joining a Calgary community-name reference later would make it human-readable — optional.