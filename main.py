from support_functions import process_dataframe_columns
from mappings import source_columns_mapping
import logging
import pandas as pd

# Create a custom logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def process_file(filename, processed_filename, column_mapping):
    df = pd.read_csv(filename)
    df = process_dataframe_columns(df, column_mapping)
    df.to_csv(processed_filename)

if __name__ == "__main__":
    process_file('source_data.csv', 'final.csv', source_columns_mapping)

