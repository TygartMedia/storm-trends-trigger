#!/usr/bin/env python3
"""
storm_trends.py — v1: pull rising Google Trends queries for damage/restoration
terms after a storm event, for Restoration Intel content planning.

Usage:
    python3 storm_trends.py --storm-type hail --location "San Antonio TX" --geo US-TX --out trends.json

Technical reality (Sep 2026): the unofficial pytrends endpoints are frequently
blocked from datacenter IPs (HTTP 411/429/timeouts). This script degrades
gracefully: every section reports ok/blocked, and the lightweight
suggestions() endpoint usually still works. When everything is blocked, use the
browser-driven fallback in references/browser_fallback.md.
"""
import argparse, json, sys, time

SEEDS = {
    "hail": ["hail damage roof", "hail damage roof repair", "hail damage claim",
             "roof damage hail storm", "roofing company hail damage"],
    "tornado": ["tornado damage", "tornado damage repair", "storm damage restoration",
                "roof damage tornado", "tornado damage claim"],
    "hurricane": ["hurricane damage repair", "hurricane roof damage",
                  "water damage restoration", "storm damage restoration",
                  "hurricane damage claim"],
    "wind": ["wind damage roof", "wind damage roof repair", "storm damage roof",
             "wind damage claim", "roof repair wind storm"],
    "flood": ["flood restoration", "water damage restoration", "flood damage repair",
              "water mitigation", "flooded basement cleanup"],
}

SLEEP = 6  # seconds between calls; be polite, these endpoints rate-limit hard


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--storm-type", required=True, choices=sorted(SEEDS))
    ap.add_argument("--location", required=True,
                    help='City/state label, e.g. "San Antonio TX" (used for long-tail seeds)')
    ap.add_argument("--geo", default="US",
                    help="pytrends geo code, e.g. US-TX for Texas, US for national")
    ap.add_argument("--timeframe", default="now 7-d",
                    help="pytrends timeframe, e.g. 'now 7-d' or 'today 1-m'")
    ap.add_argument("--out", default="storm_trends_out.json")
    args = ap.parse_args()

    try:
        from pytrends.request import TrendReq
    except ImportError:
        print("pytrends not installed: pip install pytrends", file=sys.stderr)
        sys.exit(2)

    city = args.location.split()[0].lower()
    seeds = SEEDS[args.storm_type]
    out = {"storm_type": args.storm_type, "location": args.location,
           "geo": args.geo, "timeframe": args.timeframe, "sections": {}}

    def section(name, fn):
        try:
            out["sections"][name] = {"status": "ok", "data": fn()}
            print(f"OK: {name}", flush=True)
        except Exception as e:  # noqa: BLE001 — degradation is the point
            out["sections"][name] = {"status": "blocked", "error": str(e)[:200]}
            print(f"BLOCKED: {name}: {str(e)[:100]}", flush=True)
        time.sleep(SLEEP)

    pt = TrendReq(hl="en-US", tz=-360)  # US Central

    # 1. Keyword suggestions — lightest endpoint, usually survives blocking.
    def suggestions():
        res = {}
        for kw in seeds[:3] + [f"{seeds[0]} {city}", f"roof repair {city}"]:
            res[kw] = pt.suggestions(kw)
            time.sleep(2)
        return res
    section("suggestions", suggestions)

    # 2. Rising related queries — the money section when it works.
    def rising():
        res = {}
        for kw in seeds[:3]:
            pt.build_payload([kw], cat=0, timeframe=args.timeframe,
                             geo=args.geo, gprop="")
            rq = pt.related_queries().get(kw, {})
            top = rq.get("top")
            rsg = rq.get("rising")
            res[kw] = {
                "top": top.head(10).to_dict() if top is not None else None,
                "rising": rsg.head(15).to_dict() if rsg is not None else None,
            }
            time.sleep(SLEEP)
        return res
    section("rising_related_queries", rising)

    # 3. Interest over time — confirms the spike is real and current.
    def iot():
        pt.build_payload(seeds[:4], cat=0, timeframe=args.timeframe,
                         geo=args.geo, gprop="")
        return pt.interest_over_time().tail(7).to_dict()
    section("interest_over_time_7d", iot)

    # 4. Interest by subregion — which metros are searching hardest.
    def subregion():
        pt.build_payload(seeds[:2], cat=0, timeframe=args.timeframe,
                         geo=args.geo, gprop="")
        df = pt.interest_by_region(resolution="DMA" if args.geo.startswith("US-")
                                   else "REGION", inc_low_vol=True)
        return df.sort_values(seeds[0], ascending=False).head(10).to_dict()
    section("interest_by_subregion", subregion)

    ok = sum(1 for s in out["sections"].values() if s["status"] == "ok")
    out["summary"] = (f"{ok}/4 sections succeeded. "
                      + ("Use the results below." if ok >= 2 else
                         "Blocked by Google — use references/browser_fallback.md instead."))

    with open(args.out, "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(out["summary"])
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
