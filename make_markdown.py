import pandas as pd

for num in range(1, 10):
    folder = f"./examples/patient_{num}"
    df = pd.read_csv(f"{folder}/summary.csv")
    pretty = df.to_markdown(index=False)

    with open(f"{folder}/summary.md", "w") as f:
        f.write(pretty)
