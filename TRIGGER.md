# The Trigger — workflow and rules

## Workflow

1. **Confirm the storm happened.** Verify via web search: news coverage,
   National Weather Service alerts, governor or SBA disaster declarations.
   Never run this on a rumor or a forecast.

2. **Pick storm type + location.**
   - Type: `hail | tornado | hurricane | wind | flood`
   - Location: city/state, e.g. `"San Antonio TX"`
   - Geo code: `US-TX` (state) or `US` (national)

3. **Run the script** (preferred path):
   ```bash
   pip install pytrends   # one-time
   python3 bin/storm_trends.py --storm-type hail --location "San Antonio TX" \
       --geo US-TX --out trends.json
   ```
   Seed terms per storm type live in `SEEDS` at the top of the script —
   extend them, don't hardcode new ones at the call site. Output is JSON
   with `sections` (each `ok`/`blocked`) and a `summary`.

4. **If ≥2 sections succeed:** rank the rising/breakout queries by growth,
   note which metros are searching hardest, write the brief.

5. **If blocked:** drive trends.google.com by hand (or with a browser
   automation) using the same seed terms and geo — the script's output
   tells you exactly what to look for.

6. **Write the brief:** ranked query table (query, growth, which seed
   surfaced it) + 3–5 article angles for your publication, each tied to a
   specific spike. Headline-style, in your publication's voice.

## Operating rules

1. **Verify the storm before running** — no speculative trend-chasing.
2. **Never invent growth numbers.** If a section is blocked, say so. Honest
   provenance: label every number as measured or don't include it.
3. **The brief is the product.** This kit produces a publishing brief; your
   editorial desk decides what ships.
4. **Recency matters.** Run within 72 hours of the event. After a week the
   spike is usually over.
5. **Keep runs polite.** The script sleeps 6s between calls. Don't
   parallelize or hammer the endpoints — Google will block you, and the
   script will tell you so honestly.
