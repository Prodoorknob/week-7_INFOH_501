import unittest
import pandas as pd
from loader import *

TOL=1e-3

class TestLoader(unittest.TestCase):

    def setUp(self):
        self.geolocator=get_geolocator()

    def test_valid_locations(self):
        
        locations = ["Museum of Modern Art", "USS Alabama Battleship Memorial Park"]

        df = build_geo_dataframe(self.geolocator,locations)

        expected = {
            "Museum of Modern Art": (40.7618552, -73.9782438, "museum"),
            "USS Alabama Battleship Memorial Park": (30.684373, -88.015316, "park"),
        }

        found_types = df["type"].astype(str).str.lower().tolist()
        for name, (lat, lon, type) in expected.items():
            lat_ok = np.any(np.isclose(df["latitude"].values,  lat, atol=TOL))
            lon_ok = np.any(np.isclose(df["longitude"].values, lon, atol=TOL))
            type_ok = type in found_types
            self.assertTrue(lat_ok, f"{name}: latitude not within tolerance")
            self.assertTrue(lon_ok, f"{name}: longitude not within tolerance")
            self.assertTrue(type_ok, f"{name}: expected type '{type}' not found in {found_types}")


    def test_invalid_location(self):
        
        result = fetch_location_data(self.geolocator, "asdfqwer1234")

        self.assertTrue(pd.isna(result["latitude"]))
        self.assertTrue(pd.isna(result["longitude"]))
        self.assertTrue(pd.isna(result["type"]))

if __name__ == "__main__":
    unittest.main()
