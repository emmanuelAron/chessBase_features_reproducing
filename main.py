# main.py

import pandas as pd
from stats import calculate_average_moves, plot_game_length_distribution, plot_eco_category_distribution, plot_games_per_player

# Load the DataFrame from the CSV file created in pgn_to_csv.py
df = pd.read_csv("games_1990.csv")

# Run analysis and visualization functions
calculate_average_moves(df)
plot_game_length_distribution(df)
plot_eco_category_distribution(df)
plot_games_per_player(df)
