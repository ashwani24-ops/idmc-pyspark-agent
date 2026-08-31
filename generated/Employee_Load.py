# ==================================================
# AUTO GENERATED PYSPARK CODE
# Mapping: Employee_Load
# ==================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder .appName("Employee_Load") .getOrCreate()

# --------------------------------------------------
# Read source: CUSTOMER
# --------------------------------------------------
customer_df = spark.read.table("CUSTOMER")
df = customer_df

# --------------------------------------------------
# Transformation: EXP_CUSTOMER
# Type: Expression
# --------------------------------------------------
df = df.withColumn("FULL_NAME", concat(col("FIRSTNAME"), lit(' '), col("LASTNAME")))

# --------------------------------------------------
# Write target: DIM_CUSTOMER
# --------------------------------------------------
df.write.mode("overwrite").saveAsTable("DIM_CUSTOMER")

spark.stop()