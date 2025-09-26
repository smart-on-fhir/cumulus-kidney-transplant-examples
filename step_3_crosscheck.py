import pandas as pd
import examples

def crosscheck_encounter_date(patient_num):
    encounters_path = examples.file_encounters_csv(patient_num)
    documents_path = examples.file_documents_csv(patient_num)

    encounters = pd.read_csv(encounters_path,   dtype={"encounter_num": str, "encounter_date": str})
    documents = pd.read_csv(documents_path,     dtype={"encounter_num": str, "encounter_date": str})

    enc_dates = encounters[["encounter_num", "encounter_date"]].drop_duplicates()
    doc_dates = documents[["encounter_num", "encounter_date"]].drop_duplicates()

    merged = pd.merge(enc_dates, doc_dates, on="encounter_num", how="outer", suffixes=("_enc", "_doc"))
    mismatches = merged[merged["encounter_date_enc"] != merged["encounter_date_doc"]]

    if not mismatches.empty:
        print("❌ Mismatches found:")
        print(mismatches)
        raise Exception('Mismatched encounter_date(s)')


def crosscheck_txt(patient_num):
    for row in examples.read_documents_csv(patient_num).itertuples():
        document_file = examples.file_document_txt(patient_num, row.encounter_num, row.document_num)
        if not document_file.exists():
            print("❌ File Not Found:")
            print(str(document_file))
            raise Exception(f"{document_file} does not exist")

if __name__ == "__main__":
    for patient_num in examples.list_patient_csv():
        crosscheck_txt(patient_num)
        crosscheck_encounter_date(patient_num)
        print('✅ ', patient_num)


