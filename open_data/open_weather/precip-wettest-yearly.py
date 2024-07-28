import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from plotly.io import write_image

def save_figure(fig, filename, format='png'):
    """
    Save the Plotly figure as an image file.
    
    :param fig: Plotly figure object
    :param filename: Name of the file to save (without extension)
    :param format: Format to save the image (default is 'png')
    """
    full_filename = f"{filename}.{format}"
    write_image(fig, full_filename)
    print(f"Figure saved as {full_filename}")

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

def plot_yearly_precipitation(df):
    fig = go.Figure()
    
    # Calculate average precipitation
    avg_precipitation = df['precipitation'].mean()
    
    # Create color scale based on deviation from average
    max_deviation = max(abs(df['precipitation'] - avg_precipitation))
    colors = ['#FF{:02X}00'.format(int(255 * (1 - abs(val - avg_precipitation) / max_deviation))) if val < avg_precipitation 
              else '#00{:02X}00'.format(int(255 * (1 - abs(val - avg_precipitation) / max_deviation)))
              for val in df['precipitation']]
    
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['precipitation'],
        text=df.apply(lambda row: f"{row['year']}<br>{row['precipitation']:.1f} mm", axis=1),
        textposition='outside',
        textangle=0,
        marker_color=colors,
        hoverinfo='text'
    ))
    
    # Add average line
    fig.add_hline(y=avg_precipitation, line_dash="dash", line_color="black", annotation_text="Average", 
                  annotation_position="bottom right")
    
    fig.update_layout(
        title='Yearly Precipitation in Denmark (1991-2020)',
        xaxis_title='Year (Driest to Wettest)',
        yaxis_title='Precipitation (mm)',
        template='plotly_white',
        xaxis=dict(tickmode='linear', dtick=1),  # Show tick for every year
        showlegend=False
    )
    
    #fig.show()
    return fig

# Main execution
if __name__ == "__main__":
    # Approximate center coordinates of Denmark
    latitude = 56.2639  # Denmark
    longitude = 9.5018
    
    # Set date range for 1991-2020
    start_date = "1991-01-01"
    end_date = "2020-12-31"
    
    precipitation_data = get_precipitation_data(latitude, longitude, start_date, end_date)
    
    if precipitation_data is not None:
        yearly_precipitation = get_yearly_precipitation(precipitation_data)
        fig = plot_yearly_precipitation(yearly_precipitation)
        #fig.show()
        save_figure(fig, "denmark_yearly_precipitation_1991_2020", format="png")

        
        print("\nTop 5 wettest years:")
        print(yearly_precipitation.nlargest(5, 'precipitation')[['year', 'precipitation']])
        print("\nBottom 5 driest years:")
        print(yearly_precipitation.nsmallest(5, 'precipitation')[['year', 'precipitation']])
        print(f"\nAverage yearly precipitation: {yearly_precipitation['precipitation'].mean():.1f} mm")
    else:
        print("Failed to retrieve precipitation data.")
