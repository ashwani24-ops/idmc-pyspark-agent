from generator.expression_converter import ExpressionConverter


class PySparkGenerator:
    """
    Generates PySpark code from the normalized IDMC IR
    and transformation execution plan.
    """

    @staticmethod
    def generate(ir, plan):

        code = []

        mapping_name = ir.get(
            "mapping",
            "IDMC_Mapping"
        )

        # ==========================================================
        # HEADER
        # ==========================================================

        code.append(
            "# =================================================="
        )

        code.append(
            "# AUTO GENERATED PYSPARK CODE"
        )

        code.append(
            f"# Mapping: {mapping_name}"
        )

        code.append(
            "# =================================================="
        )

        code.append("")

        # ==========================================================
        # IMPORTS
        # ==========================================================

        code.append(
            "from pyspark.sql import SparkSession"
        )

        code.append(
            "from pyspark.sql.functions import *"
        )

        code.append("")

        # ==========================================================
        # SPARK SESSION
        # ==========================================================

        code.append(
            "spark = SparkSession.builder "
            f'.appName("{mapping_name}") '
            ".getOrCreate()"
        )

        code.append("")

        # ==========================================================
        # PROCESS EXECUTION PLAN
        # ==========================================================

        for step in plan:

            operation = step.get(
                "operation"
            )

            # ======================================================
            # READ
            # ======================================================

            if operation == "READ":

                PySparkGenerator._generate_read(
                    code,
                    step
                )

            # ======================================================
            # TRANSFORMATION
            # ======================================================

            elif operation == "TRANSFORMATION":

                PySparkGenerator._generate_transformation(
                    code,
                    step
                )

            # ======================================================
            # WRITE
            # ======================================================

            elif operation == "WRITE":

                PySparkGenerator._generate_write(
                    code,
                    step
                )

            # ======================================================
            # UNKNOWN
            # ======================================================

            else:

                code.append(
                    f"# WARNING: Unknown operation: "
                    f"{operation}"
                )

                code.append("")

        # ==========================================================
        # STOP SPARK
        # ==========================================================

        code.append(
            "spark.stop()"
        )

        return "\n".join(code)

    # ==============================================================
    # READ GENERATOR
    # ==============================================================

    @staticmethod
    def _generate_read(code, step):

        source = step.get(
            "object"
        )

        if not source:

            code.append(
                "# ERROR: Source object not available"
            )

            code.append("")

            return

        variable_name = (
            PySparkGenerator._safe_variable_name(
                source
            )
        )

        code.append(
            "# --------------------------------------------------"
        )

        code.append(
            f"# Read source: {source}"
        )

        code.append(
            "# --------------------------------------------------"
        )

        code.append(
            f'{variable_name}_df = '
            f'spark.read.table("{source}")'
        )

        code.append(
            f"df = {variable_name}_df"
        )

        code.append("")

    # ==============================================================
    # TRANSFORMATION GENERATOR
    # ==============================================================

    @staticmethod
    def _generate_transformation(
        code,
        step
    ):

        name = step.get(
            "name",
            "UNKNOWN_TRANSFORMATION"
        )

        transformation_type = step.get(
            "type",
            "UNKNOWN"
        )

        transformation_type_lower = (
            transformation_type.lower()
        )

        code.append(
            "# --------------------------------------------------"
        )

        code.append(
            f"# Transformation: {name}"
        )

        code.append(
            f"# Type: {transformation_type}"
        )

        code.append(
            "# --------------------------------------------------"
        )

        # ==========================================================
        # EXPRESSION
        # ==========================================================

        if transformation_type_lower == "expression":

            PySparkGenerator._generate_expression(
                code,
                step
            )

        # ==========================================================
        # FILTER
        # ==========================================================

        elif transformation_type_lower == "filter":

            PySparkGenerator._generate_filter(
                code,
                step
            )

        # ==========================================================
        # LOOKUP
        # ==========================================================

        elif transformation_type_lower == "lookup":

            PySparkGenerator._generate_lookup(
                code,
                step
            )

        # ==========================================================
        # JOINER
        # ==========================================================

        elif transformation_type_lower == "joiner":

            PySparkGenerator._generate_joiner(
                code,
                step
            )

        # ==========================================================
        # ROUTER
        # ==========================================================

        elif transformation_type_lower == "router":

            PySparkGenerator._generate_router(
                code,
                step
            )

        # ==========================================================
        # AGGREGATOR
        # ==========================================================

        elif transformation_type_lower == "aggregator":

            PySparkGenerator._generate_aggregator(
                code,
                step
            )

        # ==========================================================
        # SORTER
        # ==========================================================

        elif transformation_type_lower == "sorter":

            PySparkGenerator._generate_sorter(
                code,
                step
            )

        # ==========================================================
        # RANK
        # ==========================================================

        elif transformation_type_lower == "rank":

            PySparkGenerator._generate_rank(
                code,
                step
            )

        # ==========================================================
        # SEQUENCE GENERATOR
        # ==========================================================

        elif transformation_type_lower in [
            "sequence",
            "sequence generator",
            "sequencegenerator"
        ]:

            PySparkGenerator._generate_sequence(
                code,
                step
            )

        # ==========================================================
        # UPDATE STRATEGY
        # ==========================================================

        elif transformation_type_lower in [
            "update strategy",
            "updatestrategy"
        ]:

            PySparkGenerator._generate_update_strategy(
                code,
                step
            )

        # ==========================================================
        # UNKNOWN
        # ==========================================================

        else:

            code.append(
                f"# TODO: Implement "
                f"{transformation_type}"
            )

            code.append(
                f"# Transformation name: {name}"
            )

        code.append("")

    # ==============================================================
    # EXPRESSION
    # ==============================================================

    @staticmethod
    def _generate_expression(
        code,
        step
    ):

        ports = step.get(
            "ports",
            []
        )

        if not ports:

            code.append(
                "# No expression ports found"
            )

            return

        for port in ports:

            port_name = port.get(
                "name"
            )

            expression = port.get(
                "expression"
            )

            if not port_name:

                continue

            if not expression:

                continue

            pyspark_expression = (
                ExpressionConverter.convert(
                    expression
                )
            )

            code.append(
                f'df = df.withColumn('
                f'"{port_name}", '
                f'{pyspark_expression}'
                f')'
            )

    # ==============================================================
    # FILTER
    # ==============================================================

    @staticmethod
    def _generate_filter(
        code,
        step
    ):

        condition = step.get(
            "condition"
        )

        if not condition:

            code.append(
                "# ERROR: Filter condition "
                "not available"
            )

            return

        pyspark_condition = (
            ExpressionConverter.convert_condition(
                condition
            )
        )

        code.append(
            "df = df.filter("
        )

        code.append(
            f"    {pyspark_condition}"
        )

        code.append(
            ")"
        )

    # ==============================================================
    # LOOKUP
    # ==============================================================

    @staticmethod
    def _generate_lookup(
        code,
        step
    ):

        config = step.get(
            "config",
            {}
        )

        lookup_source = config.get(
            "lookup_source"
        )

        join_condition = config.get(
            "join_condition"
        )

        join_type = config.get(
            "join_type",
            "left"
        )

        return_fields = config.get(
            "return_fields",
            []
        )

        if not lookup_source:

            code.append(
                "# ERROR: Lookup source "
                "not available"
            )

            return

        if not join_condition:

            code.append(
                "# ERROR: Lookup join condition "
                "not available"
            )

            return

        lookup_variable = (
            PySparkGenerator._safe_variable_name(
                lookup_source
            )
        )

        # ----------------------------------------------------------
        # Read lookup
        # ----------------------------------------------------------

        code.append(
            f'# Read lookup source: '
            f'{lookup_source}'
        )

        code.append(
            f'{lookup_variable}_df = '
            f'spark.read.table("{lookup_source}")'
        )

        code.append("")

        # ----------------------------------------------------------
        # Join condition
        # ----------------------------------------------------------

        condition_parts = (
            join_condition.split("=")
        )

        if len(condition_parts) != 2:

            code.append(
                "# ERROR: Complex lookup "
                "join condition requires "
                "special handling"
            )

            return

        left_column = (
            condition_parts[0].strip()
        )

        right_column = (
            condition_parts[1].strip()
        )

        # ----------------------------------------------------------
        # Join
        # ----------------------------------------------------------

        code.append(
            "df = df.join("
        )

        code.append(
            f"    {lookup_variable}_df,"
        )

        code.append(
            f'    df["{left_column}"] == '
            f'{lookup_variable}_df["{right_column}"],'
        )

        code.append(
            f'    "{join_type}"'
        )

        code.append(
            ")"
        )

        code.append("")

        # ----------------------------------------------------------
        # Return fields
        # ----------------------------------------------------------

        for field in return_fields:

            code.append(
                f'df = df.withColumn('
                f'"{field}", '
                f'{lookup_variable}_df["{field}"]'
                f')'
            )

    # ==============================================================
    # JOINER
    # ==============================================================

    @staticmethod
    def _generate_joiner(
        code,
        step
    ):

        config = step.get(
            "config",
            {}
        )

        right_source = config.get(
            "right_source"
        )

        join_condition = config.get(
            "join_condition"
        )

        join_type = config.get(
            "join_type",
            "inner"
        )

        if not right_source:

            code.append(
                "# ERROR: Joiner right source "
                "not available"
            )

            return

        if not join_condition:

            code.append(
                "# ERROR: Joiner condition "
                "not available"
            )

            return

        right_variable = (
            PySparkGenerator._safe_variable_name(
                right_source
            )
        )

        code.append(
            f'# Read join source: '
            f'{right_source}'
        )

        code.append(
            f'{right_variable}_df = '
            f'spark.read.table("{right_source}")'
        )

        code.append("")

        condition_parts = (
            join_condition.split("=")
        )

        if len(condition_parts) != 2:

            code.append(
                "# TODO: Complex join condition"
            )

            return

        left_column = (
            condition_parts[0].strip()
        )

        right_column = (
            condition_parts[1].strip()
        )

        code.append(
            "df = df.join("
        )

        code.append(
            f"    {right_variable}_df,"
        )

        code.append(
            f'    df["{left_column}"] == '
            f'{right_variable}_df["{right_column}"],'
        )

        code.append(
            f'    "{join_type}"'
        )

        code.append(
            ")"
        )

    # ==============================================================
    # ROUTER
    # ==============================================================

    @staticmethod
    def _generate_router(
        code,
        step
    ):

        config = step.get(
            "config",
            {}
        )

        groups = config.get(
            "groups",
            []
        )

        if not groups:

            code.append(
                "# ERROR: Router groups "
                "not available"
            )

            return

        for group in groups:

            group_name = group.get(
                "name"
            )

            condition = group.get(
                "condition"
            )

            if not group_name or not condition:

                continue

            safe_name = (
                PySparkGenerator._safe_variable_name(
                    group_name
                )
            )

            converted_condition = (
                ExpressionConverter.convert_condition(
                    condition
                )
            )

            code.append(
                f'{safe_name}_df = df.filter('
                f'{converted_condition}'
                f')'
            )

    # ==============================================================
    # AGGREGATOR
    # ==============================================================

    @staticmethod
    def _generate_aggregator(
        code,
        step
    ):

        config = step.get(
            "config",
            {}
        )

        group_by = config.get(
            "group_by",
            []
        )

        aggregates = config.get(
            "aggregates",
            []
        )

        if not group_by:

            code.append(
                "# WARNING: No group-by fields"
            )

        if not aggregates:

            code.append(
                "# WARNING: No aggregate expressions"
            )

        group_columns = ", ".join(
            f'col("{column}")'
            for column in group_by
        )

        aggregate_expressions = []

        for aggregate in aggregates:

            function = aggregate.get(
                "function"
            )

            field = aggregate.get(
                "field"
            )

            alias = aggregate.get(
                "alias",
                field
            )

            if function and field:

                aggregate_expressions.append(
                    f'{function.lower()}'
                    f'(col("{field}")).alias("{alias}")'
                )

        if group_by and aggregate_expressions:

            code.append(
                "df = df.groupBy("
            )

            code.append(
                f"    {group_columns}"
            )

            code.append(
                ").agg("
            )

            code.append(
                "    "
                + ",\n    ".join(
                    aggregate_expressions
                )
            )

            code.append(
                ")"
            )

    # ==============================================================
    # SORTER
    # ==============================================================

    @staticmethod
    def _generate_sorter(
        code,
        step
    ):

        config = step.get(
            "config",
            {}
        )

        sort_fields = config.get(
            "sort_fields",
            []
        )

        if not sort_fields:

            code.append(
                "# ERROR: Sort fields "
                "not available"
            )

            return

        expressions = []

        for sort_field in sort_fields:

            field = sort_field.get(
                "field"
            )

            order = sort_field.get(
                "order",
                "ASC"
            )

            if not field:
                continue

            if order.upper() == "DESC":

                expressions.append(
                    f'col("{field}").desc()'
                )

            else:

                expressions.append(
                    f'col("{field}").asc()'
                )

        if expressions:

            code.append(
                "df = df.orderBy("
            )

            code.append(
                "    "
                + ",\n    ".join(
                    expressions
                )
            )

            code.append(
                ")"
            )

    # ==============================================================
    # RANK
    # ==============================================================

    @staticmethod
    def _generate_rank(
        code,
        step
    ):

        config = step.get(
            "config",
            {}
        )

        partition_by = config.get(
            "partition_by",
            []
        )

        order_by = config.get(
            "order_by",
            []
        )

        output_column = config.get(
            "output_column",
            "RANK"
        )

        partition_expression = ", ".join(
            f'col("{field}")'
            for field in partition_by
        )

        order_expression = []

        for field_config in order_by:

            field = field_config.get(
                "field"
            )

            order = field_config.get(
                "order",
                "DESC"
            )

            if order.upper() == "DESC":

                order_expression.append(
                    f'col("{field}").desc()'
                )

            else:

                order_expression.append(
                    f'col("{field}").asc()'
                )

        if not order_expression:

            code.append(
                "# ERROR: Rank order fields "
                "not available"
            )

            return

        code.append(
            "from pyspark.sql.window import Window"
        )

        code.append("")

        if partition_by:

            code.append(
                "window_spec = Window.partitionBy("
            )

            code.append(
                f"    {partition_expression}"
            )

            code.append(
                ").orderBy("
            )

        else:

            code.append(
                "window_spec = Window.orderBy("
            )

        code.append(
            "    "
            + ",\n    ".join(
                order_expression
            )
        )

        code.append(
            ")"
        )

        code.append("")

        code.append(
            f'df = df.withColumn('
            f'"{output_column}", '
            f'rank().over(window_spec)'
            f')'
        )

    # ==============================================================
    # SEQUENCE GENERATOR
    # ==============================================================

    @staticmethod
    def _generate_sequence(
        code,
        step
    ):

        config = step.get(
            "config",
            {}
        )

        output_column = config.get(
            "output_column",
            "SEQUENCE_ID"
        )

        code.append(
            "from pyspark.sql.window import Window"
        )

        code.append("")

        code.append(
            "window_spec = Window.orderBy("
            "monotonically_increasing_id()"
            ")"
        )

        code.append("")

        code.append(
            f'df = df.withColumn('
            f'"{output_column}", '
            f'row_number().over(window_spec)'
            f')'
        )

    # ==============================================================
    # UPDATE STRATEGY
    # ==============================================================

    @staticmethod
    def _generate_update_strategy(
        code,
        step
    ):

        config = step.get(
            "config",
            {}
        )

        strategy = config.get(
            "strategy"
        )

        code.append(
            "# --------------------------------------------------"
        )

        code.append(
            "# Update Strategy"
        )

        code.append(
            f"# Strategy: {strategy}"
        )

        code.append(
            "# --------------------------------------------------"
        )

        code.append(
            "# TODO: Implement Delta MERGE / "
            "INSERT / UPDATE / DELETE logic"
        )

    # ==============================================================
    # WRITE
    # ==============================================================

    @staticmethod
    def _generate_write(
        code,
        step
    ):

        target = step.get(
            "object"
        )

        if not target:

            code.append(
                "# ERROR: Target object "
                "not available"
            )

            return

        code.append(
            "# --------------------------------------------------"
        )

        code.append(
            f"# Write target: {target}"
        )

        code.append(
            "# --------------------------------------------------"
        )

        code.append(
            f'df.write.mode("overwrite")'
            f'.saveAsTable("{target}")'
        )

        code.append("")

    # ==============================================================
    # SAFE VARIABLE NAME
    # ==============================================================

    @staticmethod
    def _safe_variable_name(
        name
    ):

        if not name:

            return "df"

        value = (
            str(name)
            .lower()
            .strip()
        )

        value = (
            value
            .replace(" ", "_")
            .replace("-", "_")
            .replace(".", "_")
            .replace("/", "_")
        )

        return value