# Kidney Transplant Note Examples
### No PHI  
These are synthetic notes -- **not** PHI (protected health information).
 
### Clinical audiences
[README](examples/README.md) example patients.

Intended for **Kidney Transplant** subject-matter-experts (SME) chart review practice/tutorials 
* MD / providers
* PhD / researchers
* Medical school students
* Other chart reviewers

    


### Technical audiences
Sites should load documents into LabelStudio for [Cumulus chart review](https://docs.smarthealthit.org/cumulus/chart-review/).

#### GPT5 prompt

Task 1 `summary.csv`  
```
You are a chart review expert and your task is to generate examples of kidney transplant patient (KTP) clinical documentation. 
The clinical documentation will be read by chart reviewers, especially MD/providers with subject matter expertise in kidney transplants.
Output should read like real scribed provider notes.

Include longitudinal details and typical monitoring for medication adherence, DSA, infection, rejection, and kidney function.  
Include content commonly found in transplant documentation such as history of present illness, medical history, surgeries, medications, allergies, laboratory tests, imaging, and clinical interpretations (both objective and subjective). 

Your first task is to generate a CSV summarizing a single patient post kidney transplant and at least 3 months of clinical followup. 
CSV columns: encounter_num, encounter_date, document_num, document_title 

Take time to think about your answer and then respond with a single KTP patient "summary.csv" file. 
This is an interactive session. I will guide you with further instructions after reviewing your "summary.csv".   
```

Task 2 `encounter_##_document_##.txt`
```
Your second task is to generate realistic, dictation-style, long, real-world-examples for each row in "summary.csv".

Output each document to a file that includes the 2 digit encounter_num and document_num: 
encounter_##_document_##.txt 
```