# Kidney Transplant Note Examples
### No PHI  
These are synthetic notes -- **not** PHI (protected health information).
 
### Clinical audiences
Intended for **Kidney Transplant** subject-matter-experts (SME) chart review practice/tutorials 
* MD / providers
* PhD / researchers
* Medical school students
* Other chart reviewers 

### Technical audiences
Sites should load documents into LabelStudio for [Cumulus chart review](https://docs.smarthealthit.org/cumulus/chart-review/).

#### GPT5 prompt

Task 1 summary  
```
You are a chart review expert and your task is to generate examples of kidney transplant patient (KTP) clinical documentation. 
The clinical documentation will be read by chart reviewers, especially MD/providers with subject matter expertise in kidney transplants. 
The clinical documentation should be as realistic as possible, representing real world scenarios of patients post transplant.

Your first task is to generate a CSV summarizing a single patient post kidney transplant and at least 3 months of clinical followup. 
CSV columns: encounter_num, encounter_date, document_num, document_title 

Take time to think about your answer and then respond with a single KTP patient `summary.csv` file.
This is an interactive session. After you provide the `summary.csv`, I will guide you with further instructions.  
```
Task 2 detail  
```
Generate a realistic, real-world-example for 

encounter_num,encounter_date,document_num,document_title
1,2025-06-03,1,Transplant Surgery Operative Note – Deceased Donor Kidney Transplant

Output to file: encounter_1_note_1.txt 
```