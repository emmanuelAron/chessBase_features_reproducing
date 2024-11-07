
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common.db_connection import connect

# Connect to the database
connection = connect(host="localhost", user="root", password="emma", database="chessdb")

if connection:
    # Load data from the view into a DataFrame
    query = "SELECT * FROM game_opening_details;"
    df_view = pd.read_sql(query, connection)
    
    # Close the connection after loading data
    connection.close()
else:
    print("Failed to connect to the database.")

def calculate_average_moves(df):
    """
    Calculates the average number of moves per game.
    """
    average_turns = df['Moves'].apply(lambda x: len(x.split()) if isinstance(x, str) else 0).mean()
    print("Average number of moves per game:", average_turns)
    return average_turns

def plot_game_length_distribution(df):
    """
    Plots the distribution of game lengths (number of moves).
    """
    game_lengths = df['Moves'].apply(lambda x: len(x.split()) if isinstance(x, str) else 0)
    plt.figure(figsize=(10, 6))
    plt.hist(game_lengths, bins=range(0, 230, 4), edgecolor='black')
    plt.title('Distribution of Game Lengths')
    plt.xlabel('Number of Moves')
    plt.ylabel('Number of Games')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()  # Ensures the plot is displayed

def plot_eco_category_distribution(df):
    """
    Plots the distribution of game lengths by ECO category (A, B, C, D, E).
    """
    eco_filtered_data = df[df['ECO_Code'].str.startswith(('A', 'B', 'C', 'D', 'E'), na=False)]
    plt.figure(figsize=(14, 10))
    for i, eco in enumerate(['A', 'B', 'C', 'D', 'E'], 1):
        plt.subplot(3, 2, i)
        sns.histplot(
            eco_filtered_data[eco_filtered_data['ECO_Code'].str.startswith(eco)]['Moves']
            .apply(lambda x: len(x.split()) if isinstance(x, str) else 0),
            bins=range(0, 230, 4), edgecolor='black'
        )
        plt.title(f'Distribution of Game Lengths - ECO {eco}')
        plt.xlabel('Number of Moves')
        plt.ylabel('Number of Games')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()  # Ensures all subplots are displayed

def plot_games_per_player(df):
    """
    Plots the number of games each top player has played as White and Black.
    """
    white_games = df['White'].dropna().astype(str).value_counts().reset_index()
    white_games.columns = ['Player', 'White Games']
    black_games = df['Black'].dropna().astype(str).value_counts().reset_index()
    black_games.columns = ['Player', 'Black Games']
    games_per_player = pd.merge(white_games, black_games, on='Player', how='outer').fillna(0)
    games_per_player['White Games'] = games_per_player['White Games'].astype(int)
    games_per_player['Black Games'] = games_per_player['Black Games'].astype(int)
    games_per_player['Total Games'] = games_per_player['White Games'] + games_per_player['Black Games']
    top_players = games_per_player.nlargest(20, 'Total Games')
    top_players_melted = top_players.melt(id_vars='Player', value_vars=['White Games', 'Black Games'],
                                          var_name='Game Type', value_name='Number of Games')
    
    plt.figure(figsize=(16, 8))  # Increase figure size for better readability
    sns.barplot(data=top_players_melted, x='Player', y='Number of Games', hue='Game Type')
    plt.title('Number of Games per Top 20 Players (White and Black)')
    plt.xlabel('Player')
    plt.ylabel('Number of Games')
    plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate labels and adjust font size and alignment
    plt.legend(title='Game Type')
    plt.tight_layout()  # Adjust layout to make sure everything fits within the figure area
    plt.show()


# Run the statistics functions
calculate_average_moves(df_view)                # Prints the average moves
plot_game_length_distribution(df_view)          # Displays game length distribution
plot_eco_category_distribution(df_view)         # Displays ECO category distribution
plot_games_per_player(df_view)                  # Displays games per player distribution