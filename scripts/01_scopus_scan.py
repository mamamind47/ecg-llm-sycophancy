"""Scopus novelty scan for the ECG-sycophancy topic.

Key is read from $SCOPUS_API_KEY or ~/.config/scopus/key (never passed on argv).
Usage: SSL_CERT_FILE=/etc/ssl/cert.pem python3 scripts/01_scopus_scan.py data/scopus_YYYY-MM-DD
"""
import csv, json, os, sys, time, urllib.parse, urllib.request

QUERIES = {
    "q1_ecg_sycophancy":
        'TITLE-ABS-KEY((ecg OR electrocardiogra*) AND sycophan*)',
    "q2_ecg_llm_misleading":
        'TITLE-ABS-KEY((ecg OR electrocardiogra*) AND ("large language model*" OR "vision language model*" OR "multimodal large language model*" OR chatgpt OR "GPT-4" OR "GPT-4o" OR "GPT-5" OR gemini OR claude) '
        'AND (mislead* OR anchor* OR "cognitive bias" OR "automation bias" OR persua* OR "user opinion" OR adversarial OR "prompt sensitivity" OR "clinical context"))',
    "q3_medical_vlm_sycophancy":
        'TITLE-ABS-KEY(sycophan* AND (medical OR clinical OR diagnos*) AND (image* OR vision OR multimodal))',
    "q4_ecg_llm_census":
        'TITLE-ABS-KEY((ecg OR electrocardiogra*) AND ("large language model*" OR "vision language model*" OR "multimodal large language model*" OR chatgpt OR "GPT-4" OR "GPT-4o" OR "GPT-5" OR gemini OR claude)) AND PUBYEAR > 2022',
}

def key():
    k = os.environ.get("SCOPUS_API_KEY")
    if not k:
        with open(os.path.expanduser("~/.config/scopus/key")) as f:
            k = f.read().strip()
    return k

def search(q, apikey, cap=500):
    rows, start = [], 0
    while start < cap:
        url = "https://api.elsevier.com/content/search/scopus?" + urllib.parse.urlencode(
            {"query": q, "start": start, "count": 25, "sort": "-coverDate"})
        req = urllib.request.Request(url, headers={"X-ELS-APIKey": apikey, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)["search-results"]
        total = int(data.get("opensearch:totalResults", 0))
        entries = [e for e in data.get("entry", []) if "error" not in e]
        for e in entries:
            rows.append({
                "title": e.get("dc:title", ""),
                "first_author": e.get("dc:creator", ""),
                "source": e.get("prism:publicationName", ""),
                "date": e.get("prism:coverDate", ""),
                "doi": e.get("prism:doi", ""),
                "cited_by": e.get("citedby-count", ""),
                "type": e.get("subtypeDescription", ""),
            })
        start += 25
        if start >= total or not entries:
            break
        time.sleep(0.2)
    return total, rows

def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    apikey = key()
    for name, q in QUERIES.items():
        total, rows = search(q, apikey)
        path = os.path.join(out_dir, f"{name}.csv")
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["title", "first_author", "source", "date", "doi", "cited_by", "type"])
            w.writeheader(); w.writerows(rows)
        print(f"{name}: total={total} saved={len(rows)} -> {path}")

if __name__ == "__main__":
    main(sys.argv[1])
