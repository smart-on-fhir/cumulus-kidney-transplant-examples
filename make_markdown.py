import pandas as pd

for num in range(1, 2):
    folder = f"./examples/patient_{num}"
    df = pd.read_csv(f"{folder}/notes.csv")
    pretty = df.to_markdown(index=False)

    with open(f"{folder}/notes.md", "w") as f:
        f.write(pretty)
