import pandas as pd
import xarray as xr
from datetime import datetime
import cftime 

# Load the dataset
ds = xr.open_dataset('datasets_nc/precipitation.nc')

'''# Check the units of the 'psl' variable
pr_units = ds['pr'].attrs.get('units', 'No units attribute found')
print(f"The units of precipitation are: {pr_units}")'''

# Convert cftime.DatetimeJulian to Python datetime
def convert_cftime_to_datetime(cftime_array):
    python_dates = [datetime(year=date.year, month=date.month, day=date.day, hour=date.hour, minute=date.minute, second=date.second) for date in cftime_array]
    return pd.to_datetime(python_dates)

# Apply the conversion
ds['time'] = convert_cftime_to_datetime(ds['time'].values)

# print(ds.info())

# Resample to monthly data
monthly_pr = ds['pr'].resample(time='1M').mean()

# Aggregate spatially by taking the global mean
global_mean_pr = monthly_pr.mean(dim=['lat', 'lon'])

# Convert to DataFrame
df = global_mean_pr.to_dataframe().reset_index()

# Extract year and month from the datetime column
df['Year'] = df['time'].dt.year
df['Month'] = df['time'].dt.month

# Convert pr from kg m^-2 s^-1 to mm month^-1
seconds_in_day = 86400
df['days_in_month'] = df['time'].dt.days_in_month
df['pr_mm_month'] = df['pr'] * seconds_in_day * df['days_in_month']

df = df[['Year', 'Month', 'pr_mm_month']]  # Reorder columns

# Save to CSV
df.to_csv('processed_csv/processed_precipitation.csv', index=False)


