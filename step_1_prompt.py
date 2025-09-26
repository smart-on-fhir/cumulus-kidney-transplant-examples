import examples

EXAMPLE_PROMPT = '@@@EXAMPLE_PROMPT@@@'

def make_prompts():
    step1_prompt = examples.read_text('step_1_prompt.txt')

    for row in examples.read_patients_csv().itertuples():
        patient_num = row.patient_num
        example_prompt = row.example_prompt
        if patient_num and example_prompt:
            patient_dir = examples.dir_patient(patient_num)
            patient_dir.mkdir(parents=True, exist_ok=True)

            with open(f"{patient_dir}/step_1_prompt.txt", "w") as f:
                f.write(step1_prompt.replace(EXAMPLE_PROMPT, example_prompt))

if __name__ == "__main__":
    make_prompts()
