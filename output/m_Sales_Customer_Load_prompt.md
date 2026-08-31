
# IDMC TO PYSPARK GENERATION TASK

You are an expert Informatica IDMC and
Databricks PySpark migration engineer.

Convert the supplied IDMC mapping metadata
into production-quality PySpark code.

IMPORTANT:

- Do not invent metadata.
- Do not invent fields.
- Do not invent transformations.
- Preserve transformation order.
- Preserve field lineage.
- Preserve business logic.

# MAPPING

m_Sales_Customer_Load

# TRANSFORMATION RULES

SOURCE:
Use Spark DataFrame readers.

Use a placeholder:

SOURCE_PATH = "<SOURCE_PATH>"

FILTER:
Convert to DataFrame filter operations.

EXPRESSION:
Convert expressions into withColumn operations.

LOOKUP:
Convert lookup transformations into DataFrame joins.
Preserve lookup conditions and join type.

ROUTER:
Use when/otherwise or filtered DataFrames.
Preserve router conditions.

AGGREGATOR:
Use groupBy and agg.
Preserve grouping and aggregation functions.

SORTER:
Use orderBy.
Preserve sort direction.

TARGET:
Create the final target DataFrame.
Use:

TARGET_PATH = "<TARGET_PATH>"

Do not use real credentials.

# CODE QUALITY

The generated PySpark must:

- use Spark DataFrame APIs
- avoid pandas
- avoid unnecessary UDFs
- handle NULL values
- use meaningful DataFrame names
- use aliases for joins
- preserve IDMC transformation names in comments

For example:

# IDMC TRANSFORMATION: FIL_ACTIVE_CUSTOMER

# REQUIRED STRUCTURE

1. Imports
2. SparkSession
3. Configuration
4. Source reads
5. Transformations in execution order
6. Target preparation
7. Target write
8. Spark shutdown

# VALIDATION

Before producing the code verify:

1. Every source is represented.
2. Every transformation is represented.
3. Every target is represented.
4. Field lineage is respected.
5. Execution order is respected.
6. Target fields are populated.
7. No unknown fields are introduced.

If something cannot be translated exactly,
add a TODO comment rather than inventing behavior.

# IDMC IR

