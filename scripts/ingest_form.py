# This script will ingest the Google Form responses for our experiment.
# The responses will be output to a Google Sheet which will then be downloaded in csv format

import polars as pl
from pathlib import Path

TRACK_ORDER = [
    "a_sky_full_of_stars",
    "politik",
    "yellow",
    "the_scientist",
    "adventure_of_a_lifetime",
    "clocks",
]

COLUMN_NAMES = [
    "timestamp",
    "musical_training",
    "listening_frequency",
    "coldplay_familiarity",
    *[
        f"{track}_{metric}"
        for track in TRACK_ORDER
        for metric in ["valence", "energy", "emotion_word", "confidence"]
    ],
    "song_ranking",
    "coldplay_liking",
]


def read_form_responses(file_path: str | Path) -> pl.DataFrame:
    """Read the Google Form CSV and return a DataFrame with clean column names."""
    df = pl.read_csv(file_path)
    df.columns = COLUMN_NAMES[: len(df.columns)]
    return df


def test_read_csv() -> None:
    """Test the CSV reading function."""
    csv_path = Path(__file__).resolve().parent.parent / "circumplex_hub_form_responses.csv"
    df = read_form_responses(csv_path)
    print(df.head())
    print(df.columns)


def main() -> None:
    test_read_csv()

if __name__ == "__main__":
    main()