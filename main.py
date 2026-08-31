from pathlib import Path
from parser.xml_reader import XMLReader
from parser.mapping_parser import MappingParser
from parser.graph_builder import GraphBuilder
from utils.repository_summary import RepositorySummary
from parser.repository_parser import RepositoryParser
from utils.json_writer import JsonWriter
from agents.generator_agent import GeneratorAgent



def main():

    project_root = Path(__file__).parent

    repository = project_root / "repository"

    output = project_root / "output"

    generated = project_root / "generated"

    mappings = RepositoryParser.parse(repository)

    # Agent 1: XML -> JSON
    for mapping in mappings:

        print("\n" + "=" * 70)
        print(f"Mapping: {mapping.name}")
        print("=" * 70)

        graph = GraphBuilder.build(mapping)

        print("\nGraph Nodes:")
        print(list(graph.nodes))

        print("\nGraph Edges:")
        print(list(graph.edges))

        print("\nHas Cycle:")
        print(GraphBuilder.has_cycle(graph))

        execution_order = GraphBuilder.execution_order(graph)

        print("\nExecution Order:")
        print(execution_order)

        print("\nRoot Nodes:")
        print(GraphBuilder.root_nodes(graph))

        print("\nLeaf Nodes:")
        print(GraphBuilder.leaf_nodes(graph))

        # Generate normalized IR
        output_folder = project_root / "output"

        JsonWriter.write(
            mapping,
            execution_order,
            output_folder
        )

    # Agent 2: JSON -> PySpark
    agent = GeneratorAgent()

    for json_file in output.glob("*.json"):

        code = agent.generate(json_file)

        target = generated / (json_file.stem + ".py")

        target.write_text(code, encoding="utf-8")

        print(f"Generated: {target}")


if __name__ == "__main__":
    main()