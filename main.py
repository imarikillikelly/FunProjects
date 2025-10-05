# main.py

# -------C3: Create main.py file and instance of class and methods from C1 & C2-------

from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base

from weather import EventWeather

engine = create_engine("sqlite:///weather.db", echo = True)
Session = sessionmaker(bind = engine)
base = declarative_base()

# --------------------C4: Create a class that creates a table in SQLite--------------------
class Weather(base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key = True)
    latitude = Column(Float)
    longitude = Column(Float)
    month = Column(Integer)
    day = Column(Integer)
    year = Column(Integer)
    avg_temp = Column(Float)
    min_temp = Column(Float)
    max_temp = Column(Float)
    avg_wind_mph = Column(Float)
    min_wind_mph = Column(Float)
    max_wind_mph = Column(Float)
    sum_precip_in = Column(Float)
    min_precip_in = Column(Float)
    max_precip_in = Column(Float)

    # Define the representation of the class
    def __repr__(self):
        return (f"<Weather(latitude = {self.latitude},"
                f" longitude = {self.longitude},"
                f" month = {self.month},"
                f" day = {self.day},"
                f" year = {self.year},"
                f" avg_temp = {self.avg_temp},"
                f" min_temp = {self.min_temp},"
                f" max_temp = {self.max_temp},"
                f" avg_wind_mph = {self.avg_wind_mph},"
                f" min_wind_mph = {self.min_wind_mph},"
                f" max_wind_mph = {self.max_wind_mph},"
                f" sum_precip_in = {self.sum_precip_in},"
                f" min_precip_in = {self.min_precip_in},"
                f" max_precip_in = {self.max_precip_in})>")

#--------------------C6: Define functions to retrieve all weather data from the table--------------------
def get_all_weather(session):
    rows = session.query(Weather).all()
    print("\n--- All rows in 'weather' table ---")
    for row in rows:
        print(row)
    return rows

def get_weather_for_year(session, year):
    return session.query(Weather).filter(Weather.year == year).first()

def get_weather(session):
    return get_all_weather(session)


if __name__ == "__main__":
    # Define event details
    manvel_latitude = 29.46274
    manvel_longitude = -95.35799
    event_month = 6
    event_day = 25
    event_year = 2025
    year_range = list(range(event_year - 4, event_year + 1))

    # Create an instance of the EventWeather class
    event = EventWeather(manvel_latitude, manvel_longitude, event_month, event_day, event_year)
    event.compute_five_years(year_range)

    print("Past five-year historical weather aggregation for June 25th in Manvel, TX ({}–{}):".format(year_range[0], year_range[-1]))
    print("Avg Temp (F):", event.five_yr_avg_temp)
    print("Min Temp (F):", event.five_yr_min_temp)
    print("Max Temp (F):", event.five_yr_max_temp)
    print("Avg Wind (mph):", event.five_yr_avg_wind_mph)
    print("Min Wind (mph):", event.five_yr_min_wind_mph)
    print("Max Wind (mph):", event.five_yr_max_wind_mph)
    print("Sum Precip (in):", event.five_yr_sum_precip_in)
    print("Min Precip (in):", event.five_yr_min_precip_in)
    print("Max Precip (in):", event.five_yr_max_precip_in)

    # --------------------C5: Populate the table with the weather data--------------------
    # Create tables
    base.metadata.create_all(engine)
    # Create a session
    session = Session()
    # Delete all rows in the table prior to loading new data
    session.query(Weather).delete()
    session.commit()
    # Use variables from the created instance of the Weather class and add it to the session
    weather1 = Weather(latitude = manvel_latitude,
                       longitude = manvel_longitude,
                       month = event_month,
                       day = event_day,
                       year = event_year,
                       avg_temp = event.five_yr_avg_temp,
                       min_temp = event.five_yr_min_temp,
                       max_temp = event.five_yr_max_temp,
                       avg_wind_mph = event.five_yr_avg_wind_mph,
                       min_wind_mph = event.five_yr_min_wind_mph,
                       max_wind_mph = event.five_yr_max_wind_mph,
                       sum_precip_in = event.five_yr_sum_precip_in,
                       min_precip_in = event.five_yr_min_precip_in,
                       max_precip_in = event.five_yr_max_precip_in)

    # Update the database
    session.add(weather1)
    session.commit()

    #----------------C6: Retrieve and print all weather data from the table----------------
    get_weather(session)