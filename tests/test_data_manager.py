import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from app.data_manager import load_data, calculate_scores

class DataManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.df = load_data()

    def test_load_data(self):
        self.assertNotEqual(self.df.shape[0], 0, 'No data was loaded')
        expected_columns = {'name', 'alt_name', 'lat', 'long', 'country', 'admin1', 'population'}
        self.assertTrue(expected_columns.issubset(self.df.columns), 'Dataframe does not contain all required columns')

    def test_calculate_scores_without_location(self):
        results_df = calculate_scores(self.df, 'London')
        self.assertNotEqual(results_df.shape[0], 0, 'No scores were calculated')
        self.assertIn('score', results_df.columns, "Results dataframe does not have a 'score' column")

    def test_calculate_scores_with_location(self):
        results_df = calculate_scores(self.df, 'London', latitude=43.70011, longitude=-79.4163)
        self.assertNotEqual(results_df.shape[0], 0, 'No scores were calculated with location')
        self.assertTrue(all(results_df.iloc[i]['score'] >= results_df.iloc[i + 1]['score'] for i in range(len(results_df) - 1)),
                        'Results are not sorted by score in descending order')

if __name__ == '__main__':
    unittest.main()