import unittest
import os
import sys
import pandas as pd

# Thêm path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.csv_reader import read_csv


class TestCSVReader(unittest.TestCase):

    def test_read_csv_valid(self):
        file = "test_valid.csv"
        df = pd.DataFrame({
            "pid": ["P1", "P2"],
            "arrival_time": [0, 1],
            "burst_time": [5, 3],
            "priority": [1, 2]
        })
        df.to_csv(file, index=False)

        processes = read_csv(file)

        self.assertEqual(len(processes), 2)

        os.remove(file)


    def test_read_csv_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_csv("khong_ton_tai.csv")


    def test_read_csv_missing_column(self):
        file = "test_missing_col.csv"
        df = pd.DataFrame({
            "pid": ["P1"],
            "arrival_time": [0],
        })
        df.to_csv(file, index=False)

        with self.assertRaises((ValueError, KeyError)):
            read_csv(file)

        os.remove(file)


    def test_read_csv_missing_value(self):
        file = "test_missing_val.csv"
        df = pd.DataFrame({
            "pid": ["P1"],
            "arrival_time": [None],
            "burst_time": [5]
        })
        df.to_csv(file, index=False)

        with self.assertRaises((ValueError, TypeError)):
            read_csv(file)

        os.remove(file)


    def test_read_csv_no_priority(self):
        file = "test_no_priority.csv"
        df = pd.DataFrame({
            "pid": ["P1"],
            "arrival_time": [0],
            "burst_time": [5],
            "priority": [None]
        })
        df.to_csv(file, index=False)

        processes = read_csv(file)

        self.assertEqual(processes[0].priority, 0)

        os.remove(file)


if __name__ == '__main__':
    unittest.main(verbosity=2)
