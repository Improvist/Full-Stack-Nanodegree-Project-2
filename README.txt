AUTHOR:	Ryan Chrisco
FILES: tournament.sql, tournament.py, tournament_test.py
DESCRIPTION: Stores players in a database along with wins and losses and
	     allows matching (via swiss pairing) of players and reporting
	     of match results
DIRECTIONS: Install Postgres SQL 9.3.6
	    Create a database named "tournament" in Postgres by issuing the
		command "createdb tournament" from the shell
	    Run "psql" from the shell, ensuring Postgres SQL is on your PATH
	    While in the Postgres interpreter, run the command "\c tournament"
		to connect to the tournament database. Then run the command 
		"\i tournament.sql" to create the necessary database objects.
	    Install Python 2.7.6
	    Run "python tournament_test.py" from the shell
	    Watch all tests succeed!
NOTES: 
