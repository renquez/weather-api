import requests


# A class to store location-based weather data
class LocationWeather:
    def __init__(self, latitude: float, longitude: float, month: int, day: int, year: int):

        self.latitude = latitude
        self.longitude = longitude
        self.month = month
        self.day = day
        self.year = year
        self.avg_temp = None
        self.min_temp = None
        self.max_temp = None
        self.avg_wind_speed = None
        self.min_wind_speed = None
        self.max_wind_speed = None
        self.sum_precipitation = None
        self.min_precipitation = None
        self.max_precipitation = None

    # method to fetch weather data
    def get_weather_data(self):
        # lists to capture data
        temps = []
        wind_speeds = []
        precips = []
        # parameters to return desired units of measure
        params = {
            "timezone": "America/Chicago",
            "wind_speed_unit": "mph",
            "temperature_unit": "fahrenheit",
            "precipitation_unit": "inch",
        }

        # years variable and for loop to populate years list containing 5 years
        year1 = self.year
        years = [year1]
        for n in range(4):
            year1 -= 1
            years.append(year1)

        # loop to output 5-year data to dictionary
        for year in years:
            open_meteo_url = (f'https://archive-api.open-meteo.com/v1/archive?'
                              f'latitude={self.latitude}&longitude={self.longitude}&start_date={year}-'
                              f'{self.month:02d}-{self.day:02d}&end_date={year}-{self.month:02d}-'
                              f'{self.day:02d}&daily=temperature_2m_mean,precipitation_sum,wind_speed_10m_max')

            response = requests.get(open_meteo_url, params=params)

            # check for successful get response
            if response.status_code == 200:
                data = response.json()
                print(data)

                temp = data['daily']['temperature_2m_mean'][0]
                wind_speed = data['daily']['wind_speed_10m_max'][0]
                precip = data['daily']['precipitation_sum'][0]

                # append lists with data obtained
                temps.append(temp)
                wind_speeds.append(wind_speed)
                precips.append(precip)

            else:
                print(f'Error: {response.status_code}')
                return None

        return {'years': years, 'temps': temps, 'wind_speeds': wind_speeds, 'precips': precips}


    def stats_fy_temps(self):
        # use get_weather_data method to obtain data
        fy_data = self.get_weather_data()


        # extract temperature data
        fy_temps = [temp for temp in fy_data['temps']]


        # calculate statistics
        self.avg_temp = round(sum(fy_temps) / len(fy_temps), 2)
        self.min_temp = round(min(fy_temps), 2)
        self.max_temp = round(max(fy_temps), 2)
        return self.avg_temp, self.min_temp, self.max_temp


    def stats_fy_wind_speed(self):
        # use get_weather_data method to obtain data
        fy_data = self.get_weather_data()


        # extract windspeed data
        fy_wind_speed = [ws for ws in fy_data['wind_speeds']]


        # calculate statistics
        self.avg_wind_speed = round(sum(fy_wind_speed) / len(fy_wind_speed), 2)
        self.min_wind_speed = round(min(fy_wind_speed), 2)
        self.max_wind_speed = round(max(fy_wind_speed), 2)
        return self.avg_wind_speed, self.min_wind_speed, self.max_wind_speed


    def stats_fy_precip(self):
        # use get_weather_data method to obtain data
        fy_data = self.get_weather_data()


        # extract precipitation data
        fy_precip = [precip for precip in fy_data['precips']]


        # calculate statistics
        self.sum_precipitation = round(sum(fy_precip), 2)
        self.min_precipitation = round(min(fy_precip), 2)
        self.max_precipitation = round(max(fy_precip), 2)
        return self.sum_precipitation, self.min_precipitation, self.max_precipitation
