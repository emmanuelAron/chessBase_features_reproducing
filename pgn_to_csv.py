# pgn_to_csv.py

# 1) We are doing a first extraction and retreatment by recreating 6 columns for our csv file.
# 2) We will print the number of rows of this DataFrame (almost equivalent to the number of games but not exactly)
# 3) Then we will work on the cleaning part.

import chess.pgn
import pandas as pd

# Open the PGN file
pgn_file = open("games_1990.pgn")

# Initialize a list to store the games
games_data = []

while True:
    game = chess.pgn.read_game(pgn_file)
    if game is None:
        break

    # Extract game information
    game_data = {
        "White": game.headers["White"],
        "Black": game.headers["Black"],
        "Result": game.headers["Result"],
        "Event": game.headers["Event"],
        "Date": game.headers["Date"],
        "Moves": game.mainline_moves()
    }
    games_data.append(game_data)

# Convert to DataFrame
df = pd.DataFrame(games_data)

# Convert to CSV
df.to_csv("games_1990.csv", index=False)

# Display the first 20 rows
print(df.head(20))

# 2 Number of rows of this DataFrame
print('Number of rows :', len(df))

# Cleaning:
"""
Basically this csv is already cleaned but we can achieve some minor improvements.
We can remove the first row, we can remove also rows where 
"kampflos" is present, or "een" (human error ?) (in 'Moves' column).
Also we can see that there is Date in the format "1990.??.??" for the majority of rows
and a full date for a minority of rows (ie : 1990.11.04). We could eventually decide to
print only 1990 when there is ?? but I think that it is more coherent to keep the same 
format everywhere. And what are the column types?
"""

# Display column types
print(df.dtypes)

# Drop the first row permanently
df.drop(index=0, inplace=True)

# Drop rows containing "kampflos" or other pattern in "Moves" column
mask = df["Moves"].str.contains("kampflos") | df["Moves"].str.contains("een")
df = df[~mask]

# Convert 'Date' column to datetime with handling invalid values
df['Date'] = pd.to_datetime(df['Date'], format='%Y.%m.%d', errors='coerce')

# Replace NaT by "1990-01-01" if needed
df['Date'] = df['Date'].fillna(pd.to_datetime("1990-01-01"))

# Check column types after cleaning
print(df.dtypes)
