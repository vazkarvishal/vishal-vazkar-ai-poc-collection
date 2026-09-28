# 🏠 Reading Detached Property Watch

This is a reusable Reading example adapted from a saved ChatGPT automation prompt on 2026-09-28. The recipient address has been replaced with a placeholder. The live automation remains in ChatGPT; edits to this file do not update it. Schedule: daily at 08:00 Europe/London.

FEATURE FLAGS:
- SEND_EMPTY_EMAIL = true
- ATTACH_REJECTED_XLSX = true

AREA PRIORITY ORDER:
Treat the user's listed area order as an explicit presentation/search priority, without changing acceptance criteria or match scores:
1. Caversham
2. Caversham Heights
3. Emmer Green
4. Earley
5. Lower Earley
6. Woodley
7. Shinfield
8. Tilehurst
Search all areas fully. When presenting accepted properties, sort first by AREA PRIORITY, then by MATCH SCORE descending, then by price ascending. Apply the same area-priority ordering to Investment Outliers.

Search for newly listed, newly reduced, back-on-market, new-build, off-plan and auction residential properties in Caversham, Caversham Heights, Emmer Green, Earley, Lower Earley, Woodley, Shinfield and Tilehurst. Check major aggregators including Rightmove, Zoopla and OnTheMarket; specialist new-build sources including NewHomesForSale and direct developer sites where discoverable; and auction/fixer-upper sources including Allsop, SDL/Eddisons/Auction House and other relevant local auction listings.

PRIMARY HOME CRITERIA:
- Detached house only.
- Maximum asking price £800,000. Treat £700,000 or below as preferred and £700,001–£800,000 as stretch.
- Minimum 4 bedrooms.
- Minimum 3 bathrooms/WCs suitable for family use, ideally at least 2 full bathrooms plus a downstairs WC.
- At least two bedrooms must each be at least 4.0m x 3.0m based on the published floorplan. If dimensions are unavailable, mark NEEDS VERIFICATION.
- Minimum internal area 1,500 sq ft / approximately 139 sq m.
- Open-plan kitchen/dining/family room OR a genuinely large kitchen.
- Garage required.
- Private garden required.
- Prefer driveway/off-street parking.

LOCATION / QUALITY CHECKS:
- Check postcode/address against current local crime information, prioritising official police.uk neighbourhood/street-level data where available. Reject or heavily penalise materially elevated nearby violent crime, burglary, vehicle crime or persistent anti-social behaviour.
- Check practical access to a useful London-commuter station. Prefer <=15 minutes typical drive/taxi; 16–20 minutes acceptable; >20 minutes normally reject unless exceptional.
- Check school quality and likely catchment practicality.
- Check official flood-risk information where possible; strongly penalise medium/high material risk.
- Check road/noise/environmental exposure and penalise direct adjacency to major arterial roads, motorways, rail lines, industrial estates or other persistent noise/air-quality sources.
- Prefer strong schools, good takeaway/delivery, taxi/Uber availability, established family neighbourhoods and convenient Reading access.

OUTLIER / INVESTMENT LANE:
Also search for detached houses, unusually large houses, auction properties, probate/modernisation projects or rundown homes in the same target areas that may fail normal condition criteria but could represent an investment opportunity. Prioritise excellent streets/locations, meaningful discount to local renovated values, extension/reconfiguration potential, large plots and strong underlying floor area. Condition can be poor, but location/crime must be strong. Never treat auction guide price as expected purchase price.
- Show a maximum of 5 Investment Outliers per run.
- Rank Investment Outliers first by Area Priority, then strongest location/value/refurbishment potential.
- For every Investment Outlier, include one concise bullet starting with “Why outlier:” explaining why it was surfaced despite failing the primary-home criteria.

