#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

from contextlib import contextmanager
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")
    except:
        print "Connection failed"


@contextmanager
def get_cursor():
    """
    Query helper function using context lib. Creates a cursor from a database
    connection object, and performs queries using that cursor.
    """
    DB = connect()
    cursor = DB.cursor()
    try:
        yield cursor
    except:
        raise
    else:
        DB.commit()
    finally:
        cursor.close()
        DB.close()


def deleteTournaments():
    """Remove all the match records from the database."""
    with get_cursor() as cursor:
        cursor.execute("DELETE FROM tournament;")


def deleteMatches():
    """Remove all the match records from the database."""
    with get_cursor() as cursor:
        cursor.execute("DELETE FROM match;")


def deletePlayers():
    """Remove all the player records from the database."""
    with get_cursor() as cursor:
        cursor.execute("DELETE FROM player;")


def createTournament(name):
    """Create a new tournament.
    Args:
        name: the tournament's unique identifier
    """
    insert_t = "INSERT INTO tournament (game_id) VALUES (%s) RETURNING game_id"
    with get_cursor() as cursor:
        cursor.execute(insert_t, (name,))
        tournament_id = cursor.fetchone()[0]
    return tournament_id


def countPlayers(tournament_id):
    """Returns the number of players currently registered in a tournament."""
    select_p = """SELECT COUNT(*)
                    FROM player
                   WHERE signed_on = (%s);"""
    with get_cursor() as cursor:
        cursor.execute(select_p, (tournament_id,))
        qty_players = cursor.fetchone()[0]
    return qty_players


def registerPlayer(name, tournament_id):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    insert_p = "INSERT INTO player (full_name, signed_on) VALUES (%s, %s);"
    with get_cursor() as cursor:
        cursor.execute(insert_p, (name, tournament_id,))


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
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM standings;")
        t_standings = cursor.fetchall()
    return t_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    i_match = "INSERT INTO match (winner, loser) VALUES (%s, %s);"
    with get_cursor() as cursor:
        cursor.execute(i_match, (winner, loser,))


def invalidMatch(player1, player2):  # Function defined, but not being used.
    """Verify if a match is not valid between two players. This is True if a
    match has already been played between two players.

    Args:
      winner:  the id number of the player who won a match
      loser:  the id number of the player who lost a match

    Returns:
      True if a match has already been played by the players
      False if a match has not been played by the  players
    """
    invalid_match = """SELECT EXISTS (
                     SELECT 1
                       FROM match
                      WHERE winner = %s and loser = %s
                      );"""
    with get_cursor() as cursor:
        a_rematch = cursor.execute(invalid_match, (player1, player2,))
    return a_rematch


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
    with get_cursor() as cursor:
        cursor.execute("SELECT player_id, full_name FROM standings;")
        standings = cursor.fetchall()
        pairings = []
        # if len(pairings) % 2 != 0:
        # Code for handling odd number of players. Coming soon.

        # Using list comprehension for shorter code.
        pairings = [(standings[i] + standings[i+1])
                    if not invalidMatch(standings[i][0], standings[i+1][0])
                    # I'm not confident with this else statement, even though
                    # all tests pass. Need to do more tests.
                    else standings[i] + standings[i+2]
                    for i in xrange(0, len(standings), 2)]
    return pairings
