from unittest import TestCase
from unittest.mock import patch
from LocationWeather import LocationWeather

class TestLocationWeather(TestCase):
    def setUp(self):
        # Initialize LocationWeather with sample data for all tests
        self.weather = LocationWeather(latitude=40.0, longitude=-105.0, month=7, day=23, year=2025)

    @patch('requests.get')
    def test_get_weather_data(self, mock_get):
        # Mock an API response for one year
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'daily': {
                'temperature_2m_mean': [70.0],
                'wind_speed_10m_max': [10.0],
                'precipitation_sum': [0.1]
            }
        }

        # Call the method
        result = self.weather.get_weather_data()

        # Check that a dictionary is returned with expected keys and data
        self.assertIsInstance(result, dict)
        self.assertIn('years', result)
        self.assertIn('temps', result)
        self.assertIn('wind_speeds', result)
        self.assertIn('precips', result)
        self.assertEqual(len(result['temps']), 5)  # Expect 5 years of data
        self.assertEqual(result['temps'][0], 70.0)  # Check first temp value

    @patch('requests.get')
    def test_stats_fy_temps(self, mock_get):
        # Mock API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'daily': {
                'temperature_2m_mean': [70.0],
                'wind_speed_10m_max': [10.0],
                'precipitation_sum': [0.1]
            }
        }

        # Call the method
        avg, min_temp, max_temp = self.weather.stats_fy_temps()

        # Check stats (all data will be same)
        self.assertEqual(avg, 70.0)
        self.assertEqual(min_temp, 70.0)
        self.assertEqual(max_temp, 70.0)
        self.assertEqual(self.weather.avg_temp, 70.0)

    @patch('requests.get')
    def test_stats_fy_wind_speed(self, mock_get):
        # Mock API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'daily': {
                'temperature_2m_mean': [70.0],
                'wind_speed_10m_max': [10.0],
                'precipitation_sum': [0.1]
            }
        }

        # Call the method
        avg, min_ws, max_ws = self.weather.stats_fy_wind_speed()

        # Check stats
        self.assertEqual(avg, 10.0)  # Average of five 10.0 values
        self.assertEqual(min_ws, 10.0)
        self.assertEqual(max_ws, 10.0)
        self.assertEqual(self.weather.avg_wind_speed, 10.0)  # Check instance variable

    @patch('requests.get')
    def test_stats_fy_precip(self, mock_get):
        # Mock API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'daily': {
                'temperature_2m_mean': [70.0],
                'wind_speed_10m_max': [10.0],
                'precipitation_sum': [0.1]
            }
        }

        # Call the method
        sum_precip, min_precip, max_precip = self.weather.stats_fy_precip()

        # Check stats
        self.assertEqual(sum_precip, 0.5)  # Sum of five 0.1 values
        self.assertEqual(min_precip, 0.1)
        self.assertEqual(max_precip, 0.1)
        self.assertEqual(self.weather.sum_precipitation, 0.5)  # Check instance variable
