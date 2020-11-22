AwTACH DATABASE "20201024-3.0.1-switrs.sqlite" AS db20;
ATTACH DATABASE "20180925-3.0.1-switrs.sqlite" AS db18;
ATTACH DATABASE "20170112-3.0.1-switrs.sqlite" AS db17;
ATTACH DATABASE "20160924-3.0.1-switrs.sqlite" AS db16;
ATTACH DATABASE "/tmp/output.sqlite" AS outputdb;

-- Select all from 2020
CREATE TABLE outputdb.case_ids AS
SELECT case_id, '2020' AS db_year
FROM db20.collisions;

-- Now add the rows that don't match from earlier databases, in
-- reverse chronological order so that the newer rows are not
-- overwritten.
INSERT INTO outputdb.case_ids
SELECT * FROM (
    SELECT older.case_id, '2018'
    FROM db18.collisions AS older
    LEFT JOIN outputdb.case_ids AS prime
    ON prime.case_id = older.case_id
    WHERE prime.case_id IS NULL
);

INSERT INTO outputdb.case_ids
SELECT * FROM (
    SELECT older.case_id, '2017'
    FROM db17.collisions AS older
    LEFT JOIN outputdb.case_ids AS prime
    ON prime.case_id = older.case_id
    WHERE prime.case_id IS NULL
);

INSERT INTO outputdb.case_ids
SELECT * FROM (
    SELECT older.case_id, '2016'
    FROM db16.collisions AS older
    LEFT JOIN outputdb.case_ids AS prime
    ON prime.case_id = older.case_id
    WHERE prime.case_id IS NULL
);

SELECT db_year, COUNT(1)
FROM outputdb.case_ids
GROUP BY db_year;

-- Create the combined collision table

CREATE TABLE outputdb.collisions AS
SELECT *
FROM db20.collisions;

INSERT INTO outputdb.collisions
SELECT * FROM (
    SELECT col.*
    FROM db18.collisions AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2018'
);

INSERT INTO outputdb.collisions
SELECT * FROM (
    SELECT col.*
    FROM db17.collisions AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2017'
);

INSERT INTO outputdb.collisions
SELECT * FROM (
    SELECT col.*
    FROM db16.collisions AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2016'
);

-- Create the party table
CREATE TABLE outputdb.victims AS
SELECT *
FROM db20.victims;

INSERT INTO outputdb.victims
SELECT * FROM (
    SELECT col.*
    FROM db18.victims AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2018'
);

INSERT INTO outputdb.victims
SELECT * FROM (
    SELECT col.*
    FROM db17.victims AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2017'
);

INSERT INTO outputdb.victims
SELECT * FROM (
    SELECT col.*
    FROM db16.victims AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2016'
);

-- Create the party table
CREATE TABLE outputdb.parties AS
SELECT *
FROM db20.parties;

INSERT INTO outputdb.parties
SELECT * FROM (
    SELECT col.*
    FROM db18.parties AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2018'
);

INSERT INTO outputdb.parties
SELECT * FROM (
    SELECT col.*
    FROM db17.parties AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2017'
);

INSERT INTO outputdb.parties
SELECT * FROM (
    SELECT col.*
    FROM db16.parties AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2016'
);