{
  "name": "m_Sales_Customer_Load",
  "description": "Customer enrichment and active-customer load",
  "sources": [
    {
      "name": "SRC_CUSTOMER",
      "type": "DATABASE",
      "fields": [
        {
          "name": "CUSTOMER_ID",
          "datatype": "INTEGER"
        },
        {
          "name": "FIRST_NAME",
          "datatype": "STRING"
        },
        {
          "name": "LAST_NAME",
          "datatype": "STRING"
        },
        {
          "name": "EMAIL",
          "datatype": "STRING"
        },
        {
          "name": "STATUS",
          "datatype": "STRING"
        },
        {
          "name": "COUNTRY_CODE",
          "datatype": "STRING"
        },
        {
          "name": "CUSTOMER_TIER",
          "datatype": "STRING"
        },
        {
          "name": "UPDATED_DATE",
          "datatype": "TIMESTAMP"
        }
      ]
    },
    {
      "name": "SRC_COUNTRY",
      "type": "DATABASE",
      "fields": [
        {
          "name": "COUNTRY_CODE",
          "datatype": "STRING"
        },
        {
          "name": "COUNTRY_NAME",
          "datatype": "STRING"
        },
        {
          "name": "REGION",
          "datatype": "STRING"
        }
      ]
    }
  ],
  "targets": [
    {
      "name": "DIM_CUSTOMER",
      "type": "DELTA",
      "fields": [
        {
          "name": "CUSTOMER_ID",
          "datatype": "INTEGER"
        },
        {
          "name": "CUSTOMER_KEY",
          "datatype": "STRING"
        },
        {
          "name": "FULL_NAME",
          "datatype": "STRING"
        },
        {
          "name": "EMAIL_NORMALIZED",
          "datatype": "STRING"
        },
        {
          "name": "COUNTRY_CODE",
          "datatype": "STRING"
        },
        {
          "name": "COUNTRY_NAME",
          "datatype": "STRING"
        },
        {
          "name": "REGION",
          "datatype": "STRING"
        }
      ]
    },
    {
      "name": "AGG_CUSTOMER_REGION",
      "type": "DELTA",
      "fields": [
        {
          "name": "REGION",
          "datatype": "STRING"
        },
        {
          "name": "CUSTOMER_COUNT",
          "datatype": "LONG"
        },
        {
          "name": "MAX_CUSTOMER_ID",
          "datatype": "INTEGER"
        }
      ]
    }
  ],
  "transformations": [
    {
      "name": "FIL_ACTIVE_CUSTOMER",
      "type": "Filter",
      "config": {
        "condition": "STATUS = 'ACTIVE' AND CUSTOMER_ID IS NOT NULL"
      },
      "ports": []
    },
    {
      "name": "EXP_CUSTOMER",
      "type": "Expression",
      "config": {},
      "ports": [
        {
          "name": "CUSTOMER_ID",
          "datatype": "INTEGER",
          "port_type": "INPUT",
          "expression": null
        },
        {
          "name": "FIRST_NAME",
          "datatype": "STRING",
          "port_type": "INPUT",
          "expression": null
        },
        {
          "name": "LAST_NAME",
          "datatype": "STRING",
          "port_type": "INPUT",
          "expression": null
        },
        {
          "name": "EMAIL",
          "datatype": "STRING",
          "port_type": "INPUT",
          "expression": null
        },
        {
          "name": "COUNTRY_CODE",
          "datatype": "STRING",
          "port_type": "INPUT",
          "expression": null
        },
        {
          "name": "FULL_NAME",
          "datatype": "STRING",
          "port_type": "OUTPUT",
          "expression": "TRIM(FIRST_NAME) || ' ' || TRIM(LAST_NAME)"
        },
        {
          "name": "EMAIL_NORMALIZED",
          "datatype": "STRING",
          "port_type": "OUTPUT",
          "expression": "LOWER(TRIM(EMAIL))"
        },
        {
          "name": "CUSTOMER_KEY",
          "datatype": "STRING",
          "port_type": "OUTPUT",
          "expression": "TO_CHAR(CUSTOMER_ID) || '-' || COUNTRY_CODE"
        }
      ]
    },
    {
      "name": "LKP_COUNTRY",
      "type": "Lookup",
      "config": {
        "lookup_source": "SRC_COUNTRY",
        "lookup_condition": "COUNTRY_CODE = COUNTRY_CODE",
        "lookup_type": "CONNECTED",
        "multiple_match_policy": "RETURN_FIRST",
        "join_conditions": [
          {
            "input_field": "COUNTRY_CODE",
            "lookup_field": "COUNTRY_CODE",
            "operator": "="
          }
        ]
      },
      "ports": [
        {
          "name": "COUNTRY_CODE",
          "datatype": "STRING",
          "port_type": "INPUT",
          "expression": null
        },
        {
          "name": "COUNTRY_NAME",
          "datatype": "STRING",
          "port_type": "OUTPUT",
          "expression": null
        },
        {
          "name": "REGION",
          "datatype": "STRING",
          "port_type": "OUTPUT",
          "expression": null
        }
      ]
    },
    {
      "name": "RTR_CUSTOMER_TIER",
      "type": "Router",
      "config": {
        "groups": [
          {
            "name": "PREMIUM",
            "condition": "CUSTOMER_TIER = 'PREMIUM'"
          },
          {
            "name": "STANDARD",
            "condition": "CUSTOMER_TIER = 'STANDARD'"
          },
          {
            "name": "DEFAULT",
            "condition": "TRUE"
          }
        ]
      },
      "ports": []
    },
    {
      "name": "AGG_REGION_CUSTOMERS",
      "type": "Aggregator",
      "config": {
        "group_by": [
          "REGION"
        ],
        "aggregates": [
          {
            "field": "CUSTOMER_ID",
            "function": "COUNT",
            "alias": "CUSTOMER_COUNT"
          },
          {
            "field": "CUSTOMER_ID",
            "function": "MAX",
            "alias": "MAX_CUSTOMER_ID"
          }
        ]
      },
      "ports": []
    },
    {
      "name": "SRT_CUSTOMER",
      "type": "Sorter",
      "config": {
        "sort_fields": [
          {
            "field": "REGION",
            "order": "ASC"
          },
          {
            "field": "CUSTOMER_COUNT",
            "order": "DESC"
          }
        ]
      },
      "ports": []
    }
  ],
  "connectors": [
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "CUSTOMER_ID",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "CUSTOMER_ID"
    },
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "FIRST_NAME",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "FIRST_NAME"
    },
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "LAST_NAME",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "LAST_NAME"
    },
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "EMAIL",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "EMAIL"
    },
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "STATUS",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "STATUS"
    },
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "COUNTRY_CODE",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "COUNTRY_CODE"
    },
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "CUSTOMER_TIER",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "CUSTOMER_TIER"
    },
    {
      "from_instance": "FIL_ACTIVE_CUSTOMER",
      "from_field": "CUSTOMER_ID",
      "to_instance": "EXP_CUSTOMER",
      "to_field": "CUSTOMER_ID"
    },
    {
      "from_instance": "FIL_ACTIVE_CUSTOMER",
      "from_field": "FIRST_NAME",
      "to_instance": "EXP_CUSTOMER",
      "to_field": "FIRST_NAME"
    },
    {
      "from_instance": "FIL_ACTIVE_CUSTOMER",
      "from_field": "LAST_NAME",
      "to_instance": "EXP_CUSTOMER",
      "to_field": "LAST_NAME"
    },
    {
      "from_instance": "FIL_ACTIVE_CUSTOMER",
      "from_field": "EMAIL",
      "to_instance": "EXP_CUSTOMER",
      "to_field": "EMAIL"
    },
    {
      "from_instance": "FIL_ACTIVE_CUSTOMER",
      "from_field": "COUNTRY_CODE",
      "to_instance": "EXP_CUSTOMER",
      "to_field": "COUNTRY_CODE"
    },
    {
      "from_instance": "EXP_CUSTOMER",
      "from_field": "COUNTRY_CODE",
      "to_instance": "LKP_COUNTRY",
      "to_field": "COUNTRY_CODE"
    },
    {
      "from_instance": "LKP_COUNTRY",
      "from_field": "COUNTRY_NAME",
      "to_instance": "RTR_CUSTOMER_TIER",
      "to_field": "COUNTRY_NAME"
    },
    {
      "from_instance": "EXP_CUSTOMER",
      "from_field": "CUSTOMER_ID",
      "to_instance": "RTR_CUSTOMER_TIER",
      "to_field": "CUSTOMER_ID"
    },
    {
      "from_instance": "EXP_CUSTOMER",
      "from_field": "CUSTOMER_KEY",
      "to_instance": "RTR_CUSTOMER_TIER",
      "to_field": "CUSTOMER_KEY"
    },
    {
      "from_instance": "EXP_CUSTOMER",
      "from_field": "FULL_NAME",
      "to_instance": "RTR_CUSTOMER_TIER",
      "to_field": "FULL_NAME"
    },
    {
      "from_instance": "RTR_CUSTOMER_TIER",
      "from_field": "CUSTOMER_ID",
      "to_instance": "DIM_CUSTOMER",
      "to_field": "CUSTOMER_ID"
    },
    {
      "from_instance": "RTR_CUSTOMER_TIER",
      "from_field": "CUSTOMER_KEY",
      "to_instance": "DIM_CUSTOMER",
      "to_field": "CUSTOMER_KEY"
    },
    {
      "from_instance": "RTR_CUSTOMER_TIER",
      "from_field": "FULL_NAME",
      "to_instance": "DIM_CUSTOMER",
      "to_field": "FULL_NAME"
    },
    {
      "from_instance": "LKP_COUNTRY",
      "from_field": "COUNTRY_NAME",
      "to_instance": "DIM_CUSTOMER",
      "to_field": "COUNTRY_NAME"
    },
    {
      "from_instance": "LKP_COUNTRY",
      "from_field": "REGION",
      "to_instance": "DIM_CUSTOMER",
      "to_field": "REGION"
    }
  ],
  "field_lineage": [
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "CUSTOMER_ID",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "CUSTOMER_ID"
    },
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "FIRST_NAME",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "FIRST_NAME"
    },
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "LAST_NAME",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "LAST_NAME"
    },
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "EMAIL",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "EMAIL"
    },
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "STATUS",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "STATUS"
    },
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "COUNTRY_CODE",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "COUNTRY_CODE"
    },
    {
      "from_instance": "SRC_CUSTOMER",
      "from_field": "CUSTOMER_TIER",
      "to_instance": "FIL_ACTIVE_CUSTOMER",
      "to_field": "CUSTOMER_TIER"
    },
    {
      "from_instance": "FIL_ACTIVE_CUSTOMER",
      "from_field": "CUSTOMER_ID",
      "to_instance": "EXP_CUSTOMER",
      "to_field": "CUSTOMER_ID"
    },
    {
      "from_instance": "FIL_ACTIVE_CUSTOMER",
      "from_field": "FIRST_NAME",
      "to_instance": "EXP_CUSTOMER",
      "to_field": "FIRST_NAME"
    },
    {
      "from_instance": "FIL_ACTIVE_CUSTOMER",
      "from_field": "LAST_NAME",
      "to_instance": "EXP_CUSTOMER",
      "to_field": "LAST_NAME"
    },
    {
      "from_instance": "FIL_ACTIVE_CUSTOMER",
      "from_field": "EMAIL",
      "to_instance": "EXP_CUSTOMER",
      "to_field": "EMAIL"
    },
    {
      "from_instance": "FIL_ACTIVE_CUSTOMER",
      "from_field": "COUNTRY_CODE",
      "to_instance": "EXP_CUSTOMER",
      "to_field": "COUNTRY_CODE"
    },
    {
      "from_instance": "EXP_CUSTOMER",
      "from_field": "COUNTRY_CODE",
      "to_instance": "LKP_COUNTRY",
      "to_field": "COUNTRY_CODE"
    },
    {
      "from_instance": "LKP_COUNTRY",
      "from_field": "COUNTRY_NAME",
      "to_instance": "RTR_CUSTOMER_TIER",
      "to_field": "COUNTRY_NAME"
    },
    {
      "from_instance": "EXP_CUSTOMER",
      "from_field": "CUSTOMER_ID",
      "to_instance": "RTR_CUSTOMER_TIER",
      "to_field": "CUSTOMER_ID"
    },
    {
      "from_instance": "EXP_CUSTOMER",
      "from_field": "CUSTOMER_KEY",
      "to_instance": "RTR_CUSTOMER_TIER",
      "to_field": "CUSTOMER_KEY"
    },
    {
      "from_instance": "EXP_CUSTOMER",
      "from_field": "FULL_NAME",
      "to_instance": "RTR_CUSTOMER_TIER",
      "to_field": "FULL_NAME"
    },
    {
      "from_instance": "RTR_CUSTOMER_TIER",
      "from_field": "CUSTOMER_ID",
      "to_instance": "DIM_CUSTOMER",
      "to_field": "CUSTOMER_ID"
    },
    {
      "from_instance": "RTR_CUSTOMER_TIER",
      "from_field": "CUSTOMER_KEY",
      "to_instance": "DIM_CUSTOMER",
      "to_field": "CUSTOMER_KEY"
    },
    {
      "from_instance": "RTR_CUSTOMER_TIER",
      "from_field": "FULL_NAME",
      "to_instance": "DIM_CUSTOMER",
      "to_field": "FULL_NAME"
    },
    {
      "from_instance": "LKP_COUNTRY",
      "from_field": "COUNTRY_NAME",
      "to_instance": "DIM_CUSTOMER",
      "to_field": "COUNTRY_NAME"
    },
    {
      "from_instance": "LKP_COUNTRY",
      "from_field": "REGION",
      "to_instance": "DIM_CUSTOMER",
      "to_field": "REGION"
    }
  ],
  "execution_order": [
    "AGG_CUSTOMER_REGION",
    "AGG_REGION_CUSTOMERS",
    "SRC_COUNTRY",
    "SRC_CUSTOMER",
    "SRT_CUSTOMER",
    "FIL_ACTIVE_CUSTOMER",
    "EXP_CUSTOMER",
    "LKP_COUNTRY",
    "RTR_CUSTOMER_TIER",
    "DIM_CUSTOMER"
  ]
}

