import argparse
import base64
import pandas as pd
from pathlib import Path
from typing import Dict, Any

def generate_document_reference(row: pd.Series, csv_path: Path) -> Dict[str, Any]:
    with open(csv_path.parent.joinpath(row['path']), "rb") as f:
        file_content = f.read()

    mimetype = "text/plain"
    encoding = "utf-8"
    attachment: Dict[str, Any] = {
        "data": base64.standard_b64encode(file_content).decode("ascii"),
        "contentType": f"{mimetype}; charset={encoding}",
        "title": Path(row['path']).name
    }

    doc_ref: Dict[str, Any] = {
        "resourceType": "DocumentReference",
        "id": str(row['documentref_ref']),
        "subject": {"reference": f"Patient/{row['subject_ref']}"},
        "encounter": {"reference": f"Encounter/{row['encounter_ref']}"},
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

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate FHIR DocumentReference resources from metadata CSV.")
    parser.add_argument("csv_path", type=str, help="Path to input CSV file.")
    parser.add_argument("output_dir", type=str, help="Directory to write FHIR resources.")
    return parser

def validate_args(args) -> tuple[Path, Path] | None:
    csv_path: Path = Path(args.csv_path)
    output_dir: Path = Path(args.output_dir)

    if not csv_path.exists():
        print(f"Error: CSV file '{csv_path}' does not exist.")
        return None
    if not csv_path.is_file():
        print(f"Error: '{csv_path}' is not a file.")
        return None
    if csv_path.suffix.lower() != ".csv":
        print(f"Error: '{csv_path}' is not a CSV file.")
        return None

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error: Could not create output directory '{output_dir}': {e}")
        return None

    return csv_path, output_dir

def generate_doc_refs(csv_path: Path, output_dir: Path) -> None:
    df: pd.DataFrame = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        resource: Dict[str, Any] = generate_document_reference(row, csv_path)
        out_file: Path = output_dir / f"{row['subject_ref']}_{row['documentref_ref']}.ndjson"
        with open(out_file, "w", encoding="utf-8") as f:
            import json
            json.dump(resource, f)

def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    validated = validate_args(args)
    if validated is None:
        print("Argument validation failed. Exiting.")
        return
    
    csv_path, output_dir = validated
    generate_doc_refs(csv_path, output_dir)

if __name__ == "__main__":
    main()
