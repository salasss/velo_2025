import argparse
from pathlib import Path
import multiprocessing as mp
import pandas as pd
import matplotlib.pyplot as plt

from model import State, run_simulation
import numpy as np


def plot_results(results_list, output_dir, smooth_window=1):
    """Simple plotting function for results"""
    if not results_list:
        return
    
    # Plot the first result as example
    res = results_list[0]
    
    # Smoothing function
    def smooth(data, window):
        if window <= 1:
            return data
        return np.convolve(data, np.ones(window)/window, mode='valid')
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(smooth(res['mailly'], smooth_window), label='Mailly', color='blue')
    plt.plot(smooth(res['moulin'], smooth_window), label='Moulin', color='green')
    plt.title('Bikes at Stations')
    plt.xlabel('Time')
    plt.ylabel('Number of Bikes')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(smooth(res['unmet_mailly'], smooth_window), label='Unmet Mailly', color='red')
    plt.plot(smooth(res['unmet_moulin'], smooth_window), label='Unmet Moulin', color='orange')
    plt.title('Unmet Demand')
    plt.xlabel('Time')
    plt.ylabel('Unmet Demand')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / "plot.png", dpi=100)
    plt.close()
    print(f"Plot saved to: {output_dir / 'plot.png'}")


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

def multi_work(row):
    """this func execute the simulation in a parallel"""
    res = run_simulation(int(row['init_mailly']),int(row['init_moulin']), int(row['steps']), row['p1'], row['p2'], int(row['seed']))
    return{
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
        
        


def main():
    """Main function to run parallel parameter sweep using multiprocessing.

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
        - Use multiprocessing for parallel processing
    """
    args = parse_args()
    df_params = pd.read_csv(args.params)
    output_dir = Path(args.out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df_params['run_id'] = df_params.index
    
    tasks = df_params.to_dict('records')
    if args.workers == 'auto':
        n_workers = mp.cpu_count()
    else:
        n_workers = int(args.workers)
        
    with mp.Pool(processes=n_workers) as pool:
        res = pool.map(multi_work,tasks)
    
    df_results = pd.DataFrame(res)
    df_results = df_results.sort_values('run_id')
    csv_path = output_dir / "metrics.csv"
    df_results.to_csv(csv_path, index=False)
    print(f"test-paralle--Done! {len(df_results)} simulations run.")
    
    if args.plot:
        # Collect raw results for plotting
        raw_results = []
        for task in tasks:
            res = run_simulation(int(task['init_mailly']), int(task['init_moulin']), 
                               int(task['steps']), task['p1'], task['p2'], int(task['seed']))
            raw_results.append(res)
        plot_results(raw_results, output_dir)
        


if __name__ == "__main__":
    main()
