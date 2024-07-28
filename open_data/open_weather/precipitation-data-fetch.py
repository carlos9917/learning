import requests
import pandas as pd
from datetime import datetime, timedelta

def get_precipitation_data(latitude, longitude, start_date, end_date):
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "precipitation_sum",
        "timezone": "GMT"
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame({
            'date': data['daily']['time'],
            'precipitation': data['daily']['precipitation_sum']
        })
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return df
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
latitude = 40.7128  # New York City
longitude = -74.0060
start_date = "2023-01-01"
end_date = "2023-12-31"

precipitation_data = get_precipitation_data(latitude, longitude, start_date, end_date)

if precipitation_data is not None:
    print(precipitation_data)
    total_precipitation = precipitation_data['precipitation'].sum()
    print(f"Total precipitation: {total_precipitation:.2f} mm")
