# Worked Example — Bexar County, TX severe storms (August 2026)

## The storm (verified via web search)
- **Event:** Severe storms across South-Central Texas — tornadic activity,
  thunderstorms, hail, straight-line winds.
- **Verification:** Governor requested a U.S. SBA disaster declaration for
  Bexar County and contiguous counties (Sep 9, 2026); damage thresholds
  confirmed by local/state/federal assessment.

## What was run
```bash
python3 bin/storm_trends.py --storm-type hail --location "San Antonio TX" \
    --geo US-TX --out bexar_trends.json
```

## What actually happened (honest result)
Google blocked every section from the run environment (HTTP 411s, timeouts)
— 0/4 sections succeeded. The script reported this plainly:
```json
{"summary": "0/4 sections succeeded. Blocked by Google — run the seed terms by hand on trends.google.com instead."}
```
This is designed behavior, not failure: the next step is running the same
seed terms on trends.google.com directly.

## What a successful brief looks like (ILLUSTRATIVE — sample format, not measured data)

> **Storm:** hail/wind, San Antonio TX (Bexar County)
> **Rising queries (US-TX, past 7 days):**
> | Query | Growth | Surfaced by |
> |---|---|---|
> | hail damage roof repair san antonio | Breakout | hail damage roof repair |
> | roof damage hail storm claim | +1,200% | roof damage hail storm |
> | sba disaster loan bexar county | Breakout | hail damage claim |
> | wind damage roof repair san antonio | +450% | hail damage roof |
> | hail damage roof inspection free | +300% | roofing company hail damage |
>
> **Hottest subregions:** San Antonio DMA, Austin DMA, Houston DMA
>
> **Article angles (each tied to a spike):**
> 1. "Bexar County Hail: What Your Roof Looks Like After the August Storms" —
>    photo-led damage-identification guide (matches the breakout inspection queries).
> 2. "SBA Disaster Loans After the Texas Storms: What to Tell Homeowners" —
>    the SBA declaration is driving its own search spike; be the site that explains it.
> 3. "Hail Claim Denied? The Documentation Adjusters Actually Want" —
>    claim-query spike means denials are coming next; get ahead of it.
> 4. "Wind vs. Hail Damage: Why Your Roof Has Both" — matches the dual
>    wind/hail query pattern in the data.
> 5. "Storm Chasers Are Coming — How to Vet a Roofer This Week" —
>    consumer-protection angle timed to the contractor-search surge.

## A real measured result

Sep 13, 2026: a flash-flood warning for Yavapai County, AZ produced a
successful pull. Rising queries included `flood damage restoration` and
`flood restoration companies` as **Breakout**, and `water damage restoration
mesa` at **+450%** — all measured, same morning, all mapped to article angles.

## Takeaway

The value isn't the script alone — it's the loop: verify storm → pull trends
(script or by hand) → rank spikes → publish before competitors.
