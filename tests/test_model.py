import unittest
import subprocess
import sys
import os

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        """Préparation : On repère où sont les fichiers"""
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.params_file = os.path.join(self.root_dir, 'params.csv')
        
        #if not csv exist
        if not os.path.exists(self.params_file):
            with open(self.params_file, 'w') as f:
                f.write("init_mailly,init_moulin,steps,p1,p2,seed\n")
                f.write("10,5,5,0.5,0.5,42\n")
                f.write("10,5,5,0.5,0.5,43\n")

    def run_script(self, script_path, args=[]):
        """Helper pour lancer un script python et vérifier qu'il finit avec le code 0"""
        full_path = os.path.join(self.root_dir, script_path)
        
        #  python chemin/vers/script.py arg1 arg2 ...
        cmd = [sys.executable, full_path] + args
        
        # start processus
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=self.root_dir 
        )
        
        # check
        if result.returncode != 0:
            print(f"\n--- ERREUR lors de l'exécution de {script_path} ---")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
        
        self.assertEqual(result.returncode, 0, f"Le script {script_path} a planté !")

    def test_1_run_basic(self):
        """Vérifie que le script 1_basic tourne"""
        self.run_script('1_basic_single_sim/run_single.py')

    def test_2_run_serial(self):
        """Vérifie que le script 2_serial tourne"""
        self.run_script('2_serial_param_sweep/run_serial.py', [
            '--params', 'params.csv',
            '--out-dir', 'test_results_2',
            '--plot' # test plot
        ])

    def test_3_run_parallel(self):
        """Vérifie que le script 3_parallel tourne (Mode Multiprocessing)"""
        # note :  test just run_parallel.py 
        if os.path.exists(os.path.join(self.root_dir, '3_parallel_local/run_parallel.py')):
             self.run_script('3_parallel_local/run_parallel.py', [
                '--params', 'params.csv',
                '--out-dir', 'test_results_3'
            ])

if __name__ == '__main__':
    unittest.main()