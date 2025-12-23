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
    for i,row in df_params.iterrows():
        
        res = run_simulation(int(row['init_mailly']),int(row['init_moulin']), int(row['steps']), row['p1'], row['p2'], int(row['seed']))
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
        


if __name__ == "__main__":
    main()
