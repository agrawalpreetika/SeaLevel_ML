import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('datasets_csv/Arctic Extent.csv') 

# Drop columns that are not needed
df = df.drop(columns=['Annual','Unnamed: 13'])

# Melt the DataFrame from wide to long format
melted_df = df.melt(id_vars=['Year'], var_name='Month', value_name='nh_extent')

# Map month names to month numbers
month_mapping = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
}
melted_df['Month'] = melted_df['Month'].map(month_mapping)

# Handle non-finite values: Replace inf and -inf with NaN, then fill NaN values
melted_df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Fill NaN values with a specific value (e.g., mean, median, mode, or a constant)
fill_value = melted_df['Month'].mean() 
melted_df['Month'] = melted_df['Month'].fillna(fill_value)


# Convert the 'Month' column to integer type if it's not already
melted_df['Month'] = melted_df['Month'].astype(int)


# Save the transformed DataFrame to a new CSV file
output_file_path = 'processed_csv/processed_NHextent.csv'  # replace with desired output path
melted_df.to_csv(output_file_path, index=False)





