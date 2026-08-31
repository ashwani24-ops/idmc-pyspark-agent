import json
from pathlib import Path


class JsonWriter:

    @staticmethod
    def write(mapping, execution_order, output_folder):

        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

        data = {
            "mapping": mapping.name,
            "description": mapping.description,
            "folder": mapping.folder,
            "sources": mapping.sources,
            "targets": mapping.targets,
            "execution_order": execution_order,
            "transformations": [],
            "connectors": []
        }

        # Transformations
        for transformation in mapping.transformations:

            transformation_data = {
                
                "name": transformation.name,
                "type": transformation.type,
                "condition": getattr(
                    transformation,
                    "condition",
                    None
                ),
                "attributes": getattr(
                    transformation,
                    "attributes",
                    {}
                ),
                "ports": []

            }

            for port in transformation.ports:

                transformation_data["ports"].append({
                    "name": port.name,
                    "datatype": port.datatype,
                    "port_type": port.port_type,
                    "expression": port.expression
                })

            data["transformations"].append(
                transformation_data
            )

        # Connectors
        for connector in mapping.connectors:

            data["connectors"].append({
                "from_instance": connector.from_instance,
                "from_field": connector.from_field,
                "to_instance": connector.to_instance,
                "to_field": connector.to_field
            })

        output_file = output_folder / f"{mapping.name}.json"

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(f"IR generated: {output_file}")

        return output_file