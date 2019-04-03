import unittest
from modules.weather import current_weather, transform_current_weather, \
    five_day_weather, transform_forecast_weather, aggregate_forecast, get_current_location


class WeatherTests(unittest.TestCase):
    """
    Runs all tests to make sure that the weather functionality works as expected.
    """

    def test_bad_locations(self):
        """
        Tests to see if the weather functions catch bad locations properly.
        """

        weather_json, msg = current_weather("asdf, asdf")
        self.assertTrue(weather_json is None)

        weather_json, msg = current_weather("Chicago, IL")
        self.assertTrue(weather_json is None)

        weather_json, msg = five_day_weather("asdf, asdf")
        self.assertTrue(weather_json is None)

        return

    def test_good_location(self):
        """
        Tests to see if the weather functions catch good locations properly.
        """

        weather_json, msg = current_weather("Chicago, US")
        self.assertTrue(weather_json is not None)

        transformed_json = transform_current_weather(weather_json)
        self.assertEqual("Chicago", transformed_json["name"])
        self.assertEqual("US", transformed_json["country"])

        weather_json, msg = current_weather("San Diego, US")
        self.assertTrue(weather_json is not None)

        transformed_json = transform_current_weather(weather_json)
        self.assertEqual("San Diego", transformed_json["name"])
        self.assertEqual("US", transformed_json["country"])

        weather_json, msg = current_weather("Moscow, RU")
        self.assertTrue(weather_json is not None)

        transformed_json = transform_current_weather(weather_json)
        self.assertEqual("Moscow", transformed_json["name"])
        self.assertEqual("RU", transformed_json["country"])

        return

    def test_current_location(self):
        """
        Tests to see if the current location of the user is caught.
        """

        city, country, msg = get_current_location()
        self.assertEqual(city, "Urbana")
        self.assertEqual(country, "US")

        return

    def test_forecast(self):
        """
        Tests to see if the forecast functionality works as intended.
        """

        weather_json, msg = five_day_weather("Champaign, US")
        self.assertTrue(weather_json is not None)

        transformed_json = transform_forecast_weather(weather_json)
        self.assertEqual(transformed_json["name"], "Champaign")
        self.assertEqual(transformed_json["country"], "US")

        n = len(transformed_json["reports"])
        self.assertTrue(n > 5)

        aggregate_forecast(transformed_json)
        self.assertTrue(len(transformed_json["reports"]) != n)
        self.assertEqual(len(transformed_json["reports"]), 5)

        return


if __name__ == '__main__':
    unittest.main()
