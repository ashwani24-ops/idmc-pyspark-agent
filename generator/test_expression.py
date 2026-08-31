from generator.expression_converter import ExpressionConverter

tests = [

    "FIRSTNAME || ' ' || LASTNAME",

    "UPPER(CITY)",

    "LOWER(NAME)",

    "NVL(SALARY,0)",

    "IIF(STATUS='A','ACTIVE','INACTIVE')"

]

for t in tests:

    print("="*60)

    print("Input")

    print(t)

    print()

    print("Output")

    print(ExpressionConverter.convert(t))