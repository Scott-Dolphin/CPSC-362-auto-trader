import unittest
from app import app, plot

#UNIT TEST
class TestPlotFunction(unittest.TestCase):


    def setUp(self):
        self.app = app
        self.client = app.test_client()
        self.client.testing = True

    def test_plot(self):
        with self.app.app_context():
        # Sample input data for the plot function
            history_dict = {
                '2021-01-04': {'Open': 100.0, 'Close': 102.0, 'High': 105.0, 'Low': 95.0},
                '2021-01-05': {'Open': 102.0, 'Close': 104.0, 'High': 106.0, 'Low': 98.0}
            }
            symbol = 'TEST'
            
            # Call the plot function
            response = plot(history_dict, symbol)
            
            # Check if the response is a JSON object containing the 'image' key
            self.assertIn('image', response.json)
            print("Unit test for plot function passed")

#INTEGRATION TESTS
class TestFNGUFunctions(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_get_FNGU_data(self):
        response = self.client.get('/api/stock/FNGU')
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn('2021-01-04', response_data)   
        self.assertIn('2024-10-10', response_data)   
        print('FNGU Tests Passed')
    
        
class TestFNGDFunctions(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_get_FNGD_data(self):
        response = self.client.get('/api/stock/FNGD')
        self.assertEqual(response.status_code, 200)   
        response_data = response.get_json()
        self.assertIn('2021-01-04', response_data)   
        self.assertIn('2024-10-10', response_data)   
        print("FNGD Tests Passed")
    

if __name__ == '__main__':
    unittest.main()