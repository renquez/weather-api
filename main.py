from sqlalchemy import Integer, Float, create_engine, engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
import pandas as pd
from LocationWeather import LocationWeather

# create a main.py file
# data for location_weather call
latitude = 29.7633
longitude = -95.3633
year = 2024
month = 1
day = 2


# Set pandas to display all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 0)


# base class for table creation
class Base(DeclarativeBase):
    pass


# C4 write a second class that creates a table using SQLAlchemy ORM
class Weather(Base):
    __tablename__ = 'weather_table'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    location_latitude: Mapped[float] = mapped_column(Float)
    location_longitude: Mapped[float] = mapped_column(Float)
    month: Mapped[int] = mapped_column(Integer)
    day: Mapped[int] = mapped_column(Integer)
    year: Mapped[int] = mapped_column(Integer)
    temp_5yr_avg: Mapped[float] = mapped_column(Float)
    temp_min_5yr_avg: Mapped[float] = mapped_column(Float)
    temp_max_5yr_avg: Mapped[float] = mapped_column(Float)
    wind_speed_5yr_avg: Mapped[float] = mapped_column(Float)
    wind_speed_min_5yr_avg: Mapped[float] = mapped_column(Float)
    wind_speed_max_5yr_avg: Mapped[float] = mapped_column(Float)
    precipitation_5yr_sum: Mapped[float] = mapped_column(Float)
    precipitation_min_5yr_avg: Mapped[float] = mapped_column(Float)
    precipitation_max_5yr_avg: Mapped[float] = mapped_column(Float)

    # C6 - method to query table and return a dataframe
    def query_weather(self):
        # query all records from Weather table
        results = session.query(Weather).all()

        # set results as a dataframe
        data = [
            {
                'id': record.id,
                'location_latitude': record.location_latitude,
                'location_longitude': record.location_longitude,
                'month': record.month,
                'day': record.day,
                'year': record.year,
                'temp_5yr_avg': record.temp_5yr_avg,
                'temp_min_5yr_avg': record.temp_min_5yr_avg,
                'temp_max_5yr_avg': record.temp_max_5yr_avg,
                'wind_speed_5yr_avg': record.wind_speed_5yr_avg,
                'wind_speed_min_5yr_avg': record.wind_speed_min_5yr_avg,
                'wind_speed_max_5yr_avg': record.wind_speed_max_5yr_avg,
                'precipitation_5yr_sum': record.precipitation_5yr_sum,
                'precipitation_min_5yr_avg': record.precipitation_min_5yr_avg,
                'precipitation_max_5yr_avg': record.precipitation_max_5yr_avg
            }
            for record in results
        ]

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # return results
        return df


# db engine creation, drop Weather table if exists, create Weather table
engine = create_engine('sqlite:///weather.db', echo=True)
Weather.__table__.drop(engine, checkfirst=True)
Weather.__table__.create(engine)

# create session to interact with db
Session = sessionmaker(bind=engine)
session = Session()


if __name__ == "__main__":


    # C3 create an instance of LocationWeather class
    houston_weather = LocationWeather(latitude, longitude, month, day, year)


    # C3 call methods set in C2
    # set avg, mins, max using stats methods
    avg_temp, min_temp, max_temp = houston_weather.stats_fy_temps()
    avg_wind, min_wind, max_wind = houston_weather.stats_fy_wind_speed()
    sum_precip, min_precip, max_precip = houston_weather.stats_fy_precip()


    # C5 populate table created in C4 with weather data and commit
    weather_insert = Weather(
        location_latitude = houston_weather.latitude,
        location_longitude = houston_weather.longitude,
        month = month,
        day = day,
        year = year,
        temp_5yr_avg = avg_temp,
        temp_min_5yr_avg = min_temp,
        temp_max_5yr_avg = max_temp,
        wind_speed_5yr_avg = avg_wind,
        wind_speed_min_5yr_avg = min_wind,
        wind_speed_max_5yr_avg = max_wind,
        precipitation_5yr_sum = sum_precip,
        precipitation_min_5yr_avg = min_precip,
        precipitation_max_5yr_avg = max_precip
    )
    session.add(weather_insert)
    session.commit()
    print(f'Data inserted successfully!')


    #set weather table for querying and print
    weather_table = Weather()
    weather_record = Weather.query_weather(weather_table)
    print(weather_record)
    session.close()
