import pandas as pd
import xarray as xr
from datetime import datetime
import cftime 

import pandas as pd

# Load the dataset
ds = xr.open_dataset('datasets_nc/seasurfacetemp.nc') # unit is degree Celsius

# Check the units of the 'psl' variable
tos_units = ds['tos'].attrs.get('units', 'No units attribute found')
print(f"The units of sea surface temperature are: {tos_units}")

# Convert cftime.DatetimeJulian to Python datetime if needed
def convert_cftime_to_datetime(cftime_array):
    python_dates = [datetime(year=date.year, month=date.month, day=date.day, hour=date.hour, minute=date.minute, second=date.second) for date in cftime_array]
    return pd.to_datetime(python_dates)

# Apply the conversion if necessary
if isinstance(ds['time'].values[0], cftime.DatetimeJulian):
    ds['time'] = convert_cftime_to_datetime(ds['time'].values)

# Resample to monthly data
monthly_tos = ds['tos'].resample(time='1M').mean()

# Aggregate spatially by taking the global mean
global_mean_tos = monthly_tos.mean(dim=['lat', 'lon'])

# Convert to DataFrame
df = global_mean_tos.to_dataframe().reset_index()

# Extract year and month from the datetime column
df['Year'] = df['time'].dt.year
df['Month'] = df['time'].dt.month
df = df[['Year', 'Month', 'tos']]  # Reorder columns

# Save to CSV
df.to_csv('processed_csv/processed_seasurfacetemp.csv', index=False)
