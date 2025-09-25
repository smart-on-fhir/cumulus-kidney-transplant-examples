Kidney Transplant Patient Chart Review Dataset
----------------------------------------------

Scenario:
This dataset contains synthetic but realistic clinical documentation for a kidney transplant recipient (KTP) who experiences gaps in care and receives follow-up at more than one healthcare system. The patient demonstrates periods of missed visits, outside facility care, adherence concerns, development of donor-specific antibodies (DSA), and treatment with IVIG.

Structure:
- Files are named as encounter_##_document_##.txt
- summary.csv contains the index of encounters, dates, and document titles.
- Notes are written in dictation-style prose, similar to real-world provider documentation.
- Each document is moderate length (2–3 rich paragraphs) and includes typical transplant note content such as HPI, medications, labs, imaging, and assessment/plan.

Intended Use:
- For training and calibration of chart reviewers, particularly transplant nephrology reviewers.
- To provide realistic exposure to longitudinal kidney transplant documentation with multi-site complexity and adherence gaps.

Total contents:
- 29 clinical note files
- 1 summary.csv index file
- 1 README.txt file
