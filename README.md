# chessBase features reproducing  <br>

![Distribution of game lengths](tableau%20graphs/Distribution_of_game_lengths.png) <br>
![Distribution of game results per color](tableau%20graphs/Distribution_of_game_results_by_color.jpg) <br>
![Distribution of game results for each ECO code](stats_screenshot_lichess1.png) <br>

SQL script <br>
```sql
USE chessdb;
CREATE TABLE ECO_CODES(
	ECO_Code VARCHAR(5),
    Opening VARCHAR(40),
    Moves VARCHAR(200 )
);
COMMIT;
ALTER TABLE ECO_CODES
ADD COLUMN ECO_ID INT AUTO_INCREMENT PRIMARY KEY;commit;

DROP TABLE GAMES_1990; COMMIT;

CREATE TABLE GAMES_1990(
    id INT PRIMARY KEY AUTO_INCREMENT,
    White VARCHAR(50),
    Black VARCHAR(50),
    Result VARCHAR(7),
    Event VARCHAR(50),
    Date DATE
);commit;

# MOVES_1990_ underscore table
CREATE TABLE MOVES_1990_(
    game_id INT,
    Moves VARCHAR(3000),
    FOREIGN KEY (game_id) REFERENCES GAMES_1990(id)
);commit;


SELECT * FROM ECO_CODES;
COMMIT;
show tables;
SELECT * FROM games_1990;
COMMIT;
SELECT * FROM moves_1990_;
COMMIT;

ALTER TABLE GAMES_1990
ADD COLUMN Moves VARCHAR(3000);

UPDATE GAMES_1990 AS G
JOIN TEMP_MOVES AS T ON G.White = T.White AND G.Black = T.Black AND G.Date = T.Date
SET G.Moves = T.Moves
WHERE G.id IS NOT NULL;

DELETE
FROM games_1990
WHERE id IS NULL;
commit;


SELECT COUNT(*)
FROM games_1990
WHERE id IS NULL;

SET SQL_SAFE_UPDATES = 0;

DELETE FROM games_1990 WHERE White IS NULL AND Black IS NULL AND Result IS NULL
AND Event IS NULL AND Date IS NULL AND Moves IS NOT NULL; commit;

SELECT *
FROM ECO_CODES;

# Replace the apostrophe with a space in ECO_CODES table
UPDATE ECO_CODES
SET Opening = REPLACE(Opening, 'â€™', ' ')
WHERE Opening LIKE '%â€™%';commit;

# Link table between games_1990 and ECO_CODES via ECO_code and game_id, as the two tables had no common columns.
# (Following a normal form process, with the usage of foreign keys, and not adding an ECO_Code column
# directly to the games_1990 table,which would mix the datas ).
CREATE TABLE game_opening_map (
    game_id INT,
    ECO_Code VARCHAR(10),
    PRIMARY KEY (game_id, ECO_Code),
    FOREIGN KEY (game_id) REFERENCES games_1990(id),
    FOREIGN KEY (ECO_Code) REFERENCES ECO_CODES(ECO_Code)
);commit;

CREATE TABLE game_opening_map (
    game_id INT,
    ECO_ID INT,
    PRIMARY KEY (game_id, ECO_ID),
    FOREIGN KEY (game_id) REFERENCES games_1990(id),
    FOREIGN KEY (ECO_ID) REFERENCES ECO_CODES(ECO_ID)
);commit;
# Populate the linking table with corresponding IDs
INSERT INTO game_opening_map (game_id, ECO_ID)
SELECT g.id, e.ECO_ID
FROM games_1990 g
JOIN ECO_CODES e
ON g.Moves LIKE CONCAT(e.Moves, '%');commit;

select *
from game_opening_map;

SELECT g.id, g.White, g.Black, g.Result, g.Event, g.Date, g.Moves, m.ECO_ID, e.ECO_Code, e.Opening
FROM games_1990 g
JOIN game_opening_map m ON g.id = m.game_id
JOIN ECO_CODES e ON m.ECO_ID = e.ECO_ID;commit;

# VIEW CREATION AS THIS REQUEST IS A RESULT COMPUTATION (continuing the normalized form process)
CREATE VIEW game_opening_details AS
SELECT g.id, g.White, g.Black, g.Result, g.Event, g.Date, g.Moves, m.ECO_ID, e.ECO_Code, e.Opening
FROM games_1990 g
JOIN game_opening_map m ON g.id = m.game_id
JOIN ECO_CODES e ON m.ECO_ID = e.ECO_ID;COMMIT;

SELECT * FROM game_opening_details;commit;

# Adding two more columns for adding ratings(ELO) white and black
ALTER TABLE games_1990
ADD COLUMN white_rating INT,
ADD COLUMN black_rating INT;
COMMIT;

# Temp table for import 
CREATE TABLE temp_elo_data (
    id INT,
    White VARCHAR(50),
    Black VARCHAR(50),
    Date DATE,
    white_rating INT,
    black_rating INT
);
COMMIT;

SELECT * FROM temp_elo_data;

SET SQL_SAFE_UPDATES = 0;

#CREATE INDEX idx_games_white_black_date ON games_1990 (White, Black, Date);
#CREATE INDEX idx_temp_elo_white_black_date ON temp_elo_data (White, Black, Date);

SET GLOBAL connect_timeout = 1200;
SET GLOBAL wait_timeout = 1200;
SET GLOBAL interactive_timeout = 1200;

CREATE INDEX idx_temp_elo_white ON temp_elo_data (White);
CREATE INDEX idx_temp_elo_black ON temp_elo_data (Black);
CREATE INDEX idx_temp_elo_date ON temp_elo_data (Date);

UPDATE games_1990 AS g
JOIN temp_elo_data AS t
ON g.White = t.White AND g.Black = t.Black AND g.Date = t.Date
SET g.white_rating = t.white_rating,
    g.black_rating = t.black_rating;
COMMIT;

``` 

