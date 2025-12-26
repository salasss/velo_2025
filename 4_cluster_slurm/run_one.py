import argparse
import json
from pathlib import Path
import pandas as pd

from model import State, run_simulation


def parse_args():
    """Parse command line arguments for running one simulation from parameter file.
    
    Returns:
        Parsed arguments containing:
        - params: Path to CSV file with parameter combinations (default: params.csv)
        - row_index: Index of the row to execute from the parameters file
        - out_dir: Output directory for this simulation's results
        - base_seed: Base seed to use if row doesn't have seed column (default: 0)
    
    Note:
        Use argparse.ArgumentParser to define all required and optional arguments
    """
    my_args = argparse.ArgumentParser(description="Parse command line arguments for running one simulation from parameter file")
    my_args.add_argument('--params',type=str,required=True, help='Path to CSV file with parameter combinations (default: params.csv)')
    my_args.add_argument('--row-index',type=int, required=True, help=' Index of the row to execute from the parameters file')
    my_args.add_argument('--out-dir',type=str,default='results', help=' Output directory for results')
    my_args.add_argument('--base-seed',type=int,default=0,help='Base seed to use if row doesn\'t have seed column (default: 0)')
    return my_args.parse_args()

def main():
    """Main function to run a single simulation specified by row index.
    
    This function should:
    1. Parse command line arguments
    2. Read the parameters CSV file
    3. Extract the specified row by index
    4. Handle seed generation (use row seed or base_seed + row_index)
    5. Run the simulation with extracted parameters
    6. Save results to individual output directory
    7. Save metadata about the run
    
    Expected parameter CSV columns:
    - init_mailly: Initial bikes at Mailly
    - init_moulin: Initial bikes at Moulin
    - steps: Number of simulation steps
    - p1: Probability Mailly->Moulin
    - p2: Probability Moulin->Mailly
    - seed: Random seed (optional)
    
    Output structure:
    - {out_dir}/{row_index}/timeseries.csv: Simulation timeseries
    - {out_dir}/{row_index}/metrics.csv: Simulation metrics
    - {out_dir}/{row_index}/metadata.json: Run parameters and metadata
    
    Note:
        - Create subdirectory named after row_index
        - Handle missing seed column gracefully
        - Save metadata as JSON with all parameters including final seed used
    """
    args = parse_args()
    try:
        csv_all = pd.read_csv(args.params)
        row = csv_all.iloc[args.row_index]
    except IndexError:
        print(f"Erreur")
        return
    
    if 'seed' in row: seed = int(row['seed'])
    else: seed = args.base_seed + args.row_index
    
    initial_state = State(
        mailly=int(row['init_mailly']),
        moulin=int(row['init_moulin'])
    )
    df_results, metrics = run_simulation(initial=initial_state,steps=int(row['steps']),p1=row['p1'],p2=row['p2'],seed=seed)
    csv_path = Path(args.out_dir) / str(args.row_index)
    csv_path.mkdir(parents=True, exist_ok=True)
    df_results.to_csv(csv_path / "timeseries.csv", index=False)
    
    pd.DataFrame([metrics]).to_csv(csv_path / "metrics.csv", index=False)
    
    metadata = row.to_dict()
    metadata['used_seed'] = seed
    
    with open(csv_path / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    print(f"test--runoneSlurm--Done! {len(df_results)} simulations run.")
        
    
    
    


if __name__ == "__main__":
    main()
