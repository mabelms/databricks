-- Databricks notebook source
CREATE TABLE employee(
  id int, name STRING, salary DOUBLE
)

-- COMMAND ----------

INSERT INTO employee
(1, "Adam", 3500),
(2, "Sarah", 2500),
(3, "John", 2999.3),
(4, "Thomas", 4000,3),
(5, "Anna", 6200.3),
(6, "Kim", 6200.3)

-- COMMAND ----------

DESCRIBE employee