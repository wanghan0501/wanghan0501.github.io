"""
Fetch per-paper citation counts from OpenAlex and emit the same JSON
artifacts the site consumes. Stdlib only - no pip dependencies.

- One API call per DOI (site paper list is the source of truth; join by DOI,
  not fuzzy titles).
- Total citations = sum over site papers. Do NOT use OpenAlex author-level
  cited_by_count: this author profile aggregates namesake works.
- Guard: if fewer than MIN_MATCHED papers resolve, treat OpenAlex as down,
  fail without writing, so the google-scholar-stats branch keeps its last
  good data.
"""

import json
import os
import time
import urllib.error
import urllib.request

# Papers listed on the homepage (about.md / about-en.md), keyed by DOI.
PAPERS = {
    "10.1038/s41467-026-73170-5": "Breast ultrasound assistance (Nat Commun 2026)",
    "10.1038/s41467-026-69303-5": "3D molecule conformation assessment (Nat Commun 2026)",
    "10.1038/s42256-023-00775-6": "Pocket 3D molecule generation (Nat Mach Intell 2024)",
    "10.1109/TAI.2023.3285855": "Survival analysis on WSI (IEEE TAI 2023)",
    "10.1109/TMI.2022.3149168": "RECISTSup (IEEE TMI 2022)",
    "10.1002/int.22452": "Pelvic lymph node detection (IJIS 2021)",
    "10.1002/int.22280": "DeepEC dose correction (IJIS 2020)",
    "10.1007/s10489-021-02784-7": "Glioma multi-view segmentation (Applied Intelligence 2022)",
    "10.64898/2026.08.24.745890": "RCDO preprint (bioRxiv 2026)",
    "10.1101/2025.11.13.688260": "CBL-B preprint (bioRxiv 2025)",
    "10.1101/2025.09.23.678079": "HPK1 preprint (bioRxiv 2025)",
    "10.64898/2026.05.27.728070": "Nucleoside crystal preprint (bioRxiv 2026)",
}

MIN_MATCHED = 8          # of len(PAPERS); below this, treat OpenAlex as down
MAILTO = "hanwang@pku.edu.cn"
TIMEOUT = 30             # seconds per request
RETRIES = 3


def fetch_citations(doi: str) -> int | None:
    """Return cited_by_count for a DOI, or None on repeated failure."""
    url = f"https://api.openalex.org/works/doi:{doi.lower()}?mailto={MAILTO}"
    for attempt in range(1, RETRIES + 1):
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:
                data = json.load(resp)
            if "error" in data:
                raise ValueError(f"OpenAlex error for {doi}: {data.get('error')}")
            return int(data["cited_by_count"])
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
            print(f"  attempt {attempt}/{RETRIES} failed for {doi}: {exc}")
            if attempt < RETRIES:
                time.sleep(2 * attempt)
    return None


def main():
    publications = {}
    matched = 0
    for doi, label in PAPERS.items():
        count = fetch_citations(doi)
        if count is None:
            print(f"MISS  {doi}  {label}")
            continue
        matched += 1
        publications[doi.lower()] = {"num_citations": count}
        print(f"OK    {doi}  {label}  ->  {count}")

    if matched < MIN_MATCHED:
        print(
            f"Only {matched}/{len(PAPERS)} papers resolved from OpenAlex; "
            "treating as API outage, not writing results."
        )
        raise SystemExit(1)

    total = sum(v["num_citations"] for v in publications.values())
    updated = time.strftime("%Y-%m-%d %H:%M:%S")
    gs_data = {
        "citedby": total,
        "name": "Han Wang",
        "updated": updated,
        "publications": publications,
    }
    shieldsio = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(total),
    }

    os.makedirs("results", exist_ok=True)
    with open("results/gs_data.json", "w", encoding="utf-8") as f:
        json.dump(gs_data, f, ensure_ascii=False, indent=2)
    with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
        json.dump(shieldsio, f, ensure_ascii=False, indent=2)

    print(f"TOTAL citations (sum over {matched} papers): {total}")
    print(f"UPDATED {updated}")


if __name__ == "__main__":
    main()