## Filtering work: <br>
```python
# After inspecting the result, i will try to remove rows that doesn’t start with « 1. » 
# Problem : it doesnt appear in my DataFrame but it appears in my LibreOffice file...So if it 
# is not deleted in the table i will try to remove it with SQL.
 # Step 1: Remove any extraneous whitespace and hidden characters from 'Moves' column
df['Moves'] = df['Moves'].str.strip()

# Step 2: Filter rows to keep only those starting with "1." in the 'Moves' column
df_filtered = df[df['Moves'].str.match(r'^1\.\s', na=False)]

# Display the filtered DataFrame
display(df_filtered)
# Conversion to csv:
df.to_csv("ECO_code_mapping.csv")
```
## Machine Learning data preparation (focus on numerics columns)
```python
	Result	Moves	white_rating	black_rating
12	1-0	1. e4 c6 2. d4 d5 3. Nd2 dxe4 4. Nxe4 Nf6 5. N...	2285.0	2405.0
13	0-1	1. e4 e5 2. Nf3 Nc6 3. Bb5 f5 4. Nc3 Nd4 5. Nx...	2285.0	2405.0
14	0-1	1. a4	2285.0	2405.0
15	0-1	1. e4 e5 2. Nf3 Nc6 3. Bb5 Nf6 4. d3 Nd4 5. Nx...	2285.0	2405.0
22	1/2-1/2	1. c4 f5 2. g3 Nf6 3. Bg2 g6 4. Nc3 Bg7 5. e3 ...	2275.0	2255.0
23	1-0	1. c4 e5 2. Nc3 d6 3. g3 f5 4. Bg2 Nf6 5. e3 B...	2275.0	2255.0
24	1/2-1/2	1. c4 Nf6 2. Nc3 e6 3. Nf3 c5 4. g3 Nc6 5. Bg2...	2275.0	2255.0
31	1-0	1. Nf3 Nc6 2. d4 d5 3. c4 Bg4 4. Nc3 dxc4 5. d...	2335.0	2365.0
32	1-0	1. e4 c5 2. Nf3 Nc6 3. d4 cxd4 4. Nxd4 Qb6 5. ...	2335.0	2365.0
33	1/2-1/2	1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-...	2335.0	2365.0
64	0-1	1. Nf3 d5 2. d4 Bg4 3. e3 e6 4. Be2 Nd7 5. O-O...	2245.0	2340.0
65	1/2-1/2	1. d4 Nf6 2. c4 g6 3. Nc3 Bg7 4. e4 d6 5. f3 O...	2245.0	2340.0
75	0-1	1. c4 Nc6 2. Nc3 e5 3. g3 d6 4. Bg2 Be6 5. d3 ...	2315.0	2235.0
76	1/2-1/2	1. c4 c6 2. e4 d5 3. exd5 cxd5 4. cxd5 Nf6 5. ...	2315.0	2235.0
77	1/2-1/2	1. c4 Nf6 2. Nf3 g6 3. Nc3 c5 4. g3 Bg7 5. Bg2...	2315.0	2235.0
78	1-0	1. e4 e5 2. Nf3 Nc6 3. Bb5 f5 4. d3 fxe4 5. dx...	2315.0	2315.0
79	0-1	1. e4 e5 2. Nf3 Nc6 3. Bb5 Nf6 4. O-O Bc5 5. N...	2315.0	2315.0
80	1-0	1. e4 e6 2. d4 d5 3. Nc3 Bb4 4. e5 b6 5. Bd2 Q...	2315.0	2315.0
81	1/2-1/2	1. d4 e6 2. c4 f5 3. Nc3 Nf6 4. Bf4 Bb4 5. Qb3...	2290.0	2305.0
82	1/2-1/2	1. d4 Nf6 2. c4 d6 3. Nc3 Bf5 4. Bg5 Nbd7 5. f...	2290.0	2305.0
16535
# We add the 'target' column , and remove the 'Result' column :
df_clean['target'] = df_clean['Result'].apply(lambda x: 1 if x == '1-0' else (0 if x == '1/2-1/2' else -1))
df_clean = df_clean.drop(columns=['Result'])

```

