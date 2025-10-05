import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import Weather, base, get_weather_for_year, get_all_weather

anchor_year = 2025  # in sync with main.py


def make_session():
    engine = create_engine("sqlite:///:memory:", future=True)
    base.metadata.create_all(engine)
    return sessionmaker(bind=engine, future=True)()


class TestMain(unittest.TestCase):
    def test_get_weather_for_year_returns_none_when_empty(self):
        s = make_session()
        self.assertIsNone(get_weather_for_year(s, anchor_year))

    def test_insert_and_fetch_by_year(self):
        s = make_session()
        # insert one very simple row
        row = Weather(
            latitude=29.46274, longitude=-95.35799,
            month=6, day=25, year=anchor_year,
            avg_temp=71.2, min_temp=68.0, max_temp=75.0,
            avg_wind_mph=17.6, min_wind_mph=10.0, max_wind_mph=25.0,
            sum_precip_in=0.35, min_precip_in=0.0, max_precip_in=0.2
        )
        s.add(row)
        s.commit()

        found = get_weather_for_year(s, anchor_year)
        self.assertIsNotNone(found)
        self.assertEqual(found.year, anchor_year)
        self.assertAlmostEqual(found.avg_temp, 71.2, places=6)

    def test_get_all_weather_runs_without_error(self):
        s = make_session()
        s.add(Weather(year=anchor_year))  # minimal insert; other fields are nullable
        s.commit()
        # should not raise; also sanity-check count
        get_all_weather(s)
        self.assertGreaterEqual(s.query(Weather).count(), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)