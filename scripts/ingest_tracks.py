# This script ingests the audio features in JSON format from the 6 tracks played in the experiment

import json
from pathlib import Path
import polars as pl
from plotnine import *
from polars import col as c

# Set the path to the directory containing the track JSON files
track_path = Path("/Users/ethanrg/Projects/Hubproject/Circumplex-Model-Experiment/spotify_data")
track_dfs = []

def create_track_df() -> pl.DataFrame:
    """Create a Polars DataFrame from the track data dictionary."""
    # Loop through each JSON file in the directory
    for track in track_path.glob("*.json"):
        if track.stat().st_size == 0:
            print(f"Skipping empty file: {track.name}")
            continue

        with open(track) as f:
            track_data = json.load(f)  # Load the JSON data into a Python dictionary

        # Wrap the flat dict in a list so polars treats it as a single row
        track_df = pl.DataFrame([track_data]).with_columns(
            pl.lit(track.stem).alias("track_name")
        )
        track_dfs.append(track_df)

    if not track_dfs:
        raise RuntimeError("No valid track JSON files found.")

    # Concatenate all the track DataFrames into a single DataFrame
    tracks_df = pl.concat(track_dfs, how="diagonal")
    return tracks_df

if __name__ == "__main__":
    tracks = create_track_df()
    filtered_tracks = (
        tracks
        .select(c.track_name, c.energy, c.valence)
    )
    print(filtered_tracks)