Exploration of Cairo open-source python library , with svg and matplotlib <br>
```python
# Install necessary libraries
!pip install python-chess cairosvg

# Import libraries
import chess
import chess.svg
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import cairosvg

# Create the chess board
board = chess.Board()

# Add moves
moves = ["d4", "d5", "c4", "e6"]
for move in moves:
    board.push_san(move)

# Convert the position to SVG and then to PNG using cairosvg
try:
    # Generate the SVG image
    svg_image = chess.svg.board(board=board)
    
    # Convert the SVG image to PNG
    png_image = BytesIO()
    cairosvg.svg2png(bytestring=svg_image.encode('utf-8'), write_to=png_image)
    
    # Load the PNG image with PIL
    png_image.seek(0)
    image = Image.open(png_image)

    # Display the image with Matplotlib
    plt.figure(figsize=(6, 6))
    plt.imshow(image)
    plt.axis('off')  # Hide the axis
    plt.show()

except OSError as e:
    print("Error: The 'cairo' library is required to use cairosvg.")
    print("Make sure 'libcairo' is installed and accessible in the PATH.")
    print(e)
except Exception as e:
    print("An error occurred while creating or displaying the image.")
    print(e)
```
Result of my webscraping to csv: <br>

```csv
code,name
A01,Larsen's Opening
A02,Bird's Opening
A03,"Bird's Opening, 1...d5"
A04,Zukertort Opening
A05,"Zukertort Opening, 2...Nf6"
A06,Réti Opening
A07,King's Indian attack (Barcza system)
A08,"King's Indian Attack, 3. Bg2"
A09,"Réti Opening, without: 2...c6, 2...e6"
A10,English Opening
A11,"English, Caro-Kann defensive system"
A12,"English, Caro-Kann defensive system"
A13,English Opening
A14,"English, Neo-Catalan declined"
A15,"English, 1...Nf6 (Anglo-Indian defense)"
A16,English Opening
A17,"English Opening, Hedgehog Defense"
A18,"English, Mikenas-Carls variation"
A19,"English, Mikenas-Carls, Sicilian variation"
```

