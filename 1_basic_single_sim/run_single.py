import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
from model import State, run_simulation
import pandas as pd


def parse_args():
    """Parse command line arguments for single simulation run.
    
    Returns:
        Parsed arguments containing:
        - steps: Number of simulation steps
        - p1: Probability of movement from Mailly to Moulin
        - p2: Probability of movement from Moulin to Mailly
        - init_mailly: Initial bikes at Mailly station
        - init_moulin: Initial bikes at Moulin station
        - seed: Random seed (default: 0)
        - out_csv: Output CSV file path
        - plot: Boolean flag to generate plots
    
    Note:
        Use argparse.ArgumentParser to define all required and optional arguments
    """
    my_parser = argparse.ArgumentParser(description="basic single simulation run")
    my_parser.add_argument('--steps',type=int,required=True,help='Number of simulation steps')
    my_parser.add_argument('--p1',type=float,required=True,help='Probability of movement from Mailly to Moulin')
    my_parser.add_argument('--p2',type=float,required=True,help='Probability of movement from Moulin to Mailly')
    my_parser.add_argument('--init-mailly',type=int,required=True,help='Initial bikes at Mailly station')
    my_parser.add_argument('--init-moulin',type=int,required=True,help='Initial bikes at Moulin station')
    my_parser.add_argument('--seed',type=int,default=0,help='Random seed (default: 0)')
    my_parser.add_argument('--out-csv',type=str,default='results.csv',help='Output CSV file path')
    my_parser.add_argument('--plot',action='store_true',help='Boolean flag to generate plot')
    # i used action='store_true' because a had issues with type bool
    return my_parser.parse_args()


def main():
    """Main function to run a single bike-sharing simulation.
    
    This function should:
    1. Parse command line arguments
    2. Run the simulation with specified parameters
    3. Save results to CSV files (timeseries and metrics)
    4. Optionally generate and save plots
    
    Output files:
    - Timeseries data: CSV with time, mailly, moulin columns
    - Metrics data: CSV with key-value pairs of simulation metrics
    - Optional plot: PNG showing bike counts over time for both stations
    
    Note:
        Create output directories if they don't exist
        Save metrics as tab-separated key-value pairs
    """
    my_args = parse_args()
    output_path = Path(my_args.out_csv)
    #if we a parent in the arg outcsv we will create it
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    results, metrics =run_simulation(initial_mailly=my_args.init_mailly,initial_moulin=my_args.init_moulin,steps=my_args.steps,p1=my_args.p1,p2=my_args.p2,seed=my_args.seed)
    results.to_csv(path_or_buf=output_path,index=False)
    print(f"resuklts csv saved")
    
    
    metrics_path = output_path.with_name(output_path.stem + "_metrics.csv")
    # i reimported here pandas to reuse .to_csv
    pd.Series(metrics).to_csv(path_or_buf=metrics_path,sep='\t',header=False)
    print(f"metrics csv saved")
    
    
    if my_args.plot:
        plt.figure(figsize=(10, 10))
        plt.plot(results['time'], results['mailly'], label='Mailly')
        plt.plot(results['time'], results['moulin'], label='Moulin')
        plt.xlabel('Time Step')
        plt.ylabel('Number of Bikes')
        plt.title('Bike Sharing Simulation')
        plt.legend()
        plt.grid(True)
        
        plot_path = output_path.with_name(output_path.stem + "_plot.png")
        plt.savefig(plot_path)
        print(f"Plot saved")
if __name__ == "__main__":
    main()
