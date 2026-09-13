# Storm-Trends Trigger

A storm hits a region. Within hours, homeowners start searching for help.
This kit catches the rising queries and turns them into publishable article
angles — fast enough to rank while demand is spiking.

## The idea

Severe weather creates instant, local, high-intent search demand. Google
Trends shows you which queries are breaking out *right now*, in which metros.
That data becomes your editorial calendar for the week: write what people are
already searching for, before your competitors notice.

Works for any trade vertical: restoration, roofing, HVAC, plumbing, tree
service, disaster recovery — anything where weather drives demand.

## The loop

1. **Verify the storm.** News, NWS alerts, governor/SBA declarations.
   Never run this on a rumor.
2. **Pick storm type + location.** `hail | tornado | hurricane | wind | flood`
   + city/state, e.g. `--storm-type hail --location "San Antonio TX" --geo US-TX`.
3. **Run the script.** `bin/storm_trends.py` pulls rising queries per storm
   type via pytrends. Each section reports `ok` or `blocked` — honestly.
4. **Rank the spikes.** Breakout and high-growth queries, hottest metros.
5. **Write the brief.** 3–5 article angles, each tied to a specific spike.

## What's in this kit

- `TRIGGER.md` — the full workflow and operating rules.
- `bin/storm_trends.py` — the trends puller (pytrends; sleeps 6s between
  calls, degrades gracefully, never invents numbers).
- `examples/worked-example.md` — a real run, start to finish, including
  what a blocked run looks like.

## Status

Extracted 2026-09-13 from a production trigger running every 3 hours since
2026-09-09. Real measured result: a Sep 13 flash-flood warning surfaced
`flood damage restoration` and `flood restoration companies` as Breakout
queries the same morning.

Offered as-is: take it, make it better — if you build something better,
we'll be customer #1 and we'll pay you for it.
