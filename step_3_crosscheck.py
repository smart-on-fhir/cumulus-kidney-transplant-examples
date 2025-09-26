#!/usr/bin/env python3
import sys
from pathlib import Path
import pandas as pd
import examples

###################################################################################################################
#
README = "GPT5 wrote this validator for its own output with minimal modifications"
#
###################################################################################################################

def crosscheck_csv(patient_num):
    encounters_path = examples.file_encounters_csv(patient_num)
    documents_path = examples.file_documents_csv(patient_num)

    e = pd.read_csv(encounters_path, dtype={"encounter_num": str, "encounter_date": str}, skipinitialspace=True)
    d = pd.read_csv(documents_path,  dtype={"encounter_num": str, "encounter_date": str}, skipinitialspace=True)

    # Minimal column check
    need_e = {"encounter_num", "encounter_date", "encounter_summary"}
    need_d = {"encounter_num", "encounter_date", "document_num", "document_title"}
    missing = []
    if not need_e.issubset(e.columns): missing.append(f"{encounters_path} missing {need_e - set(e.columns)}")
    if not need_d.issubset(d.columns): missing.append(f"{documents_path} missing {need_d - set(d.columns)}")
    if missing:
        print("COLUMN ERROR:")
        for m in missing: print(" -", m)
        sys.exit(1)

    # Optional: detect conflicting dates within each file (same encounter_num -> different dates)
    e_conflict = (e.groupby("encounter_num")["encounter_date"].nunique() > 1)
    d_conflict = (d.groupby("encounter_num")["encounter_date"].nunique() > 1)
    e_conflict_ids = e_conflict[e_conflict].index.tolist()
    d_conflict_ids = d_conflict[d_conflict].index.tolist()

    if e_conflict_ids:
        print("INTRA-FILE DATE CONFLICT in encounters.csv for encounter_num:", e_conflict_ids)
    if d_conflict_ids:
        print("INTRA-FILE DATE CONFLICT in documents.csv for encounter_num:", d_conflict_ids)

    # Reduce to unique mapping encounter_num -> encounter_date for comparison
    e_map = e.drop_duplicates(subset=["encounter_num"])[["encounter_num", "encounter_date"]]
    d_map = d.drop_duplicates(subset=["encounter_num"])[["encounter_num", "encounter_date"]]

    # 1) Presence in both CSVs
    e_ids = set(e_map["encounter_num"])
    d_ids = set(d_map["encounter_num"])
    only_in_e = sorted(e_ids - d_ids)
    only_in_d = sorted(d_ids - e_ids)

    # 2) Date match across files
    merged = e_map.merge(d_map, on="encounter_num", how="inner", suffixes=("_encounters", "_documents"))
    date_mismatch = merged[merged["encounter_date_encounters"] != merged["encounter_date_documents"]]

    ok = True
    if only_in_e:
        ok = False
        print("MISSING IN documents.csv (present in encounters.csv only):", only_in_e)
    if only_in_d:
        ok = False
        print("MISSING IN encounters.csv (present in documents.csv only):", only_in_d)
    if not date_mismatch.empty:
        ok = False
        print("DATE MISMATCHES:")
        print(date_mismatch.to_string(index=False))

    if e_conflict_ids or d_conflict_ids:
        ok = False

    if ok:
        print("✅ Validation passed: encounter_num sets match and all encounter_date values agree.")
        sys.exit(0)
    else:
        print("❌ Validation failed. See details above.")
        sys.exit(2)

def crosscheck_txt(patient_num):
    for row in examples.read_documents_csv(patient_num).itertuples():
        document_file = examples.file_document_txt(patient_num, row.encounter_num, row.document_num)
        if not document_file.exists():
            raise Exception(f"{document_file} does not exist")

if __name__ == "__main__":
    for patient_num in examples.list_patient_csv():
        crosscheck_csv(patient_num)
        crosscheck_txt(patient_num)

