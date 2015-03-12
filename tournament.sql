-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE SEQUENCE player_numerator; --controls player IDs; ensures unique IDs

CREATE TABLE players (name text, --core table for registered players
		      player_id bigint,
		      wins int,
		      losses int);

