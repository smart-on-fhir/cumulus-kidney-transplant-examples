# Kidney Transplant Note Examples
### No PHI  
These are synthetic notes -- **not** PHI (protected health information).
 
## Clinical Research Users
See `examples` [README](examples/README.md) for kidney transplant patient (KTP) examples.

Intended for **Kidney Transplant** subject-matter-experts (SME) chart review practice/tutorials 
* MD / providers
* PhD / researchers
* Medical school students
* Other chart reviewers

## Technical Users
See `code` [README.md](code/README.md) for steps to update/recreate KTP examples.  

Those following along with the [cumulus-library-kidney-transplant](https://github.com/smart-on-fhir/cumulus-library-kidney-transplant/blob/main/RUNNING.md) running 
instructions can either run the steps detailed in that document while pointing at the 
NDJSON in `examples/fhir/ndjson`, or they can jump to populating a labelstudio project 
with the provided `examples/fhir/labelstudio-export.json` file using the typical import UI. 

**Note:** the target project needs to have a labeling interface before importing these 
tasks. Make sure you have already [set that up](https://github.com/smart-on-fhir/cumulus-library-kidney-transplant/blob/main/RUNNING.md#6-configure-label-studio).
