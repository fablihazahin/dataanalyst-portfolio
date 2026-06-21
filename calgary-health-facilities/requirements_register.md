# Requirements Register — Calgary Public Service Facilities
**Prepared by:** Fabliha Zahin · **Date:** 20.06.26

> Framed as: "If I were asked to turn this raw, undocumented dataset into a clean, searchable directory, what would the requirements be?" Each has an ID so it can be traced through to a solution.

| ID | Requirement | Type | Source | Priority | Status |
|---|---|---|---|---|---|
| REQ-01 | Every facility must have a name, type, and location | Functional | Data review | High | Open |
| REQ-02 | Facility type must come from the defined set of 9 values | Functional | Data review | High | Open |
| REQ-03 | Users can filter facilities by type and by community | Functional | Assumed user need | Medium | Open |
| REQ-04 | Address should be present for every facility (7 currently missing) | Non-functional | Data quality | Medium | Open |
| REQ-05 | Community code should be present and valid (10 currently missing) | Non-functional | Data quality | Medium | Open |
| REQ-06 | Coordinates must be valid and within Calgary's bounds | Non-functional | Data quality | Low | Open |
| REQ-07 | All fields must be documented in a data dictionary | Non-functional | Governance | High | Open |

## Field guide
- **Type:** Functional (what the system must do) or Non-functional (quality, performance, governance).
- **Source:** where the requirement came from — data review, an assumed user need, or a governance standard.
- **Priority:** High / Medium / Low. **Status:** Open / In progress / Met.