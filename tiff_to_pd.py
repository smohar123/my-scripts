import pandas as pd
import numpy as np
from PIL import Image

def tiff_to_dataframe(tiff_path):
    """
    Converts a TIFF image to a Pandas DataFrame.

    Args:
        tiff_path (str): The path to the TIFF image file.

    Returns:
        pandas.DataFrame: A DataFrame representing the image data, or None if an error occurs.
    """
    try:
        with Image.open(tiff_path) as img:
            img_array = np.array(img)
            df = pd.DataFrame(img_array.reshape(-1, img_array.shape[-1]))
            return df
    except FileNotFoundError:
        print(f"Error: TIFF file not found at '{tiff_path}'")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
tiff_file_path = '/Users/smohar/Downloads/13SGA.tiff'  # Replace with the actual path to your TIFF file
df_from_tiff = tiff_to_dataframe(tiff_file_path)

if df_from_tiff is not None:
    print("TIFF image converted to DataFrame successfully.")
    print(df_from_tiff.head())
else:
    print("TIFF to DataFrame conversion failed.")