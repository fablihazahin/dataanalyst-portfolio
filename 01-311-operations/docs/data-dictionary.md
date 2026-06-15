# Data Dictionary — Calgary 311 Service Operations Dashboard

**Source:** City of Calgary Open Data — 311 Service Requests (`iahh-g8bj`), via the Socrata SODA API.
**Scope:** Requests from 2025-01-01 to present.
**Fact table:** `FactServiceRequest` (grain: one service request).

## Fields

| Field | Origin | Type | Description | Transformation / Notes |
|---|---|---|---|---|
| `service_request_id` | Source | Text | Unique ID for each 311 request | None |
| `requested_date` | Source | Date/Time | Timestamp the request was logged | Typed to Date/Time; rows with null removed; basis for `RequestedDate` |
| `updated_date` | Source | Date/Time | Timestamp of the most recent update | Typed to Date/Time; reference only |
| `closed_date` | Source | Date/Time | Timestamp the request was closed (blank if still open) | Typed to Date/Time; drives `ResolutionDays` |
| `status_description` | Source | Text | Request status (e.g., Closed, Open) | Trimmed; used by Closed/Open measures (filter = "Closed") |
| `source` | Source | Text | Channel the request came through (Phone, App, Web, Other) | Trimmed; used in the channel donut |
| `service_name` | Source | Text | Full service type, formatted "Category - Detail" | Trimmed; basis for `Category`; key to `DimService` |
| `agency_responsible` | Source | Text | City department responsible for the request | Trimmed; key to `DimAgency` |
| `address` | Source | Text | Street address (frequently blank for privacy) | Kept; largely unused |
| `comm_code` | Source | Text | Community code | Key to `DimCommunity` |
| `comm_name` | Source | Text | Community name | Trimmed; community display label |
| `location_type` | Source | Text | Geocoding precision/type (e.g., Community Centrepoint) | Kept; reference only |
| `longitude` | Source | Decimal | Longitude coordinate | Typed to Decimal; Data category = Longitude; used by map |
| `latitude` | Source | Decimal | Latitude coordinate | Typed to Decimal; Data category = Latitude; used by map |
| `point` | Source | Geo | Combined point geometry | Kept; unused in visuals |
| `Category` | Derived | Text | High-level service group | Text before " - " in `service_name` (falls back to full name if no delimiter) |
| `RequestedDate` | Derived | Date | Date-only version of `requested_date` | `Date.From([requested_date])`; join key to `DimDate[Date]` |
| `ResolutionDays` | Derived | Decimal | Days from request to close (blank if open or inconsistent) | `if closed_date null or closed < requested then null else Duration.TotalDays(closed − requested)`; feeds Avg/Median Days to Close |

## Measures (`_Measures` table)

| Measure | Description |
|---|---|
| `Total Requests` | Count of all service requests |
| `Closed Requests` | Requests where `status_description = "Closed"` |
| `Open Requests` | Total minus Closed |
| `% Closed` | Closed ÷ Total |
| `Avg Days to Close` | Average `ResolutionDays` over closed requests |
| `Median Days to Close` | Median `ResolutionDays` over closed requests |
| `Requests Prior Month` | Total Requests shifted back one month |
| `Requests MoM %` | Month-over-month change in Total Requests |
| `Requests Rolling 3M` | Total Requests over a trailing 3-month window |
| `% Closed Within 7 Days` | Share of closed requests resolved in ≤ 7 days |

## Dimensions

| Table | Key | Built from |
|---|---|---|
| `DimDate` | `Date` | DAX `CALENDAR` (2025-01-01 → today); marked as date table |
| `DimService` | `service_name` | Distinct `service_name` + `Category` |
| `DimCommunity` | `comm_code` | Distinct `comm_code` + `comm_name` (deduped on `comm_code`) |
| `DimAgency` | `agency_responsible` | Distinct `agency_responsible` |