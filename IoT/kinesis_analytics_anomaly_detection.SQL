--Creates a temporary stream.
CREATE OR REPLACE STREAM "TEMP_STREAM" (
	        "FREQ"        INTEGER,
	        "RPM"        INTEGER,
	        "FANID"         varchar(20),
	        "ANOMALY_SCORE"    DOUBLE);

--Creates another stream for application output.	        
CREATE OR REPLACE STREAM "DESTINATION_SQL_STREAM" (
	        "FREQ"        INTEGER,
	        "RPM"        INTEGER,
	        "FANID"         varchar(20),
	        "ANOMALY_SCORE"    DOUBLE);


-- Compute an anomaly score for each record in the input stream
-- using Random Cut Forest
CREATE OR REPLACE PUMP "STREAM_PUMP" AS 
   INSERT INTO "TEMP_STREAM"
      SELECT STREAM "FREQ", "RPM", "FANID", ANOMALY_SCORE 
      FROM TABLE(RANDOM_CUT_FOREST(
              CURSOR(SELECT STREAM * FROM "SOURCE_SQL_STREAM_001")));

CREATE OR REPLACE PUMP "OUTPUT_PUMP" AS 
   INSERT INTO "DESTINATION_SQL_STREAM"
      SELECT STREAM * FROM "TEMP_STREAM"
      -- WHERE ANOMALY_SCORE > 4 -- To keep things simple, define an important anomaly as an item with an ANOMALY_SCORE greater than 4
      ORDER BY FLOOR("TEMP_STREAM".ROWTIME TO SECOND), ANOMALY_SCORE DESC;
