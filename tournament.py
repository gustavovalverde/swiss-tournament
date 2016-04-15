#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteTournaments():
    """Remove all the match records from the database."""
    DB = connect()
    cur = DB.cursor()
    cur.execute("DELETE FROM tournament;")
    DB.commit()
    DB.close()


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cur = DB.cursor()
    cur.execute("DELETE FROM match;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cur = DB.cursor()
    cur.execute("DELETE FROM player;")
    DB.commit()
    DB.close()

def createTournament(name):
    """Create a new tournament.
    Args:
        name: the tournament's unique identifier
    """
    DB = connect()
    cur = DB.cursor()
    insert_t = "INSERT INTO tournament (game_id) VALUES (%s) RETURNING game_id"
    cur.execute(insert_t, (name,))
    tournament_id = cur.fetchone()[0]
    DB.commit()
    DB.close()
    return tournament_id


def countPlayers(tournament_id):
    """Returns the number of players currently registered in a tournament."""
    DB = connect()
    cur = DB.cursor()
    select_p = """SELECT COUNT(*)
                    FROM player
                   WHERE signed_on = (%s);"""
    cur.execute(select_p, (tournament_id,))
    qty_players = cur.fetchone()[0]
    DB.close()
    return qty_players


def registerPlayer(name, tournament_id):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cur = DB.cursor()
    insert_p = "INSERT INTO player (full_name, signed_on) VALUES (%s, %s);"
    cur.execute(insert_p, (name, tournament_id,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute("SELECT * FROM standings;")
    standings = cur.fetchall()
    DB.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cur = DB.cursor()
    # cur.execute("SELECT matches FROM standings WHERE matches = 0")
    standings = playerStandings()
    print standings
    i_match = "INSERT INTO match (winner, loser) VALUES (%s, %s);"
    # s_matches = cur.fetchall()
    # print s_matches
    for counter, each_player in enumerate(standings):
        if standings[counter][3] == 0:
            print "--- BEFORE Execute ---"
            cur.execute("SELECT * FROM match")
            print cur.fetchone()
            print "Execution"
            cur.execute(i_match, (winner, loser,))
            print "---"
            print "--- AFTER Execute ---"
            cur.execute("SELECT * FROM match")
            print cur.fetchone()
    # cur.execute("UPDATE match SET winner = %s;", (winner,))
    # cur.execute("UPDATE match SET loser = %s;", (loser,))
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
