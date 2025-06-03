-- Create a keyspace
CREATE KEYSPACE IF NOT EXISTS testdb WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };

USE testdb;

-- Create a table users
create table users
(
    email    text primary key,
    name     text,
    password text
);

INSERT INTO testdb.users (email, name, password) VALUES ('tokernel@example.com', 'Test User', '$2b$12$xSDyFGOXw009/Ckj0cwW8uz7tDZOvrONCp82ZkRFSVoR40GZpr8bS');

CREATE TABLE IF NOT EXISTS kpis (
    id UUID,
    timestamp TIMESTAMP,
    kpi_name TEXT,
    value DOUBLE,
    tags SET<TEXT>,
    PRIMARY KEY ((id), kpi_name, timestamp)
);

CREATE TABLE IF NOT EXISTS kpis (
    timestamp TIMESTAMP,
    kpi_name TEXT,
    value DOUBLE,
    tags TEXT,
    PRIMARY KEY (kpi_name, timestamp)
);

CREATE MATERIALIZED VIEW IF NOT EXISTS kpis_by_kpi_name_and_timestamp AS
SELECT id, timestamp, kpi_name, value, tags
FROM kpis2
WHERE kpi_name IS NOT NULL AND timestamp IS NOT NULL AND id IS NOT NULL
PRIMARY KEY ((kpi_name), timestamp, id);