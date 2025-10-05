# weather.py

import requests
from datetime import date

# Base URL for Open-Meteo
o_m_url = "https://archive-api.open-meteo.com/v1/archive"

# ------------------------------C1: Create a dataclass for weather data-----------------------------
class EventWeather:
    # Define where and when for the event day
    def __init__(self, latitude, longitude, month, day, year):
        self.latitude = latitude
        self.longitude = longitude
        self.month = month
        self.day = day
        self.year = year  # anchor year for previous five years

        # All aggregated results will be populated after results are fetched
        self.five_yr_avg_temp = None
        self.five_yr_min_temp = None
        self.five_yr_max_temp = None

        self.five_yr_avg_wind_mph = None
        self.five_yr_min_wind_mph = None
        self.five_yr_max_wind_mph = None

        self.five_yr_sum_precip_in = None
        self.five_yr_min_precip_in = None
        self.five_yr_max_precip_in = None

        # Added for caching each year response
        self._year_cache = {}

    # ------------------------------C2: Required methods for dataclass-----------------------------

    # Grab daily data for this exact month/day in a specific year
    def _get_daily_for_year(self, year):
        # If we already fetched this year, reuse it
        if year in self._year_cache:
            return self._year_cache[year]

        # Convert date into a string for the API
        day_str = date(year, self.month, self.day).isoformat()
        # Parameters to include with the base URL
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start_date": day_str,
            "end_date": day_str,
            "daily": ",".join([
                "temperature_2m_mean", # daily mean temperature
                "wind_speed_10m_max", # daily max wind speed
                "precipitation_sum", # daily total precipitation
            ]),
            "temperature_unit": "fahrenheit",
            "windspeed_unit": "mph",
            "precipitation_unit": "inch",
            "timezone": "America/Chicago",
        }
        # Call API and fetch data from Open-Meteo with response expected within 30 seconds
        weather_info = requests.get(o_m_url, params = params, timeout = 30)
        weather_info.raise_for_status() # Fail if the response code is 4xx or 5xx
        js = weather_info.json()

        # Returns lists for each daily variable
        daily = js.get("daily", {}) # Grab the 'daily' section
        t = daily.get("temperature_2m_mean") or [] # List of temps
        w = daily.get("wind_speed_10m_max") or [] # List of max winds
        p = daily.get("precipitation_sum") or [] # List of precipitation totals

        # Check that the length of all lists is 1, raise an Error if not
        if not (len(t) == len(w) == len(p) == 1):
            raise RuntimeError(f"Unexpected daily array shape for {day_str}")

        # Store the single-day values into a small dictionary
        weather_details = {
            # Uses each single value stored in the lists
            "temp_f": float(t[0]),
            "wind_mph": float(w[0]),
            "precip_in": float(p[0]),
        }
        # Cache and return weather details for this year
        self._year_cache[year] = weather_details
        return weather_details

    def get_mean_temperature_f(self, year):
        return self._get_daily_for_year(year)["temp_f"]

    def get_max_wind_mph(self, year):
        return self._get_daily_for_year(year)["wind_mph"]

    def get_precip_sum_in(self, year):
        return self._get_daily_for_year(year)["precip_in"]

        # Compute & store five-year aggregates in the dataclass fields

    def compute_five_years(self, years = None):
        # Set to the latest year and the four prior years
        if years is None:
            years = list(range(self.year - 4, self.year + 1))

        temps = []
        winds = []
        precs = []
        # Pull each year’s numbers and build lists
        for y in years:
            temps.append(self.get_mean_temperature_f(y))
            winds.append(self.get_max_wind_mph(y))  # daily max wind, then stats across years
            precs.append(self.get_precip_sum_in(y))

        # Average temp across years, plus min/max
        self.five_yr_avg_temp = sum(temps) / len(temps)
        self.five_yr_min_temp = min(temps)
        self.five_yr_max_temp = max(temps)

        # Average wind speed across years, plus min/max
        self.five_yr_avg_wind_mph = sum(winds) / len(winds)
        self.five_yr_min_wind_mph = min(winds)
        self.five_yr_max_wind_mph = max(winds)

        # Average total over five years, plus min/max
        self.five_yr_sum_precip_in = sum(precs)
        self.five_yr_min_precip_in = min(precs)
        self.five_yr_max_precip_in = max(precs)