# EXECUTION PLAN

{
  "mapping": "m_Sales_Customer_Load",
  "steps": [
    {
      "sequence": 1,
      "name": "AGG_CUSTOMER_REGION",
      "type": "TARGET",
      "depends_on": []
    },
    {
      "sequence": 2,
      "name": "AGG_REGION_CUSTOMERS",
      "type": "AGGREGATOR",
      "depends_on": []
    },
    {
      "sequence": 3,
      "name": "SRC_COUNTRY",
      "type": "SOURCE",
      "depends_on": []
    },
    {
      "sequence": 4,
      "name": "SRC_CUSTOMER",
      "type": "SOURCE",
      "depends_on": []
    },
    {
      "sequence": 5,
      "name": "SRT_CUSTOMER",
      "type": "SORTER",
      "depends_on": []
    },
    {
      "sequence": 6,
      "name": "FIL_ACTIVE_CUSTOMER",
      "type": "FILTER",
      "depends_on": [
        "SRC_CUSTOMER"
      ]
    },
    {
      "sequence": 7,
      "name": "EXP_CUSTOMER",
      "type": "EXPRESSION",
      "depends_on": [
        "FIL_ACTIVE_CUSTOMER"
      ]
    },
    {
      "sequence": 8,
      "name": "LKP_COUNTRY",
      "type": "LOOKUP",
      "depends_on": [
        "EXP_CUSTOMER"
      ]
    },
    {
      "sequence": 9,
      "name": "RTR_CUSTOMER_TIER",
      "type": "ROUTER",
      "depends_on": [
        "LKP_COUNTRY",
        "EXP_CUSTOMER"
      ]
    },
    {
      "sequence": 10,
      "name": "DIM_CUSTOMER",
      "type": "TARGET",
      "depends_on": [
        "RTR_CUSTOMER_TIER",
        "LKP_COUNTRY"
      ]
    }
  ]
}

# FINAL OUTPUT

Generate only valid PySpark/Python code.

Do not provide explanations.
Do not provide Markdown fences.
Do not provide analysis.

The generated code should be saved as:

output/m_Sales_Customer_Load.py
