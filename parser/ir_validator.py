from pathlib import Path
import json


class IRValidator:

    def __init__(self, ir):
        self.ir = ir
        self.errors = []
        self.warnings = []

    # ==========================================================
    # MAIN VALIDATION
    # ==========================================================

    def validate(self):

        self.errors = []
        self.warnings = []

        self._validate_mapping()
        self._validate_sources()
        self._validate_targets()
        self._validate_transformations()
        self._validate_connectors()
        self._validate_execution_order()
        self._validate_field_lineage()

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings
        }

    # ==========================================================
    # HELPER
    # ==========================================================

    @staticmethod
    def _as_list(value):

        if value is None:
            return []

        if isinstance(value, list):
            return value

        if isinstance(value, dict):
            return list(value.values())

        return []

    # ==========================================================
    # MAPPING
    # ==========================================================

    def _validate_mapping(self):

        if not self.ir.get("name"):

            self.errors.append(
                "Mapping name is missing"
            )

    # ==========================================================
    # SOURCES
    # ==========================================================

    def _validate_sources(self):

        sources = self._as_list(
            self.ir.get("sources")
        )

        if not sources:

            self.warnings.append(
                "Mapping has no sources"
            )

        for source in sources:

            if not isinstance(source, dict):

                self.errors.append(
                    f"Invalid source object: "
                    f"{source}"
                )

                continue

            name = source.get("name")

            if not name:

                self.errors.append(
                    "Source without name found"
                )

                continue

            if not source.get("fields"):

                self.warnings.append(
                    f"Source '{name}' "
                    f"has no fields"
                )

    # ==========================================================
    # TARGETS
    # ==========================================================

    def _validate_targets(self):

        targets = self._as_list(
            self.ir.get("targets")
        )

        if not targets:

            self.errors.append(
                "Mapping has no targets"
            )

        for target in targets:

            if not isinstance(target, dict):

                self.errors.append(
                    f"Invalid target object: "
                    f"{target}"
                )

                continue

            name = target.get("name")

            if not name:

                self.errors.append(
                    "Target without name found"
                )

                continue

            if not target.get("fields"):

                self.warnings.append(
                    f"Target '{name}' "
                    f"has no fields"
                )

    # ==========================================================
    # TRANSFORMATIONS
    # ==========================================================

    def _validate_transformations(self):

        transformations = self._as_list(
            self.ir.get("transformations")
        )

        names = set()

        for transformation in transformations:

            if not isinstance(
                transformation,
                dict
            ):

                self.errors.append(
                    f"Invalid transformation: "
                    f"{transformation}"
                )

                continue

            name = transformation.get(
                "name"
            )

            transformation_type = (
                transformation.get("type")
            )

            if not name:

                self.errors.append(
                    "Transformation "
                    "without name found"
                )

                continue

            if name in names:

                self.errors.append(
                    f"Duplicate transformation: "
                    f"{name}"
                )

            names.add(name)

            if not transformation_type:

                self.errors.append(
                    f"Transformation '{name}' "
                    f"has no type"
                )

            # --------------------------------------------------
            # Filter
            # --------------------------------------------------

            if (
                transformation_type
                and transformation_type.lower()
                == "filter"
            ):

                config = transformation.get(
                    "config",
                    {}
                )

                condition = config.get(
                    "condition"
                )

                if not condition:

                    self.errors.append(
                        f"Filter '{name}' "
                        f"has no condition"
                    )

            # --------------------------------------------------
            # Lookup
            # --------------------------------------------------

            if (
                transformation_type
                and transformation_type.lower()
                == "lookup"
            ):

                config = transformation.get(
                    "config",
                    {}
                )

                if not config.get(
                    "lookup_source"
                ):

                    self.errors.append(
                        f"Lookup '{name}' "
                        f"has no lookup source"
                    )

                if not config.get(
                    "join_conditions"
                ):

                    self.warnings.append(
                        f"Lookup '{name}' "
                        f"has no parsed "
                        f"join conditions"
                    )

    # ==========================================================
    # CONNECTORS
    # ==========================================================

    def _validate_connectors(self):

        connectors = self._as_list(
            self.ir.get("connectors")
        )

        sources = self._as_list(
            self.ir.get("sources")
        )

        targets = self._as_list(
            self.ir.get("targets")
        )

        transformations = self._as_list(
            self.ir.get("transformations")
        )

        source_names = {
            item.get("name")
            for item in sources
            if isinstance(item, dict)
            and item.get("name")
        }

        target_names = {
            item.get("name")
            for item in targets
            if isinstance(item, dict)
            and item.get("name")
        }

        transformation_names = {
            item.get("name")
            for item in transformations
            if isinstance(item, dict)
            and item.get("name")
        }

        valid_nodes = (
            source_names
            | target_names
            | transformation_names
        )

        for connector in connectors:

            if not isinstance(
                connector,
                dict
            ):

                self.errors.append(
                    f"Invalid connector: "
                    f"{connector}"
                )

                continue

            source = connector.get(
                "from_instance"
            )

            target = connector.get(
                "to_instance"
            )

            if source not in valid_nodes:

                self.errors.append(
                    f"Connector references "
                    f"unknown source instance: "
                    f"{source}"
                )

            if target not in valid_nodes:

                self.errors.append(
                    f"Connector references "
                    f"unknown target instance: "
                    f"{target}"
                )

            if not connector.get(
                "from_field"
            ):

                self.errors.append(
                    "Connector has no "
                    "from_field"
                )

            if not connector.get(
                "to_field"
            ):

                self.errors.append(
                    "Connector has no "
                    "to_field"
                )

    # ==========================================================
    # EXECUTION ORDER
    # ==========================================================

    def _validate_execution_order(self):

        execution_order = self._as_list(
            self.ir.get(
                "execution_order"
            )
        )

        if not execution_order:

            self.errors.append(
                "Execution order is empty"
            )

            return

        sources = self._as_list(
            self.ir.get("sources")
        )

        transformations = self._as_list(
            self.ir.get("transformations")
        )

        targets = self._as_list(
            self.ir.get("targets")
        )

        all_nodes = set()

        for source in sources:

            if (
                isinstance(source, dict)
                and source.get("name")
            ):

                all_nodes.add(
                    source["name"]
                )

        for transformation in transformations:

            if (
                isinstance(transformation, dict)
                and transformation.get("name")
            ):

                all_nodes.add(
                    transformation["name"]
                )

        for target in targets:

            if (
                isinstance(target, dict)
                and target.get("name")
            ):

                all_nodes.add(
                    target["name"]
                )

        ordered_nodes = set(
            execution_order
        )

        missing = (
            all_nodes - ordered_nodes
        )

        if missing:

            self.errors.append(
                "Nodes missing from "
                "execution order: "
                f"{sorted(missing)}"
            )

        extra = (
            ordered_nodes - all_nodes
        )

        if extra:

            self.warnings.append(
                "Unknown nodes in execution "
                f"order: {sorted(extra)}"
            )

    # ==========================================================
    # FIELD LINEAGE
    # ==========================================================

    def _validate_field_lineage(self):

        lineage = self._as_list(
            self.ir.get(
                "field_lineage"
            )
        )

        connectors = self._as_list(
            self.ir.get(
                "connectors"
            )
        )

        if connectors and not lineage:

            self.errors.append(
                "Connectors exist but "
                "field_lineage is empty"
            )

        if len(lineage) != len(connectors):

            self.warnings.append(
                "Field lineage count "
                "does not match "
                "connector count"
            )

    # ==========================================================
    # REPORT
    # ==========================================================

    def print_report(self):

        print()
        print("=" * 70)
        print("IR VALIDATION REPORT")
        print("=" * 70)

        print(
            f"Mapping: "
            f"{self.ir.get('name')}"
        )

        print()

        print(
            f"ERRORS: "
            f"{len(self.errors)}"
        )

        for error in self.errors:

            print(
                f"  ERROR: {error}"
            )

        print()

        print(
            f"WARNINGS: "
            f"{len(self.warnings)}"
        )

        for warning in self.warnings:

            print(
                f"  WARNING: {warning}"
            )

        print()

        if not self.errors:

            print(
                "STATUS: VALID"
            )

        else:

            print(
                "STATUS: INVALID"
            )

        print(
            "=" * 70
        )