CROSS-RUN DEDUPLICATION — REQUIRED:
Maintain a persistent reviewed-property history across runs. Before producing today’s attachment or email output, compare every property reviewed today against properties reviewed in all prior runs, with at minimum the previous day’s reviewed-property file/history.
- Define a stable PROPERTY_KEY using, in priority order: normalized full address/postcode when available; otherwise canonical listing URL/listing ID + agent; otherwise normalized title + area + price + agent.
- A property already present in prior-run history is PREVIOUSLY_REVIEWED and must NOT be included in today’s rejected/unassessed attachment merely because it was encountered again.
- TODAY_NEW_REVIEWED = properties whose PROPERTY_KEY has never appeared in prior-run history.
- The next day’s attached rejected-properties file must contain ONLY TODAY_NEW_REVIEWED properties that are rejected or unassessed on that run.
- Do not repeat yesterday’s rejected/unassessed properties in today’s attachment.
- Accepted properties that are unchanged and were previously notified must also remain suppressed from the email.
- Exception: if a previously reviewed property has a MATERIAL CHANGE, treat it as changed for notification purposes but do not count it as a newly reviewed property. Material changes include price reduction/increase, back on market, status change, added floorplan/measurements, substantial listing-content change, new auction deadline, or other criteria-relevant change.
- For a MATERIAL CHANGE, include it in the email only when relevant, and record it separately in run accounting as PREVIOUSLY_REVIEWED_CHANGED. Do not put it into the “newly reviewed rejected” workbook unless its rejection reason itself materially changed and this should be made explicit.
- When prior-run history is unavailable or cannot be read, do NOT silently assume every property is new. Mark HISTORY_STATUS = unavailable in the technical footer and avoid claiming cross-run deduplication succeeded.

DETERMINISTIC RUN ACCOUNTING:
Maintain an explicit run ledger for every unique property candidate encountered before final acceptance/rejection.
- A property counts as SKIMMED exactly once per run after within-run deduplication.
- TOTAL_SKIMMED = count of all unique deduplicated property candidates evaluated in the current run.
- TODAY_NEW_REVIEWED = count of unique properties never present in prior-run history.
- PREVIOUSLY_REVIEWED_UNCHANGED = count of current-run properties matched to history with no material change.
- PREVIOUSLY_REVIEWED_CHANGED = count of current-run properties matched to history with a material change.
- PRIMARY_ACCEPTED = count of properties accepted into the Primary Home lane in the current run.
- OUTLIERS_ACCEPTED = count of properties surfaced in the Investment Outlier lane, capped at 5.
- TOTAL_ACCEPTED = PRIMARY_ACCEPTED + OUTLIERS_ACCEPTED.
- TODAY_NEW_REJECTED_OR_UNASSESSED = count of TODAY_NEW_REVIEWED properties not included in TOTAL_ACCEPTED.
- These counts must come from the explicit ledger and must never be estimated, rounded, inferred from result-page totals, or invented.

DEDUPLICATION / CHANGE DETECTION:
Deduplicate within the current run across portals using address, postcode, photos, floorplan, agent and listing identity. Then perform the required cross-run deduplication against prior reviewed-property history. Track new listing, price change, back on market, status change, added floorplan/measurements, new-build release or auction deadline. Do not notify repeatedly about unchanged properties.

REJECTED-PROPERTIES EXCEL:
If ATTACH_REJECTED_XLSX = true, create an .xlsx file for every run containing ONLY TODAY_NEW_REVIEWED properties whose final status is REJECTED or UNASSESSED. Never include PREVIOUSLY_REVIEWED_UNCHANGED properties. One row per unique property. Include columns:
- Run date/time
- Property Key
- Area Priority
- Area
- Address/listing title
- Asking/guide price
- Source/portal
- Listing URL
- Listing status/new/reduced/back-on-market/new-build/auction if known
- Bedrooms
- Bathrooms/WCs
- Internal sq ft
- Largest bedroom dimensions
- Second-largest bedroom dimensions
- Kitchen/layout note
- Garage
- Garden
- Parking
- Station used
- Estimated drive/taxi minutes
- Crime assessment
- School/catchment assessment
- Flood risk
- Road/noise/environmental note
- Calculated score if enough data exists
- Final status: REJECTED or UNASSESSED
- Primary rejection reason
- Secondary rejection reasons
Sort rows by Area Priority ascending, then Final Status, then Calculated Score descending where available.
Use deterministic rejection reasons tied directly to criteria, e.g. NOT_DETACHED, PRICE_OVER_800K, FEWER_THAN_4_BEDS, FEWER_THAN_3_BATHS_WCS, UNDER_1500_SQFT, BEDROOM_DIMENSIONS_FAIL, BEDROOM_DIMENSIONS_UNKNOWN, NO_GARAGE, NO_GARDEN, STATION_OVER_20_MIN, CRIME_RISK, FLOOD_RISK, ROAD_NOISE_RISK, SCHOOL_ACCESS_WEAK, LISTING_DATA_INSUFFICIENT.
Name the file: Reading_Property_Watch_Newly_Reviewed_Rejected_YYYY-MM-DD.xlsx.
- CRITICAL: every populated Listing URL cell must be a real clickable Excel hyperlink, not plain text. Verify the exported .xlsx contains clickable links before attaching it.

