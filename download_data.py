"""
Script to download the country data CSV file from Google Drive
Run this first before running the analysis
"""

import gdown
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Google Drive file ID from the original script
file_id = '1IRQWbO9m-c93XjDsbtt2nqv5RVldVPzj'

# Download the file
output_path = 'data/countries.csv'

print("Downloading country data from Google Drive...")
print(f"File ID: {file_id}")
print(f"Output path: {output_path}")

# Download using gdown
url = f'https://drive.google.com/uc?id={file_id}'
gdown.download(url, output_path, quiet=False)

print("\nDownload complete!")
print(f"File saved to: {output_path}")

# Verify the file
import pandas as pd

try:
    data = pd.read_csv(output_path)
    print(f"\nFile loaded successfully!")
    print(f"Shape: {data.shape}")
    print(f"Columns: {list(data.columns)}")
    print("\nFirst few rows:")
    print(data.head())
except Exception as e:
    print(f"\nError loading file: {e}")
    print("Please check that the file downloaded correctly.")
