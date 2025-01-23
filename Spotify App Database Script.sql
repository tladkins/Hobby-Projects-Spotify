-- --------------------------------------------------------------------------------
-- Name: Tanner Adkins
-- Abstract: Database to hold all of the songs I listen to on spotify
-- --------------------------------------------------------------------------------

-- --------------------------------------------------------------------------------
-- Options
-- --------------------------------------------------------------------------------
USE dbSpotifyData;   -- Get out of the master database
SET NOCOUNT ON;		-- Report only errors

IF OBJECT_ID( 'TSongs')							IS NOT NULL DROP TABLE TSongs

CREATE TABLE TSongs
(
	 intSongID							INTEGER			NOT NULL
	,strSongName						VARCHAR(255)	NOT NULL
	,strArtist							VARCHAR(255)	NOT NULL	
	,dtmListenedDate					Date			NOT NULL
	,CONSTRAINT TEvents_PK PRIMARY KEY ( intSongID )
)

--Test
--SELECT *
--From TSongs

