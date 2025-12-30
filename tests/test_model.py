import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 1_basic_single_sim.model import State, run_simulation


class TestModel:
    """Test cases for the bike simulation model"""
    
    def test_state_initialization(self):
        """Test State class initialization"""
        state = State(mailly=10, moulin=5)
        assert state.mailly == 10
        assert state.moulin == 5
    
    def test_run_simulation_returns_dict(self):
        """Test that run_simulation returns a dictionary"""
        result = run_simulation(
            init_mailly=10,
            init_moulin=5,
            steps=10,
            p1=0.5,
            p2=0.3,
            seed=42
        )
        
        assert isinstance(result, dict)
        assert 'mailly' in result
        assert 'moulin' in result
    
    def test_run_simulation_steps(self):
        """Test that simulation runs for correct number of steps"""
        steps = 20
        result = run_simulation(
            init_mailly=10,
            init_moulin=5,
            steps=steps,
            p1=0.5,
            p2=0.3,
            seed=42
        )
        
        assert len(result['mailly']) == steps
        assert len(result['moulin']) == steps
    
    def test_run_simulation_with_seed_reproducible(self):
        """Test that same seed produces same results"""
        result1 = run_simulation(10, 5, 15, 0.5, 0.3, 42)
        result2 = run_simulation(10, 5, 15, 0.5, 0.3, 42)
        
        assert result1['mailly'] == result2['mailly']
        assert result1['moulin'] == result2['moulin']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
