"""Check a candidate pool for ambiguous secondary PTB-XL labels (should flag 0 since v2, 2026-10-18).

The 2026-10-15 pilot showed that some candidates carry a secondary PTB-XL statement that competes
with the target as the "single main diagnosis" (e.g. a NORM record also coded VCLVH). The review
package was then rebuilt as v2 with this screen built into scripts/02_select_cases.py.
The flags use only PTB-XL codes and report text, never model answers or the clinical review.
Usage: .venv/bin/python scripts/06_label_flags.py  ->  data/cases/label_flags.csv
"""
import pandas as pd

MI_GROUPS = {"acute_mi", "old_mi"}
UNCERTAIN = ("probable", "possible", "wahrscheinlich", "verdacht")


def flags(r):
    codes = {x.split(":")[0] for x in r.ptbxl_codes.split(";")}
    f = []
    if codes & {"VCLVH", "LVH", "SEHYP"}:
        f.append("lvh_voltage")                      # LVH is itself an answer option
    if "IVCD" in codes and r.group != "lbbb":
        f.append("ivcd")                             # conduction delay competes with BBB / normal
    if r.group not in MI_GROUPS and any(k.startswith(("ISC", "INJ")) for k in codes):
        f.append("ischemia_code")                    # could be read as MI
    if r.group == "afib" and any(w in str(r.report_de).lower() for w in UNCERTAIN):
        f.append("uncertain_af")
    return ";".join(f)


c = pd.read_csv("data/cases/candidates.csv")
c["label_flag"] = c.apply(flags, axis=1)
c[["case_id", "group", "label_flag"]].to_csv("data/cases/label_flags.csv", index=False)
print(f"{(c.label_flag != '').sum()} flagged, {(c.label_flag == '').sum()} kept by rule 0")
