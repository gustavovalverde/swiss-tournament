/* First thing is to DROP everything that already exists so I can run multiple
tests. */
DROP TABLE IF EXISTS tournament CASCADE;
DROP TABLE IF EXISTS player     CASCADE;
DROP TABLE IF EXISTS match      CASCADE;
DROP VIEW  IF EXISTS standings  CASCADE;

/* With the DATABASE created is time to define all the TABLES for the
tournament project.*/
CREATE TABLE tournament (
    PRIMARY KEY (game_id),
    game_id   VARCHAR(50)
);

CREATE TABLE player (
    PRIMARY KEY (player_id),
    player_id   SERIAL,
    full_name   VARCHAR(80)                                NOT NULL,
    signed_on   VARCHAR(50) REFERENCES tournament(game_id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE match (
    PRIMARY KEY (match_id, game_id),
    match_id  SERIAL,
    winner    INTEGER REFERENCES player(player_id),
    loser     INTEGER REFERENCES player(player_id),
    draw      BOOLEAN DEFAULT 'FALSE'       NOT NULL,
    game_id   TEXT    REFERENCES tournament ON DELETE CASCADE
);

CREATE VIEW standings AS
    SELECT player_id, full_name,
           COUNT(winner) AS wins,
           COUNT(winner) + COUNT(loser) AS matches
      FROM player
 LEFT JOIN match ON player_id = winner
  GROUP BY player_id
  ORDER BY wins DESC
;
