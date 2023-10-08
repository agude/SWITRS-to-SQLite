ATTACH DATABASE "20160924-S2Sv4.1.2-switrs.sqlite3" AS db16;
ATTACH DATABASE "20170112-S2Sv4.1.2-switrs.sqlite3" AS db17;
ATTACH DATABASE "20180925-S2Sv4.1.2-switrs.sqlite3" AS db18;
ATTACH DATABASE "20201024-S2Sv4.1.2-switrs.sqlite3" AS db20;
ATTACH DATABASE "20210604-S2Sv4.1.2-switrs.sqlite3" AS db21;
ATTACH DATABASE "20231008-S2Sv4.1.2-switrs.sqlite3" AS db23;
ATTACH DATABASE "/tmp/output.sqlite" AS outputdb;

-- Select all from the newest database
CREATE TABLE outputdb.case_ids AS
SELECT case_id, '2023' AS db_year
FROM db23.collisions;

-- Now add the rows that don't match from earlier databases, in
-- reverse chronological order so that the newer rows are not
-- overwritten.
INSERT INTO outputdb.case_ids
SELECT * FROM (
    SELECT older.case_id, '2021'
    FROM db21.collisions AS older
    LEFT JOIN outputdb.case_ids AS prime
    ON prime.case_id = older.case_id
    WHERE prime.case_id IS NULL
);

INSERT INTO outputdb.case_ids
SELECT * FROM (
    SELECT older.case_id, '2020'
    FROM db20.collisions AS older
    LEFT JOIN outputdb.case_ids AS prime
    ON prime.case_id = older.case_id
    WHERE prime.case_id IS NULL
);

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
FROM db23.collisions;

INSERT INTO outputdb.collisions
SELECT * FROM (
    SELECT col.*
    FROM db21.collisions AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2021'
);

INSERT INTO outputdb.collisions
SELECT * FROM (
    SELECT col.*
    FROM db20.collisions AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2020'
);

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

-- Create the victims table
CREATE TABLE outputdb.victims AS
SELECT *
FROM db23.victims;

INSERT INTO outputdb.victims
SELECT * FROM (
    SELECT col.*
    FROM db21.victims AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2021'
);

INSERT INTO outputdb.victims
SELECT * FROM (
    SELECT col.*
    FROM db20.victims AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2020'
);

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
FROM db23.parties;

INSERT INTO outputdb.parties
SELECT * FROM (
    SELECT col.*
    FROM db21.parties AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2021'
);

INSERT INTO outputdb.parties
SELECT * FROM (
    SELECT col.*
    FROM db20.parties AS col
    INNER JOIN outputdb.case_ids AS ids
    ON ids.case_id = col.case_id
    WHERE ids.db_year = '2020'
);

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
