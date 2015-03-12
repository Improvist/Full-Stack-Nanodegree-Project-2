#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    try:
	conn = connect()
	cur = conn.cursor()
	cur.execute("UPDATE players SET wins = 0, losses = 0")
  	conn.commit() # force commit into database
    except:
	print "Failed to deleteMatches()"


def deletePlayers():
    """Remove all the player records from the database."""
    try:
	conn = connect()
	cur = conn.cursor()
	cur.execute("TRUNCATE players") # clears table entirely
	conn.commit()
    except:
	print "Failed to deletePlayers()"


def countPlayers():
    """Returns the number of players currently registered."""
    try:
	conn = connect()
	cur = conn.cursor()
	cur.execute("SELECT COUNT(*) FROM players")
	playerCount = cur.fetchone() # only need the first record
	return playerCount[0]
    except:
	print "Failed to countPlayers()"


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    try:
	conn = connect()
	cur = conn.cursor()
	# parameterized query to protect against SQL attack
	cur.execute("""INSERT INTO players (name, player_id, wins, losses) 
		     VALUES (%s, nextval('player_numerator'), 0, 0)""",
		     (name,))
	conn.commit()
    except:
	print "Failed to registerPlayer()"	


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    try:
	conn = connect()
	cur = conn.cursor()
	# perform sorting in the query to get most-winning players first
	cur.execute("""SELECT name, player_id, wins, losses
		       FROM players
		       ORDER BY wins DESC""")
	resultset = cur.fetchall() # retrieve all records discovered in query
	list_of_players = []
	# iterate over the result set from the query
	for row in resultset:
		list_of_players.append((row[1], 	#player_id
					row[0], 	#name
					row[2], 	#wins
					row[3]+row[2])) #matches
	return list_of_players
    except:
	print "Failed to get playerStandings()"


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    try:
	conn = connect()
	cur = conn.cursor()
	# update the 'players' table to reflect the winner and loser
	cur.execute("""UPDATE players 
		       SET wins = wins + 1
		       WHERE player_id = %s""", (winner,))
	conn.commit()
	cur.execute("""UPDATE players
		       SET losses = losses + 1
		       WHERE player_id = %s""", (loser,)) 
	conn.commit()	
    except:
	print "Failed to reportMatch()" 
 
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
    try:
	conn = connect()
	cur = conn.cursor()
	# retrieve the list of players and order them from most->least wins
	cur.execute("""SELECT name, player_id, wins, losses
		       FROM players
		       ORDER BY wins DESC""")
	rows = cur.fetchall()
	matchups = []
	# iterate over the results by 2, pairing every two up
	for i in range(0,len(rows), 2):
		matchups.append( (rows[i][1], rows[i][0],
				  rows[i+1][1], rows[i+1][0]) )		
	return matchups				
    except:
	print "Fail to swissPairings()"

