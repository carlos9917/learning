import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def get_precipitation_data(latitude, longitude, start_date, end_date):
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "precipitation_sum",
        "timezone": "Europe/Copenhagen"
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

def get_wettest_months(df):
    # Resample to monthly data
    monthly_data = df.resample('M').sum()
    monthly_data['year'] = monthly_data.index.year
    monthly_data['month'] = monthly_data.index.strftime('%b')
    
    # Get the 12 wettest months for each year
    wettest_months = monthly_data.groupby('year').apply(lambda x: x.nlargest(12, 'precipitation')).reset_index(drop=True)
    
    # Sort all wettest months from driest to wettest
    wettest_months_sorted = wettest_months.sort_values('precipitation')
    
    return wettest_months_sorted

def plot_wettest_months(df):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['precipitation'],
        text=df.apply(lambda row: f"{row['month']}-{row['year']}<br>{row['precipitation']:.1f} mm", axis=1),
        textposition='outside',
        textangle=-90,
        textfont=dict(size=8),
        hoverinfo='text'
    ))
    
    fig.update_layout(
        title='12 Wettest Months per Year in Denmark (1991-2020)',
        xaxis_title='Rank (Driest to Wettest)',
        yaxis_title='Precipitation (mm)',
        template='plotly_white',
        xaxis=dict(tickmode='linear', dtick=50),  # Show tick every 50 bars
        showlegend=False
    )
    
    fig.show()

# Main execution
if __name__ == "__main__":
    # Approximate center coordinates of Denmark
    latitude = 56.2639  # Denmark
    longitude = 9.5018
    
    # Set date range for 1991-2020
    start_date = "1991-01-01"
    end_date = "2024-06-30"
    
    precipitation_data = get_precipitation_data(latitude, longitude, start_date, end_date)
    
    if precipitation_data is not None:
        wettest_months = get_wettest_months(precipitation_data)
        plot_wettest_months(wettest_months)
        
        print(f"Total wettest months: {len(wettest_months)}")
        print("\nTop 5 wettest months:")
        print(wettest_months.nlargest(5, 'precipitation')[['year', 'month', 'precipitation']])
        print("\nBottom 5 wettest months:")
        print(wettest_months.nsmallest(5, 'precipitation')[['year', 'month', 'precipitation']])
    else:
        print("Failed to retrieve precipitation data.")
