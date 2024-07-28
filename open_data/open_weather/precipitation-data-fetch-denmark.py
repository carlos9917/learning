import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

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



def get_yearly_precipitation(df):
    # Resample to yearly data
    yearly_data = df.resample('Y').sum()
    yearly_data['year'] = yearly_data.index.year

    # Sort years from driest to wettest
    yearly_data_sorted = yearly_data.sort_values('precipitation')

    return yearly_data_sorted



#def plot_monthly_precipitation(df):
#    # Resample to monthly data
#    monthly_data = df.resample('M').sum()
#    
#    # Create the plot
#    fig = go.Figure()
#    
#    fig.add_trace(go.Bar(
#        x=monthly_data.index,
#        y=monthly_data['precipitation'],
#        name='Monthly Precipitation'
#    ))
#    
#    fig.update_layout(
#        title='Monthly Precipitation in Denmark (Last 10 Years)',
#        xaxis_title='Date',
#        yaxis_title='Precipitation (mm)',
#        template='plotly_white'
#    )
#    
#    fig.show()


def plot_monthly_precipitation(df):
    # Resample to monthly data
    monthly_data = df.resample('M').sum()
    
    # Create the plot
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=monthly_data.index,
        y=monthly_data['precipitation'],
        name='Monthly Precipitation'
    ))
    
    # Add vertical lines for year separations
    for year in range(monthly_data.index.year.min() + 1, monthly_data.index.year.max() + 1):
        #fig.add_vline(x=f"{year}-01-01", line_width=1, line_dash="dash", line_color="red")
        fig.add_vline(x=f"{year}-01-01", line_width=1, line_color="black")
    
    fig.update_layout(
        title='Monthly Precipitation in Denmark (Last 10 Years)',
        xaxis_title='Date',
        yaxis_title='Precipitation (mm)',
        template='plotly_white'
    )
    
    fig.show()

def plot_annual_precipitation(df):
    # Resample to yearly data
    yearly_data = df.resample('Y').sum()
    
    # Create the plot
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=yearly_data.index.year,
        y=yearly_data['precipitation'],
        name='Annual Precipitation'
    ))
    
    fig.update_layout(
        title='Annual Precipitation in Denmark (Last 10 Years)',
        xaxis_title='Year',
        yaxis_title='Precipitation (mm)',
        template='plotly_white',
        xaxis=dict(tickmode='linear', dtick=1)  # Ensure all years are shown
    )
    
    # Add value labels on top of each bar
    for i, v in enumerate(yearly_data['precipitation']):
        fig.add_annotation(
            x=yearly_data.index.year[i],
            y=v,
            text=f"{v:.0f}",
            showarrow=False,
            yshift=10
        )
    
    fig.show()

def calculate_climate_normal(df):
    # Resample to yearly data
    yearly_data = df.resample('Y').sum()
    #yearly_data = df.resample('Y').mean()
    
    # Calculate the average
    average_precipitation = yearly_data['precipitation'].mean()
    
    return average_precipitation


# Main execution
if __name__ == "__main__":
    # Approximate center coordinates of Denmark
    latitude = 56.2639  # Denmark
    longitude = 9.5018
    
    # Calculate date range for the last 10 years
    end_date = datetime.now().date()
    days_back = 365*50
    days_back = 365*10
    start_date = end_date - timedelta(days=days_back)
    
    precipitation_data = get_precipitation_data(latitude, longitude, start_date, end_date)
    precipitation_data = get_yearly_precipitation(precipitation_data)
    
    if precipitation_data is not None:
        print(precipitation_data.head())
        total_precipitation = precipitation_data['precipitation'].sum()
        print(f"Total precipitation over 10 years: {total_precipitation:.2f} mm")
        
        # Plot the monthly precipitation
        plot_monthly_precipitation(precipitation_data)
        # Plot the annual precipitation 
        #plot_annual_precipitation(precipitation_data)
    else:
        print("Failed to retrieve precipitation data.")
    
    #Set date range for 1991-2020
    start_date = "1991-01-01"
    end_date = "2020-12-31"
    precipitation_data = get_precipitation_data(latitude, longitude, start_date, end_date)
    calculate_climate_normal(precipitation_data)

    # Calculate the climate normal (1991-2020 average)
    climate_normal = calculate_climate_normal(precipitation_data)
    print(f"Average yearly precipitation (1991-2020): {climate_normal:.2f} mm")
        
    # Plot the yearly precipitation with the climate normal
    #plot_yearly_precipitation_with_average(precipitation_data, climate_normal)
