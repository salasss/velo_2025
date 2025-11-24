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
        unmet_mailly: Number of unmet requests at Mailly
        unmet_moulin: Number of unmet requests at Moulin
    """

    mailly: int
    moulin: int
    unmet_mailly: int = 0
    unmet_moulin: int = 0


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
    # TODO: Implement the step logic
    pass


def run_simulation(
    initial_mailly: int,
    initial_moulin: int,
    steps: int,
    p1: float,
    p2: float,
    seed: int,
) -> Dict[str, list]:
    """Run a complete bike-sharing simulation.

    Args:
        initial_mailly: Initial number of bikes at Mailly station
        initial_moulin: Initial number of bikes at Moulin station
        steps: Number of simulation steps to run
        p1: Probability of movement from Mailly to Moulin
        p2: Probability of movement from Moulin to Mailly
        seed: Random seed for reproducibility

    Returns:
        - Dictionary indexed by step with metrics including:
            - 'mailly': Number of bikes at Mailly station
            - 'moulin': Number of bikes at Moulin station
            - 'unmet_mailly': Number of unmet requests at Mailly
            - 'unmet_moulin': Number of unmet requests at Moulin
            - 'final_imbalance': Final difference between station bike counts

    Note:
        - Create the state object with initial bike counts
        - Initialize metrics dictionary with appropriate counters
        - Record state at each time step for the DataFrame
        - Calculate final_imbalance for each step as mailly - moulin
    """
    # TODO: Implement the simulation loop
    pass
