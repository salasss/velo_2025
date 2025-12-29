import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from model import State, run_simulation


def parse_args():
    """Parse command line arguments for serial parameter sweep.

    Returns:
        Parsed arguments containing:
        - params: Path to CSV file with parameter combinations
        - out_dir: Output directory for results
        - plot: Boolean flag to generate plots after run
        - smooth_window: Window size for smoothing timeseries (default: 1, no smoothing)

    Note:
        Use argparse.ArgumentParser to define all required and optional arguments
    """
    my_parser = argparse.ArgumentParser(description="serial parameter sweep simulation run")
    my_parser.add_argument('--params',type=str,required=True,help='Path to CSV file with parameter combinations')
    my_parser.add_argument('--out-dir',type=str,default='results',help='Output directory for results')
    my_parser.add_argument('--plot',action='store_true',help='Boolean flag to generate plot')
    my_parser.add_argument('--smooth-window',type=int, default=1,help='Window size for smoothing timeseries (default: 1, no smoothing)')
    return my_parser.parse_args()


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
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: Bikes at stations
    axes[0].plot(smooth(res['mailly'], smooth_window), label='Mailly', color='blue')
    axes[0].plot(smooth(res['moulin'], smooth_window), label='Moulin', color='green')
    axes[0].set_title('Bikes at Stations')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Number of Bikes')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Unmet demand
    axes[1].plot(smooth(res['unmet_mailly'], smooth_window), label='Unmet Mailly', color='red')
    axes[1].plot(smooth(res['unmet_moulin'], smooth_window), label='Unmet Moulin', color='orange')
    axes[1].set_title('Unmet Demand')
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Unmet Demand')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / "plot.png", dpi=100)
    plt.close()
    print(f"Plot saved to: {output_dir / 'plot.png'}")


def main():
    """Main function to run serial parameter sweep.

    This function should:
    1. Parse command line arguments
    2. Read parameter combinations from CSV file
    3. Run simulations serially for each parameter combination
    4. Collect and aggregate results
    5. Save aggregated results to CSV files
    6. Optionally generate plots

    Expected parameter CSV columns:
    - init_mailly: Initial bikes at Mailly
    - init_moulin: Initial bikes at Moulin
    - steps: Number of simulation steps
    - p1: Probability Mailly->Moulin
    - p2: Probability Moulin->Mailly
    - seed: Random seed

    Output files:
    - metrics.csv: Aggregated metrics for all runs
    - Optional plots: PNG files for timeseries and metrics visualization

    Note:
        - Process each row in the parameters file as a separate simulation run
        - Add run_id to track individual simulations
        - **OPTIONAL**: plot timeseries for both stations
        - **OPTIONAL**: Handle smoothing for timeseries plots if requested
    """
    args = parse_args()
    df_params = pd.read_csv(args.params)
    output_dir = Path(args.out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data_summary =[]
    raw_results = []
    for i,row in df_params.iterrows():
        
        res = run_simulation(int(row['init_mailly']),int(row['init_moulin']), int(row['steps']), row['p1'], row['p2'], int(row['seed']))
        raw_results.append(res)
        row_result={
            'run': i,
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
        data_summary.append(row_result)
    df_results = pd.DataFrame(data_summary)
    output_csv = output_dir / "metrics.csv"
    df_results.to_csv(output_csv, index=False)
    print(f"test--Done! {len(df_results)} simulations run.")
    print(f"test--Results saved to: {output_csv}")
    if args.plot:
        plot_results(raw_results, output_dir,args.smooth_window)

        


if __name__ == "__main__":
    main()
