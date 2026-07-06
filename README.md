# FatigueRainflowPostProcessor

Python utility that reads rainflow-binned stress/cycle files, computes fatigue damage, and writes per-file totals and estimated lifespan to a CSV report.

## What it does

For each input file, the tool:

1. Loads two-column numeric data (`stress`, `cycles`).
2. Computes cycles-to-failure `N` using a piecewise S–N relationship:
   - If `stress < 92.682982338837`: `N = 10^15.835 / stress^5`
   - Otherwise: `N = 10^11.901 / stress^3`
3. Computes row fatigue as `cycles / N`.
4. Sums row fatigue to `Total_Fatigue`.
5. Computes `Lifespan_Years = design_life / Total_Fatigue` (design life is 20 years in `Main.py`).

Results are written to `Output/fatigue_results.csv`.

## Repository files

- `Main.py` — main entry point; processes all files in the input folder and writes CSV output.
- `ReadHistogram.py` — fatigue calculations and file-loading helpers.
- `FatiguePostProcessor.bat` — Windows launcher (`python Main.py`).

## Requirements

- Python 3.x
- `numpy`

Install dependency:

```bash
pip install numpy
```

## Usage

1. Create an `Input` folder in the project root (capital `I`, as used by the current code).
2. Put one or more fatigue data files in `Input/` (plain numeric two-column files readable by `numpy.loadtxt`).
3. Run:

```bash
python Main.py
```

Or on Windows:

```bat
FatiguePostProcessor.bat
```

4. Check generated results in:

`Output/fatigue_results.csv`

## Output format

The CSV contains:

- `Input_File`
- `Total_Fatigue`
- `Lifespan_Years`

If a file fails to process, an error message is written in the corresponding output row.
