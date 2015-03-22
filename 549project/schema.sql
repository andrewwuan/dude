-- To create the database:
--   CREATE DATABASE dude;
--
-- To reload the tables:
--   mysql --user=dude --password=dude--database=dude < schema.sql

SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";

DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    user VARCHAR(20) PRIMARY KEY,
    name VARCHAR(512) NOT NULL,
    value VARCHAR(512) NOT NULL
);

