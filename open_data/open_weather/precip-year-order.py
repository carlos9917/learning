import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.io import write_image
from datetime import datetime


colors = {'past_decade': 'red',
          'other': 'blue',
          'Good': 'lightgreen',
          'Great': 'darkgreen'}


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

def get_ordered_yearly_precipitation(df):
    # Resample to yearly data
    yearly_data = df.resample('Y').sum()
    yearly_data['year'] = yearly_data.index.year
    
    # Sort years by precipitation amount
    yearly_data_sorted = yearly_data.sort_values('precipitation')
    
    return yearly_data_sorted

def plot_ordered_yearly_precipitation(df):
    df["decade"] = ["past_decade" if year > 2013 else "other" for year in df["year"]]
    color_array = ['red' if decade == 'past_decade' else 'blue' for decade in df['decade']]
    fig = go.Figure()
    df.sort_values(by = ["precipitation"],inplace=True)
    df.sort_index(axis=1,inplace=True)
    # Reset the index to the sorted order
    df_reset = df.reset_index(drop=True)
    # Set the sorted index to the DataFrame
    df.index = df_reset.index.sort_values()
    print(df)
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['precipitation'],
        text=df.apply(lambda row: f"{row['year']}<br>{row['precipitation']:.1f} mm", axis=1),
        textposition='outside',
        textangle=0,
        #marker_color='skyblue',
        marker_color=color_array,  # Use the color array here
        hoverinfo='text'
    ))
    
    # Add average line
    avg_precipitation = df['precipitation'].mean()
    fig.add_hline(y=avg_precipitation, line_dash="dash", line_color="red", 
                  annotation_text="Average", annotation_position="top left")
    
    fig.update_layout(
        title='Yearly Precipitation in Denmark (1991-2024)',
        xaxis_title='Year',
        yaxis_title='Precipitation (mm)',
        template='plotly_white',
        xaxis=dict(tickmode='array', tickvals=df.index, ticktext=df['year']),
        showlegend=False
    )
    
    return fig

def save_figure(fig, filename, format='png'):
    full_filename = f"{filename}.{format}"
    write_image(fig, full_filename)
    print(f"Figure saved as {full_filename}")

# Main execution
if __name__ == "__main__":
    # Approximate center coordinates of Denmark
    latitude = 56.2639  # Denmark
    longitude = 9.5018
    
    # Set date range for 1991-2020
    start_date = "1991-01-01"
    end_date = "2024-07-24"
    
    precipitation_data = get_precipitation_data(latitude, longitude, start_date, end_date)
    
    if precipitation_data is not None:
        ordered_yearly_precipitation = get_ordered_yearly_precipitation(precipitation_data)
        fig = plot_ordered_yearly_precipitation(ordered_yearly_precipitation)
        
        # Display the figure
        fig.show()
        
        # Save the figure as an image
        save_figure(fig, "denmark_ordered_yearly_precipitation_1991_2024", format="png")
        #save figure as html
        #fig.write_html("denmark_ordered_yearly_precipitation_1991_2024.html")

        print("\nYears ordered by precipitation amount:")
        print(ordered_yearly_precipitation[['year', 'precipitation']])
        print(f"\nAverage yearly precipitation: {ordered_yearly_precipitation['precipitation'].mean():.1f} mm")
    else:
        print("Failed to retrieve precipitation data.")
