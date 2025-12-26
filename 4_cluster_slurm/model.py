from dataclasses import dataclass
from typing import Tuple, Dict
import numpy as np
import pandas as pd


@dataclass
class State:
    """Represents the state of bikes at two stations.

    Attributes:
        mailly: Number of bikes at Mailly station
        moulin: Number of bikes at Moulin station
    """

    mailly: int
    moulin: int


def step(
    state: State,
    p1: float,
    p2: float,
    rng: np.random.Generator,
    metrics: Dict[str, int],
) -> State:
    """Simulate one time step of the bike-sharing system.

    Args:
        state: Current state of the system (bike counts at each station)
        p1: Probability of a user wanting to go from Mailly to Moulin
        p2: Probability of a user wanting to go from Moulin to Mailly
        rng: Random number generator for stochastic events
        metrics: Dictionary to track simulation metrics (unmet demand, etc.)

    Returns:
        Updated state after one simulation step

    Note:
        - If a station has no bikes available, increment the appropriate unmet demand counter
        - Update the state by moving bikes between stations based on probabilities
    """
    # User tries to go from mailly -> moulin with prob p1
    #mailly -> moulin
    #we will note remove metrics to not touch to the def 
    randomp1 = rng.random()
    if randomp1<p1:
        if(state.mailly):
            state.mailly-=1
            state.moulin+=1
        else:
            # state.unmet_mailly+=1
            metrics['unmet_mailly']+=1
    #mailly <- moulin
    randomp2 = rng.random()
    if randomp2<p2:
        if(state.moulin):
            state.moulin-=1
            state.mailly+=1
        else:
            # state.unmet_moulin+=1
            metrics['unmet_moulin']+=1
    return state


def run_simulation(initial: State, steps: int, p1: float, p2: float, seed: int):
    """Run a complete bike-sharing simulation with extended metrics.

    Args:
        initial: Initial state of the system
        steps: Number of simulation steps to run
        p1: Probability of movement from Mailly to Moulin
        p2: Probability of movement from Moulin to Mailly
        seed: Random seed for reproducibility

    Returns:
        Tuple containing:
        - DataFrame with columns ['time', 'mailly', 'moulin'] tracking bike counts over time
        - Dictionary with metrics including:
            - 'unmet_mailly': Number of unmet requests at Mailly
            - 'unmet_moulin': Number of unmet requests at Moulin
            - 'final_imbalance': Final difference between station bike counts

    Note:
        - Initialize metrics dictionary with all required counters
        - Record state at each time step for the DataFrame
        - Calculate final imbalance as mailly - moulin
    """
    state = State(mailly=initial.mailly,moulin=initial.moulin)
    rng = np.random.default_rng(seed)
    metrics = {'unmet_mailly':0,'unmet_moulin':0}
    # mailly = []
    # moulin = []
    # unmet_mailly = []
    # unmet_moulin = []
    # final_imbalance = []
    history =[]
    for i in range(steps):
        history.append({
            'time': i,
            'mailly': state.mailly,
            'moulin': state.moulin
        })
        # unmet_mailly.append(state.unmet_mailly)
        # unmet_moulin.append(state.unmet_moulin)
        # final_imbalance.append(state.mailly - state.moulin)
        step(state,p1,p2,rng,metrics)
    metrics['final_imbalance'] = state.mailly - state.moulin
    df_history = pd.DataFrame(history)
    return df_history, metrics
