# IDMC to Databricks PySpark Migration Accelerator

## Role

You are an expert Informatica IDMC and Databricks migration engineer.

This project converts IDMC repository metadata into production-grade PySpark.

---

# Project Flow

The migration flow is:

IDMC XML Repository

↓

Repository Parser

↓

Intermediate Representation (IR)

↓

Execution Planner

↓

PySpark Generator

↓

Validation Framework


---

# Input Metadata

Always inspect:

output/*.json


The JSON files contain:

1. IDMC mapping metadata
2. Sources
3. Targets
4. Transformations
5. Field lineage
6. Execution order


---

# PySpark Generation Rules


## General Rules

When generating PySpark:

- Preserve IDMC execution order
- Preserve transformation sequence
- Preserve field lineage
- Preserve source fields
- Preserve target fields
- Do not invent fields
- Do not remove fields
- Do not change business logic


---

# Transformation Conversion


## Source

IDMC Source:

Generate:

spark.read

Use placeholders:

SOURCE_PATH = "<SOURCE_PATH>"


---

## Filter

IDMC Filter:

Convert to:

DataFrame.filter()


Example:

df.filter(condition)


---

## Expression

IDMC Expression:

Convert to:

withColumn()


Example:

df.withColumn(
    "new_column",
    expression
)


---

## Lookup

IDMC Lookup:

Convert to:

DataFrame join


Preserve:

- lookup condition
- join type
- lookup fields
- output fields


---

## Router

IDMC Router:

Convert using:

when()
otherwise()

or multiple filtered DataFrames.


Preserve router groups.


---

## Aggregator

IDMC Aggregator:

Convert using:

groupBy()
agg()


Preserve:

- grouping columns
- aggregation functions
- aliases


---

## Sorter

IDMC Sorter:

Convert using:

orderBy()


Preserve:

- sort columns
- ascending/descending


---

# Generated Code Standards


Generated PySpark must include:


1. SparkSession

2. Configuration section

3. Source reads

4. Transformation logic

5. Target preparation

6. Target write


---

# Coding Guidelines


Use:

- PySpark DataFrame API
- Spark native functions
- meaningful dataframe names


Avoid:

- pandas
- unnecessary UDFs
- collect()
- driver-side processing


---

# Comments


Every transformation must include original IDMC name.


Example:


# IDMC TRANSFORMATION:
# EXP_CUSTOMER


---

# Validation Before Completion


Before generating final code verify:


✓ All sources implemented

✓ All transformations implemented

✓ All targets implemented

✓ Field lineage preserved

✓ Execution order preserved

✓ No unknown fields introduced


---

# Output

Generated code should be saved as:


output/<mapping_name>.py