# Requesting Data

## Current: CCRS (2025+)

CHP shut down iSWITRS on January 8, 2025. Crash data is now published through
the [California Crash Reporting System (CCRS)](https://data.ca.gov/dataset/ccrs)
on the California Open Data portal.

CCRS provides yearly CSV files (`crashes_YYYY.csv`, `parties_YYYY.csv`,
`injuredwitnesspassengers_YYYY.csv`). **This tool does not yet support the CCRS
format** — support is planned for a future release.

For questions, contact CHP at iswitrs@chp.ca.gov.

## Legacy: iSWITRS (pre-2025)

If you already have SWITRS data in the legacy format (`CollisionRecords.txt`,
`PartyRecords.txt`, `VictimRecords.txt`), this tool converts it as-is.

The iSWITRS portal is no longer available. The legacy instructions that were
previously here (register an account, request "Raw Data", wait for an email)
no longer apply.
