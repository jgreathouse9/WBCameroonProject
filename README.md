# Replication Materials for FDID Analysis

[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://tinyurl.com/yswoudds)

This repository contains the code and materials used to generate the results reported in our paper "Economic Impact of Cameroon’s Anglophone Crisis: A Forward
Difference-in-Differences Approach".

## 🔁 How to Replicate Our Results

To replicate our results:

1. **Click this link**: [LINK](https://mybinder.org/v2/gh/jgreathouse9/WBCameroonProject/b0a4287aeaf5e557021d1a2cb150f62fb89080c9?urlpath=lab%2Ftree%2Farcoanalysis.ipynb)
   *(You will be taken to an interactive Binder environment.)*

2. **Run the code** in the notebook or script provided.

3. When run, the code will automatically generate a file called:
   **`fdid_summary_output.txt`**

This file contains the summary output from the [Forward Difference-in-Differences](https://doi.org/10.1287/mksc.2022.0212) (FDID) and Difference-in-Differences (DID) analyses corresponding to our results section.

## 📁 Repository Contents

* `arcoanalysis.py` — The main analysis script
* `requirements.txt` — Dependencies to run the environment, namely `pandas` and [`mlsynth`](https://mlsynth.readthedocs.io)
* `fdid_summary_output.txt` — (Created at runtime; not stored here)

## 📌 Note on Reproducibility

This Binder session starts from a cold start every time you launch it. Any files generated are **not saved permanently** and will disappear once the session ends.
Let me know if you'd like a version of this with section headers for a paper (e.g., “Data Availability Statement”) or if you want help creating a more formal citation block for the repo.
