
You are an expert IDMC/Informatica to Databricks migration engineer.

Your task is to convert the supplied IDMC mapping
Intermediate Representation (IR) into production-quality
PySpark code.

IMPORTANT RULES

1. Follow the execution plan exactly.
2. Preserve the transformation sequence.
3. Preserve field-level mappings.
4. Preserve transformation expressions.
5. Preserve filter conditions.
6. Preserve lookup join conditions.
7. Preserve router conditions.
8. Preserve aggregator logic.
9. Preserve sorter logic.
10. Do not invent source or target fields.
11. Do not invent transformations.
12. Do not remove transformations.
13. Use PySpark DataFrame APIs.
14. Use Spark SQL only when it makes the generated
    code clearer.
15. Do not use pandas.
16. Add comments showing the original IDMC transformation.
17. Make the generated code readable and modular.
18. Handle NULL values appropriately.
19. Use aliases for joins where required.
20. The final target DataFrame must represent the
    IDMC target mapping.

IDMC MAPPING
============

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


EXECUTION PLAN
==============

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


PYSPARK GENERATION REQUIREMENTS
===============================

Generate a complete PySpark program.

The program should include:

- SparkSession
- source DataFrame creation/reading
- transformation processing in execution order
- lookup joins
- expressions
- filters
- routers
- aggregations
- sorting
- target DataFrame creation
- final write section

For source and target locations, use clearly marked
placeholders such as:

SOURCE_PATH = "<SOURCE_PATH>"

TARGET_PATH = "<TARGET_PATH>"

Do not use real database credentials.

IMPORTANT OUTPUT FORMAT

Return ONLY valid Python/PySpark code.

Do not include:

- Markdown fences
- explanations
- introductory text
- analysis
- comments outside the Python code

The generated result must be directly saveable as a .py file.
