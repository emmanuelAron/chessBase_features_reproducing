import pandas as pd
from common.db_connection import connect

# Define the player name you want statistics for
player_name = "Schoene, Ralf" 

# Establish database connection and load the data into `df_view`
connection = connect(host="localhost", user="root", password="emma", database="chessdb")

if connection:
    # Load data from the view into `df_view`
    query = "SELECT * FROM game_opening_details;"
    df_view = pd.read_sql(query, connection)
    
    # Close the connection after loading data
    connection.close()
else:
    print("Failed to connect to the database.")

def display_player_statistics(df, player_name):
    """
    Displays the game statistics for a specific player, including opponent, result, and tournament.

    Parameters:
        df (pd.DataFrame): DataFrame containing games data with columns for 'White', 'Black', 'Result', 'Event'.
        player_name (str): Name of the player whose statistics will be displayed.
    """
    # Filter games where the player played either as White or Black
    player_games = df[(df['White'] == player_name) | (df['Black'] == player_name)].copy()

    # Add a column for the opponent and determine if the game was a win/loss
    player_games['Opponent'] = player_games.apply(
        lambda x: x['Black'] if x['White'] == player_name else x['White'], axis=1
    )
    player_games['Player_Result'] = player_games.apply(
        lambda x: 'Win' if (x['White'] == player_name and x['Result'] == '1-0') or 
                          (x['Black'] == player_name and x['Result'] == '0-1') else
                   'Loss' if (x['White'] == player_name and x['Result'] == '0-1') or 
                              (x['Black'] == player_name and x['Result'] == '1-0') else 'Draw',
        axis=1
    )

    # Select columns to display
    stats_df = player_games[['Opponent', 'Player_Result', 'Event' , 'ECO_Code']]
    
    # Display the DataFrame
    print(f"Statistics for '{player_name}' from {len(player_games)} Games:")
    print(stats_df)

# Call the function with `df_view` and `player_name`
display_player_statistics(df_view, player_name)

