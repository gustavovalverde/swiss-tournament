/* Table definitions for the tournament project.*/

CREATE TABLE tournament (
    PRIMARY KEY (game_id),
    game_id   SERIAL,
    name      VARCHAR(50)    NOT NULL
);

CREATE TABLE player (
    PRIMARY KEY (player_id),
    player_id INTEGER,
    full_name VARCHAR(80)    NOT NULL
);

CREATE TABLE match (
    PRIMARY KEY (match_id),
    match_id  SERIAL,
    winner    INTEGER REFERENCES player(player_id),
    loser     INTEGER REFERENCES player(player_id),
    draw      BOOLEAN DEFAULT 'FALSE'         NOT NULL,
    game_id   INTEGER REFERENCES tournament   NOT NULL
);

CREATE TABLE scoreboard (
    PRIMARY KEY (score),
    full_name VARCHAR(80) REFERENCES player     NOT NULL,
    score     INTEGER     DEFAULT 0             NOT NULL,
    player_id INTEGER     REFERENCES player     NOT NULL,
    game_id   INTEGER     REFERENCES tournament NOT NULL,
);
