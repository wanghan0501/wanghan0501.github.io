"""
Fetch Google Scholar author stats via SerpAPI and emit the same JSON
artifacts the site consumes. Stdlib only - no pip dependencies.

SerpAPI maintains residential+mobile pools specialized in unblocking Google,
the only proven working path after Scholar blocked datacenter/scraper IPs.

Output (same format as the original scholarly-based main.py):
  results/gs_data.json           {citedby, name, updated, publications{}}
  results/gs_data_shieldsio.json {schemaVersion, label, message}
"""

import json
import os
import time
import urllib.parse
import urllib.request

# Single request returns everything needed for the badge and per-paper stats.
API_URL = (
    "https://serpapi.com/search.json"
    "?engine=google_scholar_author"
    "&author_id={scholar_id}"
    "&num=100"
    "&api_key={key}"
)


def main() -> None:
    scholar_id = os.environ["GOOGLE_SCHOLAR_ID"]
    api_key = os.environ["SERPAPI_KEY"]
    url = API_URL.format(scholar_id=urllib.parse.quote(scholar_id), key=urllib.parse.quote(api_key))

    req = urllib.request.Request(url, headers={"User-Agent": "gs-crawler/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.load(resp)

    if "error" in data:
        print(f"SerpAPI error: {data['error']}")
        raise SystemExit(1)
    table = data.get("cited_by", {}).get("table", [])
    if not table or "citations" not in table[0]:
        print("Unexpected SerpAPI response shape, not writing results.")
        raise SystemExit(1)

    citedby = int(table[0]["citations"]["all"])
    name = data.get("author", {}).get("name", "Han Wang")
    publications = {
        a["citation_id"]: {
            "num_citations": int((a.get("cited_by") or {}).get("value") or 0),
            "title": a.get("title", ""),
        }
        for a in data.get("articles", [])
        if a.get("citation_id")
    }

    updated = time.strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs("results", exist_ok=True)
    with open("results/gs_data.json", "w", encoding="utf-8") as f:
        json.dump(
            {"citedby": citedby, "name": name, "updated": updated, "publications": publications},
            f, ensure_ascii=False, indent=2,
        )
    with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
        json.dump(
            {"schemaVersion": 1, "label": "citations", "message": str(citedby)},
            f, ensure_ascii=False, indent=2,
        )

    print(f"OK {name}: citedby={citedby}, publications={len(publications)}, updated={updated}")


if __name__ == "__main__":
    main()
