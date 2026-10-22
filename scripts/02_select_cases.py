"""Pick the case set: clean, single-finding PTB-XL ECGs whose PTB-XL labels are the reference standard (v3, 2026-10-18).

Non-MI groups: folds 9-10 (human-validated test folds), no noise/drift/electrode flags, the target finding
at 100% likelihood (rhythm codes: present), no competing major finding, and no ambiguous secondary statement
(LVH voltage, IVCD outside LBBB, ischaemia/injury, "probable/possible" AF).
MI groups use PTB-XL's infarction stage, because MI statements alone do not separate acute from old MI:
  acute_mi = infarction_stadium1 "Stadium I" or "Stadium I-II"; old_mi = "Stadium III" with no injury statement.
Acute-stage MI is rare in folds 9-10 (17 clean records), so both MI groups draw from every human-validated fold.
Fixed seed, so reruns are identical. No new human labels are collected: PTB-XL is the reference standard.

History (archived in data/cases/): v1 2026-10-12 had ambiguous secondary labels (found by an 8-case pilot);
v2 2026-10-18 fixed that but had no acute-stage MI and relied on a clinician review that could not be done.
Usage: .venv/bin/python scripts/02_select_cases.py  ->  data/cases/candidates.csv
Case IDs are neutral (E001...) and shuffled, so neither an image filename nor the row order reveals the label.
"""
import ast
import pandas as pd

SEED = 20261012
MI_CODES = {"AMI", "ASMI", "ALMI", "IMI", "ILMI", "IPLMI", "IPMI", "LMI", "PMI",
            "INJAS", "INJAL", "INJIN", "INJIL", "INJLA"}
MAJOR = MI_CODES | {"NORM", "AFIB", "AFLT", "CLBBB", "CRBBB", "WPW", "1AVB", "LVH",
                    "IRBBB", "ILBBB", "LAFB", "LPFB", "2AVB", "3AVB", "PACE", "PVC", "BIGU", "TRIGU"}
UNCERTAIN = ("probable", "possible", "wahrscheinlich", "verdacht")
STAGE = {"acute_mi": {"Stadium I", "Stadium I-II"}, "old_mi": {"Stadium III"}}

# group -> (codes that define it, how many to sample)
GROUPS = {
    "normal":         ({"NORM"}, 20),
    "afib":           ({"AFIB"}, 10),
    "lbbb":           ({"CLBBB"}, 10),
    "rbbb":           ({"CRBBB"}, 10),
    "wpw":            ({"WPW"}, 8),
    "first_deg_avb":  ({"1AVB"}, 8),
    "acute_mi":       (MI_CODES, 25),
    "old_mi":         (MI_CODES, 10),
}


def ambiguous(group, scp, report):
    """Secondary findings that compete with the target as the single main diagnosis."""
    if set(scp) & {"VCLVH", "LVH", "SEHYP"}:
        return True
    if "IVCD" in scp and group != "lbbb":
        return True
    if group not in STAGE and any(k.startswith(("ISC", "INJ")) for k in scp):
        return True
    if group == "old_mi" and any(k.startswith("INJ") for k in scp):
        return True                                   # an injury statement means ongoing, not old
    return group == "afib" and any(w in str(report).lower() for w in UNCERTAIN)


def fits(group, codes, scp):
    if group in STAGE:
        return bool(set(scp) & codes) and not (set(scp) & MAJOR - MI_CODES)
    # PTB-XL gives rhythm codes (AFIB) likelihood 0, so presence is enough for them.
    hit = any(c in scp and (scp[c] >= 100 or c == "AFIB") for c in codes)
    return hit and not (set(scp) & MAJOR - codes)


def main():
    d = pd.read_csv("data/ptbxl/ptbxl_database.csv", index_col=0)
    d["scp"] = d.scp_codes.apply(ast.literal_eval)
    base = d[d.validated_by_human & d.baseline_drift.isna() & d.static_noise.isna()
             & d.burst_noise.isna() & d.electrodes_problems.isna()]

    picked = []
    for group, (codes, n) in GROUPS.items():
        src = base[base.infarction_stadium1.isin(STAGE[group])] if group in STAGE else base[base.strat_fold >= 9]
        pool = src[[fits(group, codes, s) and not ambiguous(group, s, rep) for s, rep in zip(src.scp, src.report)]]
        take = pool.sample(n=min(n, len(pool)), random_state=SEED)
        print(f"{group:14} pool={len(pool):4} picked={len(take)}")
        for ecg_id, r in take.iterrows():
            picked.append({"ecg_id": ecg_id, "group": group,
                           "ptbxl_codes": ";".join(f"{k}:{int(v)}" for k, v in r.scp.items()),
                           "infarction_stadium": r.infarction_stadium1 if isinstance(r.infarction_stadium1, str) else "",
                           "strat_fold": r.strat_fold, "report_de": r.report,
                           "age": r.age, "sex": "M" if r.sex == 0 else "F", "filename_hr": r.filename_hr})
    out = pd.DataFrame(picked).sample(frac=1, random_state=SEED).reset_index(drop=True)
    out.insert(0, "case_id", [f"E{i + 1:03d}" for i in range(len(out))])
    out.to_csv("data/cases/candidates.csv", index=False)
    print("total", len(out), "-> data/cases/candidates.csv")


if __name__ == "__main__":
    main()
