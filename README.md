# Weather API

## Overview
Weather API is a Python application that retrieves historical daily weather data for a specific date and location using the [Open-Meteo API](https://open-meteo.com/en/docs). It calculates five-year statistics for temperature (°F), wind speed (mph), and precipitation (inches) for a given latitude, longitude, and date. The data is stored in a SQLite database (`weather.db`) and can be queried as a pandas DataFrame for analysis.

This project is ideal for developers, researchers, or weather enthusiasts analyzing historical weather trends for a specific location and date.

## Project Structure
- `main.py`: Initializes the `LocationWeather` class, fetches weather data, stores it in a SQLite database, and queries results as a DataFrame.
- `LocationWeather.py`: Contains the `LocationWeather` class for fetching and processing weather data from Open-Meteo.
- `README.md`: Project documentation (this file).
- `requirements.txt`: Lists required Python dependencies with specific versions.
- `Test.py`: Unit tests for the `LocationWeather` class using `unittest` and `unittest.mock`.

## Prerequisites
- Python 3.13 or higher
- Internet connection to access the Open-Meteo API
- Dependencies (listed in `requirements.txt`):
  - `certifi==2025.7.9`
  - `charset-normalizer==3.4.2`
  - `greenlet==3.2.3`
  - `idna==3.10`
  - `numpy==2.3.1`
  - `pandas==2.3.0`
  - `python-dateutil==2.9.0.post0`
  - `pytz==2025.2`
  - `requests==2.32.4`
  - `six==1.17.0`
  - `SQLAlchemy==2.0.41`
  - `typing_extensions==4.14.1`
  - `tzdata==2025.2`
  - `urllib3==2.5.0`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/renquez/weather-api.git
   cd weather-api

Create a virtual environment (optional but recommended):
```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install dependencies:
```bash

pip install -r requirements.txt
```
## Usage
The API uses hardcoded inputs in `main.py` for latitude, longitude, month, day, and year to fetch 
weather data for a specific date over five years. The data is stored in a SQLite database 
(`weather.db`) and can be queried as a pandas DataFrame.

## Example
```
from main import Weather
from LocationWeather import LocationWeather

# Hardcoded inputs (e.g., Houston, TX on January 2, 2024)
latitude = 29.7633
longitude = -95.3633
month = 1
day = 2
year = 2024

# Initialize LocationWeather and fetch statistics
houston_weather = LocationWeather(latitude, longitude, month, day, year)
avg_temp, min_temp, max_temp = houston_weather.stats_fy_temps()
avg_wind, min_wind, max_wind = houston_weather.stats_fy_wind_speed()
sum_precip, min_precip, max_precip = houston_weather.stats_fy_precip()

# Store and query data
weather_table = Weather()
df = weather_table.query_weather()
print(df)
```
## Expected Output
The `query_weather` method returns a pandas DataFrame with the following columns:
- `id`: Unique record ID
- `location_latitude`, `location_longitude`: Location coordinates
- `month`, `day`, `year`: Date of the weather data
- `temp_5yr_avg`, `temp_min_5yr_avg`, `temp_max_5yr_avg`: Average, minimum, and maximum temperature (°F) over five years
- `wind_speed_5yr_avg`, `wind_speed_min_5yr_avg`, `wind_speed_max_5yr_avg`: Average, minimum, and maximum wind speed (mph) over five years
- `precipitation_5yr_sum`, `precipitation_min_5yr_avg`, `precipitation_max_5yr_avg`: Total, minimum, and maximum precipitation (inches) over five years

Example DataFrame:
```
   id  location_latitude  location_longitude  month  day  year  temp_5yr_avg  temp_min_5yr_avg  temp_max_5yr_avg  wind_speed_5yr_avg  wind_speed_min_5yr_avg  wind_speed_max_5yr_avg  precipitation_5yr_sum  precipitation_min_5yr_avg  precipitation_max_5yr_avg
0   1           29.7633          -95.3633      1    2  2024         65.43            60.12            70.34              15.67                  12.45                  18.90                  0.75                    0.00                    0.25
```
Note: The values above are placeholders; actual values depend on Open-Meteo API data for the specified date and location.
## Inputs
- `latitude`: Float (e.g., 29.7633 for Houston, TX)
- `longitude`: Float (e.g., -95.3633 for Houston, TX)
- `month`: Integer (1–12)
- `day`: Integer (1–31, depending on the month)
- `year`: Integer (e.g., 2024, starting year for the five-year history)

## Classes and Methods
### `LocationWeather` Class
Fetches and processes weather data from Open-Meteo.
- Attributes:
  - `latitude`, `longitude`: Location coordinates
  - `month`, `day`, `year`: Date for weather data
  - `avg_temp`, `min_temp`, `max_temp`: Temperature statistics (°F)
  - `avg_wind_speed`, `min_wind_speed`, `max_wind_speed`: Wind speed statistics (mph)
  - `sum_precipitation`, `min_precipitation`, `max_precipitation`: Precipitation statistics (inches)

- Methods:
  - `get_weather_data()`: Fetches daily weather data for the specified date across five years. Returns a dictionary with years, temperatures, wind speeds, and precipitation.
  - `stats_fy_temps()`: Calculates average, minimum, and maximum temperatures over five years.
  - `stats_fy_wind_speed()`: Calculates average, minimum, and maximum wind speeds over five years.
  - `stats_fy_precip()`: Calculates total, minimum, and maximum precipitation over five years.

### `Weather` Class
Manages storage of weather data in a SQLite database.
- Attributes:
  - Table `weather_table` with columns for location, date, and weather statistics.

- Methods:
  - `query_weather()`: Returns a pandas DataFrame of all records in the `weather_table`.

## Running Tests
The `Test.py` file contains unit tests for the `LocationWeather` class using `unittest` and `unittest.mock` to mock API responses. To run the tests:
```bash

python -m unittest Test.py
```
The tests verify:
- `get_weather_data()`: Returns a dictionary with expected keys and five years of data.
- `stats_fy_temps()`: Correctly calculates temperature statistics.
- `stats_fy_wind_speed()`: Correctly calculates wind speed statistics.
- `stats_fy_precip()`: Correctly calculates precipitation statistics.

## Limitations
- Inputs are hardcoded in `main.py` and must be modified directly in the code.
- The API relies on Open-Meteo’s historical data availability, which may vary by location or date.
- Timezone is hardcoded to `America/Chicago` in `LocationWeather.py`.
- Only daily data for a specific date across five years is supported.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

