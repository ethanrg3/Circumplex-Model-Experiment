# Main data analysis script for the circumplex model experiment
# This script will read in the track data and the form responses, and then perform analysis to see how the tracks were rated by the participants in terms of valence and energy

from ingest_tracks import create_track_df, plot_tracks
from ingest_form import read_csv_polars
from pathlib import Path
import polars as pl
from plotnine import *
from polars import col as c

FORM_PATH = Path("/Users/ethanrg/Projects/Hubproject/Circumplex-Model-Experiment/circumplex_hubproj_responses.csv")

def read_data() -> None:
    """Read in the track data and form responses."""
    tracks = create_track_df()
    form_responses = read_csv_polars(FORM_PATH)
    return tracks, form_responses

def main() -> None:
    """Main function to run the analysis."""
    tracks, form_responses = read_data()
    print(tracks.head(), form_responses.head())
    # Merge the track data with the form responses
    #nmerged_data = form_responses.join(tracks, on="track_id")

if __name__ == "__main__":
    main()