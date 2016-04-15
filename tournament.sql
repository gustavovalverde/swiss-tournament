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
    game_id   VARCHAR(50) NOT NULL
);

CREATE TABLE player (
    PRIMARY KEY (player_id),
    player_id   SERIAL,
    full_name   VARCHAR(80)                                NOT NULL,
    signed_on   VARCHAR(50) REFERENCES tournament(game_id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE match (
    PRIMARY KEY (match_id),
    match_id  SERIAL,
    winner    INTEGER REFERENCES player(player_id) ON DELETE CASCADE NOT NULL,
    loser     INTEGER REFERENCES player(player_id) ON DELETE CASCADE NOT NULL,
    draw      BOOLEAN DEFAULT 'FALSE'       NOT NULL
);

CREATE VIEW p_wins AS
    SELECT player_id, full_name, COUNT(winner) AS wins
      FROM player
 LEFT JOIN match ON player_id = winner
  GROUP BY player_id
;

CREATE VIEW p_losses AS
    SELECT player_id, full_name, COUNT(loser) AS losses
      FROM player
 LEFT JOIN match ON player_id = loser
  GROUP BY player_id
;

CREATE VIEW standings AS
    SELECT p_wins.player_id, p_wins.full_name, p_wins.wins,
    (p_wins.wins + p_losses.losses) AS matches
      FROM p_wins
      JOIN p_losses ON p_wins.player_id = p_losses.player_id
      ORDER BY wins DESC
;
