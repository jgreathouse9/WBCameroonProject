# cameroon_fdid/cameroon_results_vectorized.py
import pandas as pd
from pathlib import Path
from mlsynth import FDID
import numpy as np
import matplotlib.pyplot as plt

# Base path of the script (this package)
BASE_DIR = Path(__file__).parent

# Output file
OUTPUT_FILE = BASE_DIR / "fdid_summary_output2.txt"

def dump_results_to_text(results: dict, output_file: Path = OUTPUT_FILE) -> None:
    with open(output_file, "w", encoding="utf-8") as f:
        for key, model in results.items():
            f.write(f"\n===== RESULTS FOR {key} =====\n")
            for method in ["FDID", "DID"]:
                if method not in model.results:
                    continue
                f.write(f"\n--- {method} ---\n")
                res = model.results[method]
                f.write("\n[Effects]\n")
                f.write(f"  ATT: {res.effects.att}\n")
                f.write(f"  Percent ATT: {res.effects.att_percent}\n")
                if res.effects.additional_effects:
                    for k, v in res.effects.additional_effects.items():
                        f.write(f"  {k}: {v}\n")
                f.write("\n[Inference]\n")
                f.write(f"  p-value: {res.inference.p_value}\n")
                f.write(f"  95% CI: ({res.inference.ci_lower}, {res.inference.ci_upper})\n")
                f.write(f"  Std. Error: {res.inference.standard_error}\n")
                for k, v in res.inference.details.items():
                    f.write(f"  {k}: {v}\n")
                f.write("\n[Fit Diagnostics]\n")
                f.write(f"  R² pre-treatment: {res.fit_diagnostics.r_squared_pre}\n")
                f.write(f"  RMSE pre-treatment: {res.fit_diagnostics.rmse_pre}\n")
                if method == "FDID":
                    f.write("\n[Weights]\n")
                    if res.weights and res.weights.donor_weights:
                        for donor, w in res.weights.donor_weights.items():
                            f.write(f"  {donor}: {w:.4f}\n")
                    else:
                        f.write("  (No weights)\n")
                    R2_path = res.raw_results.get("R2_at_each_step")
                    if R2_path is not None:
                        f.write("\n[R2 at Each Step]\n")
                        f.write("  " + ", ".join(f"{x:.4f}" for x in R2_path) + "\n")
            f.write("\n" + "="*60 + "\n")

def run_fdid_batch(directory: Path = BASE_DIR) -> dict:
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
            keep_cols = ["date"] + [col for col in df.columns if col.startswith("ntl")] + \
                        [col for col in ["treated", "fullname"] if col in df.columns]
            processed.append((file.stem, df[keep_cols]))
        return processed

    named_dfs = load_and_filter_csvs(directory)
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
                "verbose": False
            }
            key = f"{filename}_{outcome_col}"
            results[key] = FDID(config).fit()
    return results

if __name__ == "__main__":
    results = run_fdid_batch()
    dump_results_to_text(results)
    print(f"FDID results written to {OUTPUT_FILE}")
