# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

import os
import pandas as pd

# Define the folder path where your CSV files are stored
folder_path = '/content/drive/My Drive/Dataset/'

# List files in the folder to verify they exist
print("Files in the folder:", os.listdir(folder_path))

def detect_date_column(df):
    """
    Detects a date column (case-insensitive) in a DataFrame.
    Looks for 'date' or 'observation_date'.
    Raises a ValueError if no such column exists.
    """
    possible_date_columns = ['date', 'observation_date']
    for col in df.columns:
        if col.strip().lower() in possible_date_columns:
            return col
    raise ValueError("No date column found in the dataset.")

def read_dataset(filename, rename_dict):
    """
    Loads a CSV file, converts its date column to datetime, sets it as the index,
    and renames columns as specified.

    Args:
        filename (str): Name of the CSV file.
        rename_dict (dict): Dictionary mapping original column names to new names.

    Returns:
        pd.DataFrame: Processed DataFrame with a DatetimeIndex.
    """
    full_path = os.path.join(folder_path, filename)
    df = pd.read_csv(full_path)

    try:
        date_col = detect_date_column(df)
    except ValueError as e:
        raise ValueError(f"Error in file '{filename}': {e}")

    # Convert the detected date column to datetime (coerce errors)
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    if df[date_col].isnull().all():
        raise ValueError(f"Date conversion failed for column '{date_col}' in file '{filename}'.")

    df.set_index(date_col, inplace=True)

    # Verify the index is a DatetimeIndex
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError(f"Index for file '{filename}' is not a DatetimeIndex after conversion.")

    df = df.rename(columns=rename_dict)
    return df

# Configuration: list of tuples with file name and corresponding renaming dictionary
datasets_config = [
    ('T10YIE.csv', {'T10YIE': '10-Year Breakeven Inflation Rate'}),
    ('T5YIFR.csv', {'T5YIFR': '5-Year, 5-Year Forward Inflation Expectation Rate'}),
    ('CPIAUCNS.csv', {'CPIAUCNS': 'Consumer Price Index'}),
    ('GDPC1.csv', {'GDPC1': 'Real Gross Domestic Product'}),
    ('UNRATE.csv', {'UNRATE': 'Unemployment Rate'}),
    ('FEDFUNDS.csv', {'FEDFUNDS': 'Federal Funds Effective Rate'}),
    ('PCEPI.csv', {'PCEPI': 'Personal Consumption Expenditures: Chain-type Price Index'}),
    ('DTWEXBGS.csv', {'DTWEXBGS': 'Nominal Broad U.S. Dollar Index'}),
    ('DCOILWTICO.csv', {'DCOILWTICO': 'Crude Oil Prices: West Texas Intermediate'}),
    ('DGS10.csv', {'DGS10': '10-Year Treasury Yield'})
]

# Load each dataset using the configuration; skip files with errors.
datasets = []
for filename, rename_dict in datasets_config:
    try:
        df = read_dataset(filename, rename_dict)
        datasets.append(df)
    except Exception as e:
        print(f"Skipping file '{filename}' due to error: {e}")

if not datasets:
    raise ValueError("No datasets loaded successfully. Please check your files.")

# Resample each dataset to a daily frequency and forward-fill missing values
datasets = [df.asfreq('D').ffill() for df in datasets]

# Determine the common date range across all datasets:
#   - New dataset starting point: the newest (maximum) start date among datasets
#   - New dataset ending point: the oldest (minimum) end date among datasets
start_dates = [df.index.min() for df in datasets]
end_dates   = [df.index.max() for df in datasets]

common_start = max(start_dates)
common_end   = min(end_dates)

if common_start > common_end:
    raise ValueError("No overlapping date range among datasets. Check your data.")

print("Common start date:", common_start)
print("Common end date:", common_end)

# Trim each dataset to the common date range
datasets = [df.loc[common_start:common_end] for df in datasets]

# Merge all datasets on the date index using an inner join (keeping only common dates)
merged_df = pd.concat(datasets, axis=1, join='inner')

# Save the merged dataset to a CSV file in the Dataset folder
merged_file_path = os.path.join(folder_path, 'merged_dataset.csv')
merged_df.to_csv(merged_file_path)

print("Merged dataset shape:", merged_df.shape)
print("Merged dataset saved to:", merged_file_path)