HISTORY UPDATE:
At the end of each successful run, append TODAY_NEW_REVIEWED properties to the persistent reviewed-property history with PROPERTY_KEY, first-seen date, last-seen date, last-known price/status and final classification. Update last-seen/last-known fields for PREVIOUSLY_REVIEWED_CHANGED properties. Never create duplicate history rows for the same PROPERTY_KEY.

OUTPUT / EMAIL DECISION:
- If there are new or materially changed accepted properties, send the normal concise email.
- If there are no new/materially changed accepted properties and SEND_EMPTY_EMAIL = true, still send an email titled “🏠 Reading Property Watch — No New Matches” containing a short no-match message plus the technical run footer and today’s newly-reviewed rejected/unassessed workbook.
- If TODAY_NEW_REJECTED_OR_UNASSESSED = 0, still attach an empty workbook with headers only when ATTACH_REJECTED_XLSX = true, so it is explicit that there were no newly reviewed rejected properties.
- If there are no new findings and SEND_EMPTY_EMAIL = false, do not send an email.

RESPONSE FORMAT — KEEP PROPERTY CONTENT VERY SHORT:
For each accepted property, output only:
- Property name/area + price + MATCH SCORE /100
- One clickable listing link
- Maximum 5 concise bullet highlights.
- For Investment Outliers, one bullet must be “Why outlier:”.
Order accepted properties by Area Priority first, then MATCH SCORE descending, then price ascending.

TECHNICAL RUN FOOTER — REQUIRED AT END OF EVERY EMAIL:
Add a compact section titled “Technical run info” with exactly these values derived from the ledger:
- Unique properties skimmed this run: TOTAL_SKIMMED
- Newly reviewed today: TODAY_NEW_REVIEWED
- Previously reviewed unchanged: PREVIOUSLY_REVIEWED_UNCHANGED
- Previously reviewed with material change: PREVIOUSLY_REVIEWED_CHANGED
- Primary matches accepted: PRIMARY_ACCEPTED
- Investment outliers accepted: OUTLIERS_ACCEPTED
- Total accepted: TOTAL_ACCEPTED
- Newly reviewed rejected / unassessed: TODAY_NEW_REJECTED_OR_UNASSESSED
- Newly-reviewed rejection workbook: attached / not attached
- Cross-run history status: available / unavailable
- SEND_EMPTY_EMAIL: true/false
Do not use approximate language such as “about”, “roughly”, or “around”.

SCORING:
- Immediate location, crime profile and neighbourhood quality: 15
- Station practicality / London commuting: 10
- School quality and realistic catchment access: 10
- Flood risk: 10
- Road/noise/environmental exposure: 5
- House size/layout and bedroom dimensions: 15
- Price/value: 15
- Kitchen/storage/utility practicality: 8
- Garage/garden/parking: 7
- Condition/newness: 3
- Local amenities/takeaway/cabs: 2
Total: 100

Classify results as A = 85–100, B = 75–84, C = 65–74 only if compelling, and Investment Outlier separately.

EMAIL DELIVERY:
Use the connected Gmail account and send to YOUR_EMAIL_ADDRESS.
- With accepted new/materially changed properties, subject: “🏠 Reading Property Watch — New Matches”.
- With no accepted new/materially changed properties and SEND_EMPTY_EMAIL = true, subject: “🏠 Reading Property Watch — No New Matches”.
- Attach Reading_Property_Watch_Newly_Reviewed_Rejected_YYYY-MM-DD.xlsx when ATTACH_REJECTED_XLSX = true.
- Keep property content concise, ordered by Area Priority, then append the mandatory Technical run info footer.
