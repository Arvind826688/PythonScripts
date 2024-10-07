import pandas as pd
import matplotlib.pyplot as plt
import requests
import plotly.express as px

# URL for NASA GISTEMP data (global temperature anomalies)
url = 'https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv'

# Download the data with error handling
try:
    response = requests.get(url)
    response.raise_for_status()
    with open('GLB.Ts+dSST.csv', 'wb') as file:
        file.write(response.content)
except requests.exceptions.RequestException as e:
    print(f"Error downloading data: {e}")
    exit()

# Read the data into a pandas DataFrame
data = pd.read_csv('GLB.Ts+dSST.csv', skiprows=1)

# Process the data
data = data[['Year', 'J-D', 'DJF', 'MAM', 'JJA', 'SON']]
data.columns = ['Year', 'Annual Anomaly', 'DJF', 'MAM', 'JJA', 'SON']

# Replace non-numeric values with NaNs and drop them
data.replace(' ***', pd.NA, inplace=True)
data = data.dropna()

# Convert columns to appropriate data types
data['Year'] = data['Year'].astype(int)
for col in ['Annual Anomaly', 'DJF', 'MAM', 'JJA', 'SON']:
    data[col] = data[col].astype(float)

# Apply a moving average to smooth the data
data['Smoothed Anomaly'] = data['Annual Anomaly'].rolling(window=5).mean()

# Plot the data with different styles
plt.figure(figsize=(14, 7))
plt.plot(data['Year'], data['Annual Anomaly'], marker='o', linestyle='--', color='green', label='Annual Anomaly')
plt.plot(data['Year'], data['Smoothed Anomaly'], color='blue', label='5-Year Moving Average')
plt.axhline(y=0, color='black', linestyle='-.')

# Highlight significant increases or decreases with a different threshold
significant_points = data[(data['Annual Anomaly'] >= 0.6) | (data['Annual Anomaly'] <= -0.6)]
plt.scatter(significant_points['Year'], significant_points['Annual Anomaly'], color='red')
for idx, row in significant_points.iterrows():
    plt.annotate(f"{row['Year']}", (row['Year'], row['Annual Anomaly']), textcoords="offset points", xytext=(0,10), ha='center')

plt.title('Global Temperature Anomalies (1880 - Present)')
plt.xlabel('Year')
plt.ylabel('Temperature Anomaly (°C)')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save the plot in different formats
plt.savefig('global_temperature_anomalies.png')
plt.savefig('global_temperature_anomalies.pdf')
plt.savefig('global_temperature_anomalies.svg')
plt.show()

# Create an interactive plot using Plotly
fig = px.line(data, x='Year', y='Annual Anomaly', title='Global Temperature Anomalies (1880 - Present)')
fig.add_scatter(x=data['Year'], y=data['Smoothed Anomaly'], mode='lines', name='5-Year Moving Average')
fig.add_scatter(x=significant_points['Year'], y=significant_points['Annual Anomaly'], mode='markers', name='Significant Points', marker=dict(color='red'))

# Customize the interactive plot
fig.update_layout(
    title='Global Temperature Anomalies (1880 - Present)',
    xaxis_title='Year',
    yaxis_title='Temperature Anomaly (°C)',
    template='plotly_white'
)

# Show the interactive plot
fig.show()
