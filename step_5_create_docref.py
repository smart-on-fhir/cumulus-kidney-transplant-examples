from pathlib import Path
import uuid
import hashlib
import pandas as pd
import examples

########################################################################################################################
# User choice of FHIR Reference type : UUUID, SHA1, or human readable.
########################################################################################################################
NAMESPACE = uuid.UUID("12345678-1234-5678-1234-567812345678")

def make_ref(*parts):
    return simple_ref(*parts)

def simple_ref(*parts, sep="|"):
    return sep.join(str(p) for p in parts)

def hash_ref(*parts, length=10):
    text = "|".join(str(p) for p in parts)       # join patient, encounter, and/or document.
    return hashlib.sha1(text.encode()).hexdigest()[:length]

def uuid_ref(*parts, sep="|"):
    return uuid.uuid5(NAMESPACE, simple_ref(*parts, sep=sep))

def prepare(output_path: Path | str) -> pd.DataFrame:
    """
    # CSV -> FHIR for Cumulus Chart Review
    # https://docs.smarthealthit.org/cumulus/chart-review/
    """
    docref_list = list()
    for patient_num in examples.list_patient_csv():
        for row in examples.read_documents_csv(patient_num).itertuples():
            document_file = examples.file_document_txt(patient_num, row.encounter_num, row.document_num)
            document_file = document_file.relative_to(examples.dir_examples().parent)

            docref_list.append({
                "subject_id":       make_ref(patient_num),
                "documentref_id":   make_ref(patient_num, row.encounter_num, row.document_num),
                "encounter_id":     make_ref(patient_num, row.encounter_num),
                "date": row.encounter_date,
                "type_display": row.document_title,
                "path": document_file
            })

    df = pd.DataFrame(docref_list)
    df = df[["subject_id", "documentref_id", "encounter_id", "date", "type_display", "path"]]
    df.to_csv(output_path, index=False)
    return df

if __name__ == "__main__":
    prepare('docref-data-uuid.csv')
