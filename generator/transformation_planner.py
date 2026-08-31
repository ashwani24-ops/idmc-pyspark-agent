class TransformationPlanner:
    """
    Creates an ordered transformation plan from the normalized IR.
    """

    @staticmethod
    def create_plan(ir):

        execution_order = ir.get("execution_order", [])
        
        transformations = {
            transformation["name"]: transformation
            for transformation in ir.get("transformations", [])
        }

        sources = set(ir.get("sources", []))
        targets = set(ir.get("targets", []))

        plan = []

        for node in execution_order:

            if node in sources:

                plan.append({
                    "step": len(plan) + 1,
                    "operation": "READ",
                    "object": node
                })

            elif node in transformations:

                transformation = transformations[node]

                plan.append({
                    "step": len(plan) + 1,
                    "operation": "TRANSFORMATION",
                    "name": transformation["name"],
                    "type": transformation["type"],
                    "config": transformation.get("config", {}),
                    "condition": transformation.get("condition"),
                    "attributes": transformation.get("attributes", {}),
                    "ports": transformation.get("ports", [])
                })

            elif node in targets:

                plan.append({
                    "step": len(plan) + 1,
                    "operation": "WRITE",
                    "object": node
                })

        return plan