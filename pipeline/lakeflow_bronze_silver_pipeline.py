from pyspark import pipelines as dp
from pyspark.sql.functions import col, when


@dp.materialized_view(
    name="lf_bronze_users",
    comment="Raw ingestion-style user data containing nulls and invalid values."
)
def bronze_users():
    data = [
        (1, "jenny", "US", 100),
        (2, "mike", "CA", None),
        (3, "sara", None, 200),
        (4, "john", "US", -50),
        (5, "anna", "UK", 300)
    ]

    columns = ["user_id", "name", "country", "amount"]

    return spark.createDataFrame(data, columns)


@dp.materialized_view(
    name="lf_silver_users",
    comment="Cleaned user data with invalid amounts removed and missing countries handled."
)
def silver_users():
    bronze_df = spark.read.table("lf_bronze_users")

    return (
        bronze_df
        .filter(col("amount") > 0)
        .withColumn(
            "country",
            when(col("country").isNull(), "UNKNOWN").otherwise(col("country"))
        )
    )