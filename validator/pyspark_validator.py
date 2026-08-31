import ast
import re


class PySparkValidator:

    def __init__(self, ir, execution_plan, pyspark_code):

        self.ir = ir
        self.execution_plan = execution_plan
        self.code = pyspark_code

        self.errors = []
        self.warnings = []
        self.results = []

    # =========================================================
    # MAIN VALIDATION
    # =========================================================

    def validate(self):

        self._validate_python_syntax()

        self._validate_sources()

        self._validate_transformations()

        self._validate_targets()

        self._validate_transformation_order()

        self._validate_target_usage()

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "results": self.results
        }

    # =========================================================
    # PYTHON SYNTAX
    # =========================================================

    def _validate_python_syntax(self):

        try:

            ast.parse(self.code)

            self.results.append({
                "check": "Python syntax",
                "status": "PASS"
            })

        except SyntaxError as exc:

            self.errors.append(
                f"Python syntax error: {exc}"
            )

            self.results.append({
                "check": "Python syntax",
                "status": "FAIL"
            })

    # =========================================================
    # SOURCES
    # =========================================================

    def _validate_sources(self):

        sources = self.ir.get(
            "sources",
            []
        )

        for source in sources:

            name = source.get(
                "name"
            )

            # Look for source comment
            # Example:
            # Source: SRC_CUSTOMER

            found = (
                f"Source: {name}" in self.code
                or
                name in self.code
            )

            if found:

                self.results.append({
                    "check":
                        f"Source: {name}",
                    "status":
                        "PASS"
                })

            else:

                self.errors.append(
                    f"Source missing from PySpark: {name}"
                )

                self.results.append({
                    "check":
                        f"Source: {name}",
                    "status":
                        "FAIL"
                })

    # =========================================================
    # TRANSFORMATIONS
    # =========================================================

    def _validate_transformations(self):

        transformations = self.ir.get(
            "transformations",
            []
        )

        for transformation in transformations:

            name = transformation.get(
                "name"
            )

            transformation_type = (
                transformation.get(
                    "type",
                    ""
                ).upper()
            )

            found = (
                name in self.code
            )

            if found:

                self.results.append({
                    "check":
                        f"{transformation_type}: {name}",
                    "status":
                        "PASS"
                })

            else:

                self.errors.append(
                    "Transformation missing from "
                    f"PySpark: {name} "
                    f"({transformation_type})"
                )

                self.results.append({
                    "check":
                        f"{transformation_type}: {name}",
                    "status":
                        "FAIL"
                })

    # =========================================================
    # TARGETS
    # =========================================================

    def _validate_targets(self):

        targets = self.ir.get(
            "targets",
            []
        )

        for target in targets:

            name = target.get(
                "name"
            )

            found = (
                name in self.code
            )

            if found:

                self.results.append({
                    "check":
                        f"Target: {name}",
                    "status":
                        "PASS"
                })

            else:

                self.errors.append(
                    f"Target missing from PySpark: {name}"
                )

                self.results.append({
                    "check":
                        f"Target: {name}",
                    "status":
                        "FAIL"
                })

    # =========================================================
    # EXECUTION ORDER
    # =========================================================

    def _validate_transformation_order(self):

        steps = self.execution_plan.get(
            "steps",
            []
        )

        positions = {}

        for step in steps:

            name = step.get(
                "name"
            )

            position = self.code.find(
                name
            )

            if position >= 0:

                positions[name] = position

        previous_position = -1

        for step in steps:

            name = step.get(
                "name"
            )

            if name not in positions:

                continue

            current_position = positions[name]

            if current_position < previous_position:

                self.warnings.append(
                    f"Execution order may be incorrect "
                    f"around: {name}"
                )

            previous_position = current_position

        self.results.append({
            "check":
                "Execution order",
            "status":
                "PASS"
                if not any(
                    "Execution order" in error
                    for error in self.errors
                )
                else "FAIL"
        })

    # =========================================================
    # TARGET USAGE
    # =========================================================

    def _validate_target_usage(self):

        targets = self.ir.get(
            "targets",
            []
        )

        for target in targets:

            target_name = target.get(
                "name"
            )

            # Remove potential XML prefixes
            # when checking generated code.

            target_fields = [
                field.get("name")
                for field in target.get(
                    "fields",
                    []
                )
            ]

            missing_fields = []

            for field in target_fields:

                if field and field not in self.code:

                    missing_fields.append(
                        field
                    )

            if missing_fields:

                self.warnings.append(
                    f"Target {target_name} "
                    f"may have missing fields: "
                    f"{missing_fields}"
                )

            else:

                self.results.append({
                    "check":
                        f"Target fields: {target_name}",
                    "status":
                        "PASS"
                })