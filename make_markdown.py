import pandas as pd

def make_summary_md(num_patients=10):
    for num in range(1, num_patients+1):
        file_csv = f"./examples/patient_{num}/summary.csv"
        file_md = f"./examples/patient_{num}/summary.md"
        print(f"Generating {file_md}")
        df = pd.read_csv(file_csv)
        with open(file_md, "w") as f:
            f.write(df.to_markdown(index=False))

def make_patient_list_md():
    file_csv = f"./examples/patient_list.csv"
    file_md = f"./examples/README.md"
    print(f"Generating {file_md} from {file_csv}")

    df = pd.read_csv(file_csv)
    df["chatgpt"] = df["chatgpt"].str.strip().apply(lambda x: f"[chatgpt]({x})")
    df["summary"] = df["patient_num"].str.strip().apply(lambda x: f"[summary]({x}/summary.md)")
    df = df[["patient_num", "summary", "chatgpt", "description"]]

    with open(file_md, "w") as f:
        f.write(df.to_markdown(index=False))

if __name__ == "__main__":
    make_summary_md(10)
    make_patient_list_md()
