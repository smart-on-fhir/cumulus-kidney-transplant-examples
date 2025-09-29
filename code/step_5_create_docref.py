import uuid
import base64
import hashlib
import json
from enum import Enum
from typing import Any
from pathlib import Path
import pandas as pd
import examples

########################################################################################################################
# User choice of FHIR Reference type : UUUID, SHA1, or human readable.
########################################################################################################################
NAMESPACE = uuid.UUID("12345678-1234-5678-1234-567812345678")
SEPERATOR = '-' # ID seperator

class IDType(Enum):
    simple = 'simple human readable name, best for debugging'
    hash = 'hash using sha1, when short hashes are preferred'
    uuid = 'fhir maximal standards compatibility with much longer IDs'

def map_id(*parts, id_type=IDType.simple) -> str:
    """
    :param parts: one or more {subject, encounter, document}
    :param id_type: simple, hash, or uuid
    :return: str Identifier for resource
    """
    if isinstance(id_type, str):
        id_type = IDType[id_type]  # convert string -> Enum

    if id_type == IDType.hash:
        return hash_id(*parts)
    if id_type == IDType.uuid:
        return uuid_id(*parts)
    else:
        return simple_id(*parts)

def simple_id(*parts) -> str:
    return SEPERATOR.join(str(p) for p in parts)

def hash_id(*parts, length=10) -> str:
    text = SEPERATOR.join(str(p) for p in parts)  # join patient, encounter, and/or document.
    return hashlib.sha1(text.encode()).hexdigest()[:length]

def uuid_id(*parts) -> str:
    text = simple_id(*parts)
    return str(uuid.uuid5(NAMESPACE, text))

def make_map_csv(output_path: Path | str, id_type = None) -> pd.DataFrame:
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
                "patient_num":      patient_num,
                "subject_id":       map_id(patient_num, id_type=id_type),
                "encounter_num":    row.encounter_num,
                "encounter_id":     map_id(patient_num, row.encounter_num, id_type=id_type),
                "document_num":     row.document_num,
                "documentref_id":   map_id(patient_num, row.encounter_num, row.document_num, id_type=id_type),
                "date":             row.encounter_date,
                "type_display":     row.document_title,
                "path":             document_file
            })

    df = pd.DataFrame(docref_list)
    df = df[["patient_num",
             "subject_id",
             "encounter_num",
             "encounter_id",
             "document_num",
             "documentref_id",
             "date",
             "type_display",
             "path"]]
    df.to_csv(output_path, index=False)
    print('✅ ', output_path)
    return df

def make_fhir_ndjson(csv_path: Path, output_dir: Path) -> None:
    df: pd.DataFrame = examples.read_csv(csv_path)
    for _, row in df.iterrows():
        resource: dict[str, Any] = make_fhir_documentreference(row)
        out_file: Path = output_dir / f"{row['subject_id']}_{row['documentref_id']}.ndjson"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(resource, f, indent=4)
    print('✅ ', output_dir)

def make_fhir_documentreference(row: pd.Series) -> dict[str, Any]:
    document_path = examples.dir_examples().parent.joinpath(Path(row['path']))
    with open(document_path, "rb") as f:
        file_content = f.read()

    mimetype = "text/plain"
    encoding = "utf-8"
    attachment: dict[str, Any] = {
        "data": base64.standard_b64encode(file_content).decode("ascii"),
        "contentType": f"{mimetype}; charset={encoding}",
        "title": f"{row['documentref_id']} ({row['date']})",
    }

    doc_ref: dict[str, Any] = {
        "resourceType": "DocumentReference",
        "id": str(row['documentref_id']),
        "subject": {"reference": f"Patient/{row['subject_id']}"},
        "encounter": {"reference": f"Encounter/{row['encounter_id']}"},
        "date": row['date'],
        "type": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "display": str(row['type_display'])
                }
            ]
        },
        "content": [{"attachment": attachment}]
    }
    return doc_ref

if __name__ == "__main__":
    map_csv_file = examples.dir_fhir() / 'mapping.csv'
    fhir_ndjson_dir = examples.dir_fhir() / 'ndjson'
    fhir_ndjson_dir.mkdir(parents=True, exist_ok=True)
    make_map_csv(map_csv_file, id_type=IDType.simple)
    make_fhir_ndjson(map_csv_file, fhir_ndjson_dir)
