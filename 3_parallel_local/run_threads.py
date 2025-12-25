import argparse
from pathlib import Path
import threading
import pandas as pd
import matplotlib.pyplot as plt

from model import State, run_simulation

import queue


def parse_args():
    """Parse command line arguments for parallel parameter sweep.

    Returns:
        Parsed arguments containing:
        - params: Path to CSV file with parameter combinations
        - out_dir: Output directory for results
        - workers: Number of worker processes ('auto' for automatic detection)
        - plot: Boolean flag to generate plots after run

    Note:
        Use argparse.ArgumentParser to define all required and optional arguments
    """
    my_args = argparse.ArgumentParser(description="parallel parameter sweep usings threads")
    my_args.add_argument('--params',type=str,required=True, help='Path to CSV file')
    my_args.add_argument('--out-dir',type=str,default='results', help=' Output directory for results')
    my_args.add_argument('--workers',type=str,default='4', help=' Number of worker processes (auto: for automatic detection)')
    my_args.add_argument('--plot',action='store_true',help='Boolean flag to generate plot')
    return my_args.parse_args()
    
lock = threading.Lock()
def thread_work(task_queue, results_list):
    """this func execute the simulation in a thread"""
    while True:
        row = task_queue.get()
        if row is None:
            task_queue.task_done()
            break
        try:
            res = run_simulation(int(row['init_mailly']),int(row['init_moulin']), int(row['steps']), row['p1'], row['p2'], int(row['seed']))
            row_result={
                'run_id': row.get('run_id', 0),
                #init
                'init_mailly':row['init_mailly'],
                'init_moulin':row['init_moulin'],
                'steps':row['steps'],
                'p1':row['p1'],
                'p2':row['p2'],
                'seed': row['seed'],
                #final result
                'final_mailly':res["mailly"][-1],
                'final_moulin':res["moulin"][-1],
                'unmet_mailly':res["unmet_mailly"][-1],
                'unmet_moulin':res["unmet_moulin"][-1],
                'ambulance':res["final_imbalance"][-1] 
            }
            with lock:
                results_list.append(row_result)
        except Exception as e:
            print("error")
        task_queue.task_done()
        

def main():
    """Main function to run parallel parameter sweep using threading.

    This function should:
    1. Parse command line arguments
    2. Read parameter combinations from CSV file
    3. Set up parallel processing with appropriate number of workers
    4. Submit simulation jobs to worker processes
    5. Collect results as they complete
    6. Aggregate and save results
    7. Optionally generate plots

    Expected parameter CSV columns:
    - steps: Number of simulation steps
    - p1: Probability Mailly->Moulin
    - p2: Probability Moulin->Mailly
    - init_mailly: Initial bikes at Mailly
    - init_moulin: Initial bikes at Moulin
    - seed: Random seed

    Output files:
    - metrics.csv: Aggregated metrics for all runs
    - Optional plots: PNG files for timeseries and metrics visualization

    Note:
        - Use the threading module for parallel processing
    """
    args = parse_args()
    df_params = pd.read_csv(args.params)
    output_dir = Path(args.out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if args.workers == 'auto':
        n_workers = 4 # Valeur par défaut raisonnable pour des threads
    else:
        n_workers = int(args.workers)
        
    df_params['run_id'] = df_params.index
    task_queue = queue.Queue() 
    results = []          
    threads = []
    for _ in range(n_workers):
        t = threading.Thread(target=thread_work, args=(task_queue, results))
        t.start()
        threads.append(t)
    for _, row in df_params.iterrows():
        task_queue.put(row)

    for _ in range(n_workers):
        task_queue.put(None)

    task_queue.join() 
    for t in threads:
        t.join()

    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values('run_id')
    csv_path = output_dir / "metrics.csv"
    df_results.to_csv(csv_path, index=False)
    print(f"test--threads--Done! {len(df_results)} simulations run.")
    


if __name__ == "__main__":
    main()
