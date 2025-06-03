CREATE MATERIALIZED VIEW IF NOT EXISTS kpis_by_kpi_name AS
SELECT kpi_name, timestamp, id, value, tags
FROM kpis
WHERE kpi_name IS NOT NULL AND timestamp IS NOT NULL AND id IS NOT NULL
PRIMARY KEY (kpi_name, timestamp, id);

