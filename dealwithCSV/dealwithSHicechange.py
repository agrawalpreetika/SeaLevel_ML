import pandas as pd

# Load the dataset
df = pd.read_csv('datasets_csv/AntarcticIceChangeRate.csv')  # replace with your file path

# Melt the DataFrame from wide to long format
melted_df = df.melt(id_vars=['Year'], var_name='Month', value_name='sh_icechange')

# Map month names to month numbers
month_mapping = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
}
melted_df['Month'] = melted_df['Month'].map(month_mapping)

# Convert the 'Month' column to integer type if it's not already
melted_df['Month'] = melted_df['Month'].astype(int)

# Save the transformed DataFrame to a new CSV file
output_file_path = 'processed_csv/processed_SHicechange.csv'  # replace with desired output path
melted_df.to_csv(output_file_path, index=False)





