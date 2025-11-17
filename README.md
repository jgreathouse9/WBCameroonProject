# Recplicating "Economic Impact of Cameroon’s Anglophone Crisis: A Forward Difference-in-Differences Approach"

This repository contains the code and data used to perform FDID (Forward Difference-in-Differences) analysis for the paper "Economic Impact of Cameroon’s Anglophone Crisis: A Forward
Difference-in-Differences Approach". Here is how to reproduce our results.

---

## Project Structure

```
cameroon_fdid/
├─ __init__.py
├─ cameroon_results_vectorized.py
├─ NordOuest.csv
├─ SudOuest.csv
.github/workflows/runresults.yml
pyproject.toml
poetry.lock
fdid_summary_output2.txt
```

---

## Requirements

* Python 3.12
* Poetry (dependency management and environment reproducibility)
* Git (to clone the repo)

All Python dependencies are defined in `pyproject.toml`.

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/jgreathouse9/WBCameroonProject.git
cd WBCameroonProject
```

2. **Install Poetry**

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
```

3. **Install dependencies**

```bash
poetry install --no-interaction --no-ansi
```

This creates a virtual environment and installs all required dependencies.

---

## Run the Analysis

Run the FDID analysis using [```mlsynth```](https://mlsynth.readthedocs.io/en/latest/index.html):

```bash
poetry run python -m cameroon_fdid.cameroon_results_vectorized
```

Outputs will be written to:

```
cameroon_fdid/fdid_summary_output2.txt
```

---

## GitHub Actions

The workflow `runresults.yml` automatically:

* Installs dependencies with Poetry.
* Runs the analysis.
* Commits updated results to the repository.

---

## Notes

* Ensure `pyproject.toml` and `poetry.lock` are up to date to guarantee environment consistency.
* Any new data files should be placed in `cameroon_fdid/` to be included in the analysis.

