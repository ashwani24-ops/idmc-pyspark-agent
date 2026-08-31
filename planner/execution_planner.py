from pathlib import Path
import json


class ExecutionPlanner:


    def __init__(self, ir):

        self.ir = ir


    # ======================================================
    # MAIN METHOD
    # ======================================================

    def generate_plan(self):

        execution_order = (
            self.ir.get(
                "execution_order",
                []
            )
        )


        steps = []


        sequence = 1


        for node in execution_order:


            step_type = (
                self._identify_type(
                    node
                )
            )


            dependencies = (
                self._get_dependencies(
                    node
                )
            )


            steps.append({

                "sequence":
                    sequence,

                "name":
                    node,

                "type":
                    step_type,

                "depends_on":
                    dependencies
            })


            sequence += 1


        return {

            "mapping":
                self.ir.get(
                    "name"
                ),

            "steps":
                steps
        }



    # ======================================================
    # IDENTIFY NODE TYPE
    # ======================================================

    def _identify_type(
        self,
        node
    ):


        for source in self.ir.get(
            "sources",
            []
        ):

            if source["name"] == node:

                return "SOURCE"



        for target in self.ir.get(
            "targets",
            []
        ):

            if target["name"] == node:

                return "TARGET"



        for transformation in self.ir.get(
            "transformations",
            []
        ):

            if transformation["name"] == node:

                return (
                    transformation["type"]
                    .upper()
                )


        return "UNKNOWN"



    # ======================================================
    # DEPENDENCIES
    # ======================================================

    def _get_dependencies(
        self,
        node
    ):


        dependencies = []


        for lineage in self.ir.get(
            "field_lineage",
            []
        ):


            if lineage[
                "to_instance"
            ] == node:


                dependency = (
                    lineage[
                        "from_instance"
                    ]
                )


                if dependency not in dependencies:

                    dependencies.append(
                        dependency
                    )


        return dependencies