"""
Test the sim module
"""
import unittest

from pysim import sim

class SimTest(unittest.TestCase):
    """
    Test the sim module
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch(pysim.get_program_from_file)
    def test_sim_run(self, mock_get_program_from_file):
        mock_get_program_from_file.return_value = 'add $0, #1'
        sim.run(program=program)
