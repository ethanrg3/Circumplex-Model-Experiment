# Main data analysis script for the circumplex model experiment
# This script will read in the track data and the form responses, and then perform analysis to see how the tracks were rated by the participants in terms of valence and energy

from ingest_tracks import create_track_df
from ingest_form import read_form_responses, TRACK_ORDER
from pathlib import Path
import polars as pl
from plotnine import *
from polars import col as c

FORM_PATH = Path("/Users/ethanrg/Projects/Hubproject/Circumplex-Model-Experiment/circumplex_hubproj_responses.csv")

def read_data() -> None:
    """Read in the track data and form responses."""
    tracks = create_track_df()
    form_responses = read_form_responses(FORM_PATH)
    return tracks, form_responses

def plot_single_track_VE(track: str, form_responses: pl.DataFrame, tracks: pl.DataFrame) -> None:
    """Plot the valence and energy of a single track from spotify data and the form responses."""
    spotify_track_df = tracks.filter(c.track_name == track)

    # get median valence and energy from form responses (1-7 scale, normalize to 0-1)
    valence_col = f"{track}_valence"
    energy_col = f"{track}_energy"
    med_valence = form_responses.select(c(valence_col).median()).item()
    med_energy = form_responses.select(c(energy_col).median()).item()
    # normalize from 1-7 scale to 0-1
    med_valence_norm = (med_valence - 1) / 6
    med_energy_norm = (med_energy - 1) / 6

    # build a comparison df with both sources
    comparison_df = pl.DataFrame({
        "source": ["Spotify", "Form Median"],
        "valence": [spotify_track_df["valence"][0], med_valence_norm],
        "energy": [spotify_track_df["energy"][0], med_energy_norm],
    })

    # clean track name string for a title
    clean_track_lst = track.split("_")
    clean_track = ""
    for i in range(len(clean_track_lst)):
        if i != len(clean_track_lst) - 1:
            clean_track += f"{clean_track_lst[i].capitalize()} "
        else:
            clean_track += clean_track_lst[i].capitalize()

    plot = (
        comparison_df
        .pipe(ggplot, aes(x="energy", y="valence", color="source", label="source"))
        + geom_point(size=4)
        + geom_text(size=8, nudge_y=0.03)
        + scale_x_continuous(limits=(0, 1))
        + scale_y_continuous(limits=(0, 1))
        + labs(
            x="Energy",
            y="Valence",
            title=f"Valence vs Energy: {clean_track}",
            color="Source"
        )
    )
    plot.show()


def clean_track_name(track: str) -> str:
    """Convert snake_case track name to Title Case."""
    return " ".join(word.capitalize() for word in track.split("_"))

def plot_all_tracks_VE(form_responses: pl.DataFrame, tracks: pl.DataFrame) -> None:
    """Plot valence vs energy for all 6 tracks in a faceted grid."""
    rows = []
    for track in TRACK_ORDER:
        spotify_row = tracks.filter(c.track_name == track)
        valence_col = f"{track}_valence"
        energy_col = f"{track}_energy"
        med_valence = form_responses.select(c(valence_col).median()).item()
        med_energy = form_responses.select(c(energy_col).median()).item()
        med_valence_norm = (med_valence - 1) / 6
        med_energy_norm = (med_energy - 1) / 6
        clean_name = clean_track_name(track)

        rows.append({"track": clean_name, "source": "Spotify",
                      "valence": spotify_row["valence"][0], "energy": spotify_row["energy"][0]})
        rows.append({"track": clean_name, "source": "Form Median",
                      "valence": med_valence_norm, "energy": med_energy_norm})

    comparison_df = pl.DataFrame(rows)
    print(comparison_df)

    plot = (
        comparison_df
        .pipe(ggplot, aes(x="energy", y="valence", color="source", label="source"))
        + geom_point(size=3, )
        + geom_text(size=7, nudge_y=0.04)
        + scale_x_continuous(limits=(0, 1))
        + scale_y_continuous(limits=(0, 1))
        + facet_wrap("track", ncol=3)
        + labs(x="Energy", y="Valence", title="Spotify vs Form Median: Valence and Energy", color="Source")
        + theme(figure_size=(12, 8))
    )
    plot.show()

def main() -> None:
    """Main function to run the analysis."""
    tracks, form_responses = read_data()
    plot_all_tracks_VE(form_responses, tracks)

if __name__ == "__main__":
    main()