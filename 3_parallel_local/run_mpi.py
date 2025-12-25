import argparse
from pathlib import Path
from mpi4py import MPI
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from model import State, run_simulation


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


def main():
    """Main function to run parallel parameter sweep using MPI.

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
        - Use the mpi4py module for parallel processing
    """
    #init 
    comm= MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    chunks = None
    args = parse_args()
    
    if rank==0:
        df_params = pd.read_csv(args.params)
        output_dir = Path(args.out_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        df_params['run_id'] = df_params.index
        
        all_tasks = df_params.to_dict('records')
        #div tasks in n=size
        chunks = np.array_split(all_tasks,size)
    
    #distribution/scatter
    my_tasks = comm.scatter(chunks,root=0)
    my_results = []
    
    for row in my_tasks:
        res = run_simulation(int(row['init_mailly']),int(row['init_moulin']), int(row['steps']), row['p1'], row['p2'], int(row['seed']))
        summary = {
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
        my_results.append(summary)
        
    #geting the results/gather
    all_res= comm.gather(my_results,root=0)
    
    if rank==0:
        final_data = []
        for worker_list in all_res:
            final_data.extend(worker_list)
        df_results = pd.DataFrame(final_data)
        df_results = df_results.sort_values('run_id')
        csv_path = output_dir / "metrics.csv"
        df_results.to_csv(csv_path, index=False)
        print(f"test-paralle_mpi4py--Done! {len(df_results)} simulations run.")
    
        
    
    


if __name__ == "__main__":
    main()
