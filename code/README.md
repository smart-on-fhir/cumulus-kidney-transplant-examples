# Technical Users

### (optional) Steps to recreate the example prompts, CSV, and TXT files  
Requires: `Python3.11` and `ChatGPT`

Setup  
```
$ git clone git@github.com:smart-on-fhir/cumulus-kidney-transplant-examples.git
$ cd cumulus-kidney-transplant-examples/code 

$ python3 -m venv ve; source ve/bin/activate
$ pip install -r requirements.txt
```

### 1. Generate GPT prompts

$ `python3` [step_1_prompt.py](step_1_prompt.py) 

Will generate prompts for each patient in [patients.csv](../examples/patients.csv). 

The prompt will use the template from [step_1_prompt.txt](code/step_1_prompt.txt) . 

Paste your `examples`/**patient_num**/`step1_prompt.txt` into https://chatgpt.com/

### 2. ChatGPT download 

Paste [step_2_download.txt](step_2_download_csv.txt) to get a Downloadable ZIP file with 
* `patient.csv`
* `encounters.csv`
* `documents.csv`

### 3. ChatGPT Batch downloads of TXT files 

Paste [step_3_download_txt.txt](step_3_download_txt.txt) into https://chatgpt.com/

This is the most time-consuming part. GPT5 does a **good** job at generating TXT but struggles to provide downloadable ZIP files. 
You will likely need to Download ZIP in "batches".   

### 4. Crosscheck CSV and TXT generated files

Even GPT5 "_can make mistakes_". 

$`python3` [step_4_crosscheck.py](step_4_crosscheck.py)

```
✅  patient_1
✅  patient_2
✅  patient_3
✅  patient_4
✅  patient_5
✅  patient_6
✅  patient_7
✅  patient_8
✅  patient_9
✅  patient_10
```

### 5. Create FHIR DocumentReference  

$ `python3` [step_5_create_docref.py](step_5_create_docref.py) 

Generates [docref-data.csv](docref-data-simple.csv) for use in Cumulus ETL and chart-review steps. 


## Sites should load documents into LabelStudio for [Cumulus chart review](https://docs.smarthealthit.org/cumulus/chart-review/).

Placeholder text for Dylan/Mike 
