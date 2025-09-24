import pandas as pd

for patient in range(1, 2):
    df = pd.read_csv("./examples/patient_1/documents.csv")
    markdown_table = df.to_markdown(index=False)

    with open("./examples/patient_1/documents.md", "w") as f:
        f.write(markdown_table)
