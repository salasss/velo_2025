# 2_serial_param_sweep

Goal: run many parameter sets serially and save tidy outputs.

Run:

```bash
python run_serial.py --params params.csv --out-dir results/
```

Outputs:
- results/metrics.csv: one row per run
- results/metrics_3plot.png: Plot of mailly, moulin and balance for each simulation
