from pathlib import Path
import examples

def make_readme() -> Path:
    file_md = examples.dir_examples() / "README.md"
    df = examples.read_patients_csv()
    df["chatgpt"] = df["chatgpt"].str.strip().apply(lambda x: f"[chatgpt]({x})")
    df["encounters"] = df["patient_num"].str.strip().apply(lambda x: f"[encounters]({x}/encounters.md)")
    df["documents"] = df["patient_num"].str.strip().apply(lambda x: f"[documents]({x}/documents.md)")
    df = df[["patient_num", "encounters", "documents", "chatgpt", "example_prompt"]]
    with open(file_md, "w") as f:
        f.write(df.to_markdown(index=False))
    return file_md

if __name__ == "__main__":
    print('Making markdown.')
    make_readme()
    for patient_num in examples.list_patient_csv():
        examples.markdown(examples.dir_patient(patient_num) / 'patient.csv')
        examples.markdown(examples.dir_patient(patient_num) / 'encounters.csv')
        examples.markdown(examples.dir_patient(patient_num) / 'documents.csv')
    print('README is ready.')

