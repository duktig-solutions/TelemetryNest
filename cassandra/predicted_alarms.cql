-- Use the keyspace
USE testdb;

-- Create the main table
CREATE TABLE predicted_alarms (
  operator_id INT,
  date_prediction TIMESTAMP,
  alert_sign TEXT,
  element_id INT,
  fault_description TEXT,
  fault_id INT,
  fault_name TEXT,
  object TEXT,
  probability FLOAT,
  severity TEXT,
  PRIMARY KEY ((operator_id), date_prediction)
);

-- Materialized view for querying by operator_id and element_id
CREATE MATERIALIZED VIEW predicted_alarms_by_element_id AS
SELECT operator_id, date_prediction, alert_sign, element_id, fault_description, fault_id, fault_name, object, probability, severity
FROM predicted_alarms
WHERE operator_id IS NOT NULL AND element_id IS NOT NULL AND date_prediction IS NOT NULL
PRIMARY KEY (operator_id, element_id, date_prediction);

-- Materialized view for querying by operator_id and date_prediction
CREATE MATERIALIZED VIEW predicted_alarms_by_date_prediction AS
SELECT operator_id, date_prediction, alert_sign, element_id, fault_description, fault_id, fault_name, object, probability, severity
FROM predicted_alarms
WHERE operator_id IS NOT NULL AND date_prediction IS NOT NULL
PRIMARY KEY (operator_id, date_prediction);

-- Materialized view for querying by operator_id only
CREATE MATERIALIZED VIEW predicted_alarms_by_operator AS
SELECT operator_id, date_prediction, alert_sign, element_id, fault_description, fault_id, fault_name, object, probability, severity
FROM predicted_alarms
WHERE operator_id IS NOT NULL AND date_prediction IS NOT NULL
PRIMARY KEY (operator_id, date_prediction);

-- Materialized view for querying by date_prediction only
CREATE MATERIALIZED VIEW predicted_alarms_by_date AS
SELECT operator_id, date_prediction, alert_sign, element_id, fault_description, fault_id, fault_name, object, probability, severity
FROM predicted_alarms
WHERE date_prediction IS NOT NULL and operator_id IS NOT NULL
PRIMARY KEY (date_prediction, operator_id);
