'''
Script to load geographical data into a pandas DataFrame, and save it as a CSV file.
'''

from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np

timeout=30


def get_geolocator(agent='h501-student'):
    """
    Initiate a Nominatim geolocator instance given an `agent`.

    Parameters
    ----------
    agent : str, optional
        Agent name for Nominatim, by default 'h501-student'
    """
    return Nominatim(user_agent=agent)

def fetch_location_data(geolocator, loc):
    """
    Fetch geographical data (latitude, longitude, and type) for a given location.

    """
    try:
        location = geolocator.geocode(loc, exactly_one=True, addressdetails=True, timeout=timeout)
        if location is None:
            return{
                "location": loc,
                "latitude": np.nan, 
                "longitude": np.nan,
                "type": np.nan
            }
        raw = getattr(location, "raw", {}) or {}
        geo_type = raw.get("type") or raw.get("class")
        return{
                "location": loc,
                "latitude": location.latitude, 
                "longitude": location.longitude,
                "type": geo_type
            }
    except Exception as E:
        print(f"Error, location not found for {loc}:{E}")
        return{
                "location": loc,
                "latitude": np.nan, 
                "longitude": np.nan,
                "type": np.nan
            }

def build_geo_dataframe(geolocator, locations):
    """
    Build a pandas DataFrame with geographical data for a list of locations.

    """
    
    geo_data=[]

    for loc in locations:
        geo_data.append(fetch_location_data(geolocator, loc))

    return pd.DataFrame(geo_data)


if __name__ == "__main__":
    geo = get_geolocator()

    locations = ["Museum of Modern Art", "iuyt8765(*&)", "Alaska", "Franklin's Barbecue", "Burj Khalifa"]

    df = build_geo_dataframe(geo, locations)

    df.to_csv("./geo_data.csv")
