import pandas as pd
import xarray as xr
from datetime import datetime
import cftime

# Load the dataset
ds = xr.open_dataset('datasets_nc/surfaceairtemp.nc') # temp unit is Kelvin changes to celsius

'''#Check the units of the 'psl' variable
tas_units = ds['tas'].attrs.get('units', 'No units attribute found')
print(f"The units of surface air temperature are: {tas_units}")'''

# Convert cftime.DatetimeJulian to Python datetime
def convert_cftime_to_datetime(cftime_array):
    # Convert cftime.DatetimeJulian to Python datetime
    python_dates = [datetime(year=date.year, month=date.month, day=date.day, hour=date.hour, minute=date.minute, second=date.second) for date in cftime_array]
    return pd.to_datetime(python_dates)

# Apply the conversion
ds['time'] = convert_cftime_to_datetime(ds['time'].values)

# Convert temperature from Kelvin to Celsius
# 'tos' is the variable for sea surface temperature
ds['tas'] = ds['tas'] - 273.15

# Resample to monthly data
monthly_tas = ds['tas'].resample(time='1M').mean()

# Aggregate spatially by taking the global mean
global_mean_tas = monthly_tas.mean(dim=['lat', 'lon'])

# Convert to DataFrame
df = global_mean_tas.to_dataframe().reset_index()

# Extract year and month from the datetime column
df['Year'] = df['time'].dt.year
df['Month'] = df['time'].dt.month
df = df[['Year', 'Month', 'tas']]  # Reorder columns

# Save to CSV
df.to_csv('processed_csv/processed_surfaceairtemp.csv', index=False)


