import pandas as pd
from pathlib import Path
from mlsynth import FDID

def run_fdid_batch(directory: Path = Path.cwd()) -> dict:
    """
    Loads all CSVs from a directory, filters and reformats the data,
    then runs FDID on each 'ntl*' outcome variable in each file.

    Returns:
        dict: A dictionary of FDID model results keyed by filename and outcome name.
    """

    def load_and_filter_csvs(directory: Path) -> list[tuple[str, pd.DataFrame]]:
        def parse_quarter_date(qstr):
            year, quarter = qstr.split("_Q")
            month = (int(quarter) - 1) * 3 + 1
            return pd.to_datetime(f"{year}-{month:02d}-01")

        processed = []
        for file in directory.glob("*.csv"):
            df = pd.read_csv(file)

            if "date" not in df.columns:
                continue

            df["date"] = df["date"].apply(parse_quarter_date)

            keep_cols = ["date"] + \
                        [col for col in df.columns if col.startswith("ntl")] + \
                        [col for col in ["treated", "fullname"] if col in df.columns]

            processed.append((file.stem, df[keep_cols]))

        return processed

    # Load and prepare data
    named_dfs = load_and_filter_csvs(directory)

    # Run FDID models
    results = {}

    for filename, df in named_dfs:
        outcome_cols = [col for col in df.columns if col.startswith("ntl")]

        for outcome_col in outcome_cols:
            config = {
                "df": df,
                "outcome": outcome_col,
                "treat": "treated",
                "unitid": "fullname",
                "time": "date",
                "display_graphs": False,
                "save": False,
                "counterfactual_color": ["red", "blue"],
            }

            key = f"{filename}_{outcome_col}"
            results[key] = FDID(config).fit()

    return results

results = run_fdid_batch(Path.cwd())

def dump_results_to_text(results: dict, output_file: str = "fdid_did_outputs.txt") -> None:
    """
    Dump FDID and DID result summaries from a results dictionary to a text file.

    Parameters:
        results (dict): The dictionary of fitted FDID models.
        output_file (str): The name of the output text file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        for key, models in results.items():
            f.write(f"\n===== Results for {key} =====\n")

            # FDID
            f.write("\n--- FDID ---\n")
            fdid_model = models[0]
            for section in ["Effects", "Fit", "Inference", "Weights"]:
                if section in fdid_model.raw_results:
                    f.write(f"\n[{section}]\n")
                    f.write(f"{fdid_model.raw_results[section]}\n")

            # DID
            f.write("\n--- DID ---\n")
            did_model = models[1]
            for section in ["Effects", "Fit", "Inference"]:  # no Weights
                if section in did_model.raw_results:
                    f.write(f"\n[{section}]\n")
                    f.write(f"{did_model.raw_results[section]}\n")

            f.write("\n" + "="*50 + "\n")


dump_results_to_text(results, "fdid_summary_output.txt")
