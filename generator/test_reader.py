from pathlib import Path

from generator.ir_reader import IRReader


project = Path(__file__).resolve().parent.parent

ir = project / "output" / "Customer_Load.json"

mapping = IRReader.read(ir)

print(ir)
print(mapping)