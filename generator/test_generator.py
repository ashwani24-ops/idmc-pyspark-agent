from pathlib import Path

from generator.ir_reader import IRReader

from generator.transformation_planner import TransformationPlanner

from generator.pyspark_generator import PySparkGenerator


project = Path(__file__).resolve().parent.parent

mapping = IRReader.read(

project / "output" / "Customer_Load.json"

)

plan = TransformationPlanner.create_plan(mapping)

code = PySparkGenerator.generate(plan)

print(code)