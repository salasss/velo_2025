import pytest
import sys
from pathlib import Path

# On ajoute la racine du projet au chemin Python
sys.path.insert(0, str(Path(__file__).parent.parent))

# CORRECTION IMPORT : On importe depuis le model à la racine
# (Python interdit les imports commençant par un chiffre comme '1_basic...')
from model import State, run_simulation

class TestModel:
    """Test cases for the bike simulation model"""
    
    def test_state_initialization(self):
        """Test State class initialization"""
        state = State(mailly=10, moulin=5)
        assert state.mailly == 10
        assert state.moulin == 5
    
    def test_run_simulation_returns_dict(self):
        """Test that run_simulation returns the correct structure"""
        # On utilise les arguments nommés pour être clair
        df, metrics = run_simulation(
            initial=State(10, 5),
            steps=10,
            p1=0.5,
            p2=0.3,
            seed=42
        )
        
        # run_simulation renvoie (DataFrame, Dict)
        # On vérifie le DataFrame
        assert 'mailly' in df.columns
        assert 'moulin' in df.columns
        # On vérifie les métriques
        assert isinstance(metrics, dict)
        assert 'final_imbalance' in metrics
    
    def test_run_simulation_steps(self):
        """Test that simulation runs for correct number of steps"""
        steps = 20
        df, metrics = run_simulation(
            initial=State(10, 5),
            steps=steps,
            p1=0.5,
            p2=0.3,
            seed=42
        )
        
        assert len(df) == steps

    def test_reproducibility(self):
        """Test that same seed produces same results"""
        init = State(10, 5)
        # Run 1
        df1, _ = run_simulation(init, 15, 0.5, 0.3, seed=42)
        # Run 2
        df2, _ = run_simulation(init, 15, 0.5, 0.3, seed=42)
        
        # Les listes doivent être strictement identiques
        assert df1['mailly'].equals(df2['mailly'])