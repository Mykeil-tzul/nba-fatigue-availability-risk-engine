"""
Data collection script for pulling NBA player game logs.
"""

from pathlib import Path
import pandas as pd
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

from src.config import RAW_DATA_DIR
from src.utils import ensure_directory


def get_player_id(player_name: str) -> int:
    matching_players = players.find_players_by_full_name(player_name)

    if not matching_players:
        raise ValueError(f"No NBA player found for name: {player_name}")

    return matching_players[0]["id"]


def fetch_player_game_logs(player_name: str, season: str = "2024-25") -> pd.DataFrame:
    player_id = get_player_id(player_name)

    gamelog = playergamelog.PlayerGameLog(
        player_id=player_id,
        season=season
    )

    df = gamelog.get_data_frames()[0]
    df["PLAYER_NAME"] = player_name
    df["SEASON"] = season
    return df


def fetch_multiple_players(player_names: list[str], season: str = "2024-25") -> pd.DataFrame:
    all_data = []

    for name in player_names:
        print(f"Fetching data for {name}...")
        df = fetch_player_game_logs(name, season)
        all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)
    return combined_df


def save_multiple_players(
    player_names: list[str],
    season: str = "2024-25",
    filename: str = "multi_player_game_logs.csv"
) -> Path:
    ensure_directory(RAW_DATA_DIR)

    df = fetch_multiple_players(player_names, season)

    output_path = RAW_DATA_DIR / filename
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    players_list = [
        "Kyrie Irving",
        "Stephen Curry",
        "Jalen Brunson",
        "Luka Doncic",
        "Shai Gilgeous-Alexander"
    ]

    saved_path = save_multiple_players(players_list, "2024-25")
    print(f"Saved multi-player data to: {saved_path}")