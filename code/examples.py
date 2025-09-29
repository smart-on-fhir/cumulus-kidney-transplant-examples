import os
import csv
import pandas as pd
from pandas import DataFrame
from pathlib import Path

def read_csv(file_csv: Path | str) -> DataFrame:
    """
    GPT5 generated CSV files are sometimes not formatted perfectly.
    :param file_csv: Path or str of file to read
    :return: DataFrame
    """
    return pd.read_csv(
        file_csv,
        sep=",",  # use a literal comma, not a regex
        quotechar='"',  # fields like "CMV, EBV, ..." stay intact
        quoting=csv.QUOTE_MINIMAL,
        skipinitialspace=True  # ignores the space after commas
    )

def str_patient(patient_num) -> str:
    if 'patient' not in str(patient_num):
        return f'patient-{patient_num}'
    return patient_num

def str_encounter(encounter_num) -> str:
    if 'encounter' not in str(encounter_num):
        return f'encounter-{encounter_num}'
    return encounter_num

def str_document(document_num) -> str:
    if 'document' not in str(document_num):
        return f'document-{document_num}'
    return document_num

def dir_examples() -> Path:
    return Path(os.path.dirname(__file__)).parent / 'examples'

def dir_fhir() -> Path:
    return dir_examples() / 'fhir'

def dir_patient(patient_num) -> Path:
    return dir_examples() / str_patient(patient_num)

def dir_documents(patient_num) -> Path:
    return dir_patient(patient_num) / 'documents'

def file_patients_csv() -> Path:
    return dir_examples() / 'patients.csv'

def file_encounters_csv(patient_num) -> Path:
    return dir_patient(patient_num) / 'encounters.csv'

def file_documents_csv(patient_num) -> Path:
    return dir_patient(patient_num) / 'documents.csv'

def file_document_txt(patient_num, encounter_num, document_num) -> Path:
    encounter_num = str_encounter(encounter_num)
    document_num = str_document(document_num)
    return dir_documents(patient_num)/ f'{encounter_num}_{document_num}.txt'

def read_patients_csv() -> DataFrame:
    return read_csv(file_patients_csv())

def read_encounters_csv(patient_num) -> DataFrame:
    return read_csv(file_encounters_csv(patient_num))

def read_documents_csv(patient_num) -> DataFrame:
    return read_csv(file_documents_csv(patient_num))

def list_patient_csv() -> list[str]:
    return list(read_patients_csv()['patient_num'])

def list_document_csv(patient_num) -> list[str]:
    return list(read_documents_csv(patient_num)['document_num'])

def markdown(filename_csv:Path):
    df = read_csv(filename_csv)
    with open(filename_csv.with_suffix('.md'), "w") as f:
        f.write(df.to_markdown(index=False))

def read_text(file_csv: Path | str) -> str:
    with open(file_csv, 'r') as f:
        return f.read()
