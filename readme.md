**Event Weather Snapshot (C867)**

One-day weather snapshot for a fixed location and date, aggregated across the previous five years (fetched from the Open-Meteo Historical API and stored locally in SQLite for easy querying).

**Language:** Python

**DB:** SQLite (weather.db)

**API:** Open-Meteo Historical Weather API

**Scope:** One location + one day (anchor year + previous 4 years)

**What this program does:**
* Pulls daily mean temperature (°F), daily max wind (mph), and daily precipitation total (in) for chosen month/day in each year of a 5-year window.
* Computes five-year average/min/max for temperature & wind, plus sum/min/max for precipitation.
* Saves the aggregated results into a local SQLite table.
* Reads the row back and prints a summary.

The program is intentionally scoped to one fixed location and date (Manvel, TX). The code currently sets these in main.py.

**Requirements:**
* Python 3.10+
* Internet access (to call the Open-Meteo API)
* Packages (installed via requirements.txt)
  * SQLALchemy
  * requests

**Credits:**

Weather data: [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
)

**Run order:**

#setup

`python -m venv .venv`

`source .venv/bin/activate`

`pip install -r requirements.txt`

#run the program

`python main.py`

#(optional) run tests

`python -m unittest -v`