import json
import xml.etree.ElementTree as ET
from pathlib import Path

class RepositoryParser:
    """
    Parses IDMC Repository XML
    and generates normalized Intermediate Representation (IR)
    """

    # ==========================================================
    # MAIN PARSER
    # ==========================================================

    @staticmethod
    def parse(xml_file):

        xml_file = Path(xml_file)

        if not xml_file.exists():
            raise FileNotFoundError(
                f"Repository XML not found: {xml_file}"
            )

        tree = ET.parse(xml_file)

        root = tree.getroot()

        mappings = []

        for mapping_element in root.findall(".//MAPPING"):

            mapping = (
                RepositoryParser._parse_mapping(
                    mapping_element
                )
            )

            mappings.append(mapping)

        return mappings


    # ==========================================================
    # MAPPING PARSER
    # ==========================================================

    @staticmethod
    def _parse_mapping(mapping_element):

        mapping = {

            "name":
                mapping_element.get(
                    "NAME",
                    "UNKNOWN_MAPPING"
                ),

            "description":
                mapping_element.get(
                    "DESCRIPTION",
                    ""
                ),

            "sources": [],

            "targets": [],

            "transformations": [],

            "connectors": [],

            "field_lineage": [],

            "execution_order": []
        }


        # -----------------------------
        # SOURCES
        # -----------------------------

        for source in mapping_element.findall(
            "./SOURCE"
        ):

            mapping["sources"].append(
                RepositoryParser._parse_source(
                    source
                )
            )


        # -----------------------------
        # TARGETS
        # -----------------------------

        for target in mapping_element.findall(
            "./TARGET"
        ):

            mapping["targets"].append(
                RepositoryParser._parse_target(
                    target
                )
            )


        # -----------------------------
        # TRANSFORMATIONS
        # -----------------------------

        for transformation in mapping_element.findall(
            "./TRANSFORMATION"
        ):

            mapping["transformations"].append(
                RepositoryParser._parse_transformation(
                    transformation
                )
            )


        # -----------------------------
        # CONNECTORS
        # -----------------------------

        for connector in mapping_element.findall(
            "./CONNECTOR"
        ):

            mapping["connectors"].append({

                "from_instance":
                    connector.get(
                        "FROMINSTANCE"
                    ),

                "from_field":
                    connector.get(
                        "FROMFIELD"
                    ),

                "to_instance":
                    connector.get(
                        "TOINSTANCE"
                    ),

                "to_field":
                    connector.get(
                        "TOFIELD"
                    )
            })


        # -----------------------------
        # FIELD LINEAGE
        # -----------------------------

        mapping["field_lineage"] = (

            RepositoryParser
            ._build_field_lineage(
                mapping["connectors"]
            )

        )


        # -----------------------------
        # EXECUTION ORDER
        # -----------------------------

        mapping["execution_order"] = (

            RepositoryParser
            ._build_execution_order(
                mapping
            )

        )


        return mapping



    # ==========================================================
    # SOURCE
    # ==========================================================

    @staticmethod
    def _parse_source(element):

        source = {

            "name":
                element.get(
                    "NAME"
                ),

            "type":
                element.get(
                    "TYPE"
                ),

            "fields": []
        }


        for field in element.findall(
            "./FIELD"
        ):

            source["fields"].append({

                "name":
                    field.get(
                        "NAME"
                    ),

                "datatype":
                    field.get(
                        "DATATYPE"
                    )
            })


        return source



    # ==========================================================
    # TARGET
    # ==========================================================

    @staticmethod
    def _parse_target(element):

        target = {

            "name":
                element.get(
                    "NAME"
                ),

            "type":
                element.get(
                    "TYPE"
                ),

            "fields": []
        }


        for field in element.findall(
            "./FIELD"
        ):

            target["fields"].append({

                "name":
                    field.get(
                        "NAME"
                    ),

                "datatype":
                    field.get(
                        "DATATYPE"
                    )
            })


        return target



    # ==========================================================
    # TRANSFORMATION
    # ==========================================================

    @staticmethod
    def _parse_transformation(element):

        name = element.get(
            "NAME"
        )

        transformation_type = element.get(
            "TYPE"
        )


        transformation = {

            "name":
                name,

            "type":
                transformation_type,

            "config": {},

            "ports": []
        }


        # -----------------------------
        # Attributes
        # -----------------------------

        for attribute in element.findall(
            "./ATTRIBUTE"
        ):

            key = attribute.get(
                "NAME"
            )

            value = attribute.get(
                "VALUE"
            )


            if key:

                transformation["config"][
                    key.lower()
                ] = value



        type_lower = (
            transformation_type.lower()
            if transformation_type
            else ""
        )



        # -----------------------------
        # Filter
        # -----------------------------

        if type_lower == "filter":

            condition = (
                transformation["config"]
                .get(
                    "filter_condition"
                )
            )

            transformation["config"] = {

                "condition":
                    condition
            }



        # -----------------------------
        # Lookup
        # -----------------------------

        elif type_lower == "lookup":

            config = transformation["config"]


            transformation["config"] = {

                "lookup_source":
                    config.get(
                        "lookup_source"
                    ),

                "lookup_condition":
                    config.get(
                        "lookup_condition"
                    ),

                "lookup_type":
                    config.get(
                        "lookup_type",
                        "CONNECTED"
                    ),

                "multiple_match_policy":
                    config.get(
                        "multiple_match_policy"
                    ),

                "join_conditions":
                    RepositoryParser
                    ._parse_lookup_condition(
                        config.get(
                            "lookup_condition"
                        )
                    )
            }



        # -----------------------------
        # Router
        # -----------------------------

        elif type_lower == "router":

            groups = []


            for group in element.findall(
                "./GROUP"
            ):

                groups.append({

                    "name":
                        group.get(
                            "NAME"
                        ),

                    "condition":
                        group.get(
                            "CONDITION"
                        )
                })


            transformation["config"] = {

                "groups":
                    groups
            }



        # -----------------------------
        # Aggregator
        # -----------------------------

        elif type_lower == "aggregator":

            group_by = []

            aggregates = []


            for group in element.findall(
                "./GROUPBY"
            ):

                group_by.append(
                    group.get(
                        "FIELD"
                    )
                )


            for aggregate in element.findall(
                "./AGGREGATE"
            ):

                aggregates.append({

                    "field":
                        aggregate.get(
                            "FIELD"
                        ),

                    "function":
                        aggregate.get(
                            "FUNCTION"
                        ),

                    "alias":
                        aggregate.get(
                            "OUTPUT"
                        )
                })


            transformation["config"] = {

                "group_by":
                    group_by,

                "aggregates":
                    aggregates
            }



        # -----------------------------
        # Sorter
        # -----------------------------

        elif type_lower == "sorter":

            sort_fields = []


            for sort_field in element.findall(
                "./SORTFIELD"
            ):

                sort_fields.append({

                    "field":
                        sort_field.get(
                            "FIELD"
                        ),

                    "order":
                        sort_field.get(
                            "ORDER",
                            "ASC"
                        )
                })


            transformation["config"] = {

                "sort_fields":
                    sort_fields
            }



        # -----------------------------
        # Ports
        # -----------------------------

        for port in element.findall(
            "./PORT"
        ):

            transformation["ports"].append({

                "name":
                    port.get(
                        "NAME"
                    ),

                "datatype":
                    port.get(
                        "DATATYPE"
                    ),

                "port_type":
                    port.get(
                        "PORTTYPE"
                    ),

                "expression":
                    port.get(
                        "EXPRESSION"
                    )
            })


        return transformation



    # ==========================================================
    # LOOKUP CONDITION PARSER
    # ==========================================================

    @staticmethod
    def _parse_lookup_condition(condition):

        if not condition:

            return []


        parts = condition.split("=")


        if len(parts) != 2:

            return []


        return [{

            "input_field":
                parts[0].strip(),

            "lookup_field":
                parts[1].strip(),

            "operator":
                "="
        }]



    # ==========================================================
    # FIELD LINEAGE
    # ==========================================================

    @staticmethod
    def _build_field_lineage(connectors):

        lineage = []


        for connector in connectors:

            lineage.append({

                "from_instance":
                    connector.get(
                        "from_instance"
                    ),

                "from_field":
                    connector.get(
                        "from_field"
                    ),

                "to_instance":
                    connector.get(
                        "to_instance"
                    ),

                "to_field":
                    connector.get(
                        "to_field"
                    )
            })


        return lineage



    # ==========================================================
    # EXECUTION ORDER
    # ==========================================================

    @staticmethod
    def _build_execution_order(mapping):

        nodes = set()


        for source in mapping["sources"]:

            nodes.add(
                source["name"]
            )


        for transformation in mapping["transformations"]:

            nodes.add(
                transformation["name"]
            )


        for target in mapping["targets"]:

            nodes.add(
                target["name"]
            )


        graph = {

            node: set()

            for node in nodes
        }



        for connector in mapping["connectors"]:

            frm = connector[
                "from_instance"
            ]

            to = connector[
                "to_instance"
            ]


            if frm in graph and to in graph:

                graph[to].add(
                    frm
                )



        result = []


        while graph:

            ready = [

                node

                for node, deps

                in graph.items()

                if not deps

            ]


            if not ready:

                raise Exception(
                    "Circular dependency detected"
                )


            for node in sorted(ready):

                result.append(
                    node
                )

                del graph[node]


                for deps in graph.values():

                    deps.discard(
                        node
                    )


        return result