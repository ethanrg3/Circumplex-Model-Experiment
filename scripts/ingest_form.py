# This script will ingest the Google Form responses for our experiment. 
# The responses will be output to a Google Sheet which will then be downloaded in csv format

import polars as pl
from pathlib import Path

def read_csv_polars(file_path: str) -> pl.DataFrame:
    """Read a CSV file and return a Polars DataFrame."""
    return pl.read_csv(file_path)

def test_read_csv() -> None:
    """Test the CSV reading function."""
    csv_path = Path("/Users/ethanrg/Projects/Hubproject/Circumplex-Model-Experiment/circumplex_hub_form_responses.csv")
    df = read_csv_polars(csv_path)
    print(df.head())

def main() -> None:
    test_read_csv()

if __name__ == "__main__":
    main()