# 3_parallel_local

Goal: accelerate the sweep using local CPU cores by using the three approaches.

- Threading
- Multiprocessing
- MPI

Run:

```bash
python run_threads.py --params params.csv --workers auto --out-dir thread/
python run_parallel.py --params params.csv --workers auto --out-dir multiprocessing/
python run_mpi.py --params params.csv --workers auto --out-dir mpi/
```

