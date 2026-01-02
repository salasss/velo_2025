import argparse
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt


def parse_args():
    """Parse command line arguments for collecting distributed results.
    
    Returns:
        Parsed arguments containing:
        - in_dir: Input directory containing subdirectories with individual run results
        - out_dir: Output directory for aggregated results
        - plot: Boolean flag to generate plots after collection
    
    Note:
        Use argparse.ArgumentParser to define all required and optional arguments
    """
    my_parser = argparse.ArgumentParser(description="Collect and aggregate results")
    my_parser.add_argument('--in-dir', type=str, required=True, help='Input directory with subdirectories')
    my_parser.add_argument('--out-dir', type=str, required=True, help='Output directory')
    my_parser.add_argument('--plot', action='store_true', help='Generate plots')
    return my_parser.parse_args()

def main():
    """Main function to collect and aggregate results from distributed simulations.
    
    This function should:
    1. Parse command line arguments
    2. Scan input directory for numbered subdirectories (one per simulation run)
    3. Read individual results from each subdirectory
    4. Aggregate metrics and timeseries data
    5. Save aggregated results to CSV files
    6. Optionally generate plots
    
    Expected input structure:
    - {in_dir}/0/metrics.csv, timeseries.csv, metadata.json
    - {in_dir}/1/metrics.csv, timeseries.csv, metadata.json
    - ...
    
    Output files:
    - metrics.csv: Aggregated metrics for all runs with run_id column
    - timeseries.csv: Tidy format timeseries data for all runs
    - Optional plots: PNG files for timeseries and metrics visualization
    
    Note:
        - Extract run_id from subdirectory name (should be integer)
        - Merge metadata parameters into metrics with 'param_' prefix
        - Convert timeseries to tidy format (melt operation)
        - Handle missing files gracefully
        - Sort subdirectories numerically for consistent processing
    """
    args = parse_args()
    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    all_metrics = []
    all_timeseries = []
    run_dirs = sorted([d for d in in_dir.iterdir()
                       if d.is_dir() and d.name.isdigit()],key=lambda x: int(x.name))

    if not run_dirs:
        print("error")
        return
    for run_dir in run_dirs:
        try:
            run_id = int(run_dir.name)
            
            with open(run_dir / "metadata.json", 'r') as f:
                meta = json.load(f)

            # Metrics
            if (run_dir / "metrics.csv").exists():
                metrics_df = pd.read_csv(run_dir / "metrics.csv")
                metrics_df['run_id'] = run_id
                
                for key, val in meta.items():
                    metrics_df[f'param_{key}'] = val
                
                all_metrics.append(metrics_df)

            # Timeseries
            if (run_dir / "timeseries.csv").exists():
                ts_df = pd.read_csv(run_dir / "timeseries.csv")
                ts_df['run_id'] = run_id
                all_timeseries.append(ts_df)

        except Exception as e:
            print("error")

    if all_metrics:
        final_metrics = pd.concat(all_metrics, ignore_index=True)
        final_metrics = final_metrics.sort_values('run_id')
        
        csv_path = out_dir / "metrics.csv"
        final_metrics.to_csv(csv_path, index=False)


    
    if all_timeseries:
        full_ts = pd.concat(all_timeseries, ignore_index=True)
        
        # trasformation
        tidy_ts = full_ts.melt(
            id_vars=['time', 'run_id'], 
            value_vars=['mailly', 'moulin'],
            var_name='station', 
            value_name='bikes'
        )
        
        ts_path = out_dir / "timeseries.csv"
        tidy_ts.to_csv(ts_path, index=False)
    else:
        print("No data")


if __name__ == "__main__":
    main()
