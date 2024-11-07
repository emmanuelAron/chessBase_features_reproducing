import pandas as pd
import mysql.connector
import numpy as np

# Load the CSV file into a DataFrame
data = pd.read_csv('games_1990_.csv')

data = data.replace({np.nan: None})

# Establish connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="emma",
    database="chessdb"
)
cursor = conn.cursor()

# Loop through each row in the DataFrame and update the Moves column in GAMES_1990
for _, row in data.iterrows():
    # Skip rows with missing essential information for matching
    if row['White'] is None or row['Black'] is None or row['Date'] is None:
        continue

    cursor.execute("""
        UPDATE GAMES_1990
        SET Moves = %s
        WHERE White = %s AND Black = %s AND Date = %s
    """, (row['Moves'], row['White'], row['Black'], row['Date']))

# Commit the changes to the database and close the connection
conn.commit()
cursor.close()
conn.close()