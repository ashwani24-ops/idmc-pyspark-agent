import re


class ExpressionConverter:
    """
    Converts Informatica expressions into equivalent PySpark expressions.
    """

    @staticmethod
    def convert(expression: str) -> str:

        if expression is None:
            return ""

        expr = expression.strip()

        expr = ExpressionConverter.convert_concat(expr)
        expr = ExpressionConverter.convert_nvl(expr)
        expr = ExpressionConverter.convert_upper(expr)
        expr = ExpressionConverter.convert_lower(expr)
        expr = ExpressionConverter.convert_trim(expr)
        expr = ExpressionConverter.convert_ltrim(expr)
        expr = ExpressionConverter.convert_rtrim(expr)
        expr = ExpressionConverter.convert_substr(expr)
        expr = ExpressionConverter.convert_length(expr)
        expr = ExpressionConverter.convert_abs(expr)
        expr = ExpressionConverter.convert_round(expr)
        expr = ExpressionConverter.convert_isnull(expr)
        expr = ExpressionConverter.convert_iif(expr)
        expr = ExpressionConverter.convert_decode(expr)

        return expr

    # -------------------------------------------------------
    # CONCAT
    # FIRST || ' ' || LAST
    # -------------------------------------------------------

    @staticmethod
    def convert_concat(expr):

        if "||" not in expr:
            return expr

        parts = [p.strip() for p in expr.split("||")]

        converted = []

        for part in parts:

            if part.startswith("'") and part.endswith("'"):

                converted.append(f"lit({part})")

            else:

                converted.append(f'col("{part}")')

        return "concat(" + ", ".join(converted) + ")"

    # -------------------------------------------------------

    @staticmethod
    def convert_upper(expr):

        return re.sub(
            r'UPPER\((.*?)\)',
            r'upper(col("\1"))',
            expr,
            flags=re.IGNORECASE
        )

    # -------------------------------------------------------

    @staticmethod
    def convert_lower(expr):

        return re.sub(
            r'LOWER\((.*?)\)',
            r'lower(col("\1"))',
            expr,
            flags=re.IGNORECASE
        )

    # -------------------------------------------------------

    @staticmethod
    def convert_trim(expr):

        return re.sub(
            r'TRIM\((.*?)\)',
            r'trim(col("\1"))',
            expr,
            flags=re.IGNORECASE
        )

    # -------------------------------------------------------

    @staticmethod
    def convert_ltrim(expr):

        return re.sub(
            r'LTRIM\((.*?)\)',
            r'ltrim(col("\1"))',
            expr,
            flags=re.IGNORECASE
        )

    # -------------------------------------------------------

    @staticmethod
    def convert_rtrim(expr):

        return re.sub(
            r'RTRIM\((.*?)\)',
            r'rtrim(col("\1"))',
            expr,
            flags=re.IGNORECASE
        )

    # -------------------------------------------------------

    @staticmethod
    def convert_nvl(expr):

        return re.sub(
            r'NVL\((.*?),(.*?)\)',
            r'coalesce(col("\1"), lit(\2))',
            expr,
            flags=re.IGNORECASE
        )

    # -------------------------------------------------------

    @staticmethod
    def convert_substr(expr):

        return re.sub(
            r'SUBSTR\((.*?),(.*?),(.*?)\)',
            r'substring(col("\1"), \2, \3)',
            expr,
            flags=re.IGNORECASE
        )

    # -------------------------------------------------------

    @staticmethod
    def convert_length(expr):

        return re.sub(
            r'LENGTH\((.*?)\)',
            r'length(col("\1"))',
            expr,
            flags=re.IGNORECASE
        )

    # -------------------------------------------------------

    @staticmethod
    def convert_abs(expr):

        return re.sub(
            r'ABS\((.*?)\)',
            r'abs(col("\1"))',
            expr,
            flags=re.IGNORECASE
        )

    # -------------------------------------------------------

    @staticmethod
    def convert_round(expr):

        return re.sub(
            r'ROUND\((.*?),(.*?)\)',
            r'round(col("\1"), \2)',
            expr,
            flags=re.IGNORECASE
        )

    # -------------------------------------------------------


    @staticmethod
    def convert_condition(condition):

        if not condition:
            return ""

        expr = condition.strip()

        # Informatica operators
        expr = re.sub(
            r'<>',
            '!=',
            expr
        )

        expr = re.sub(
            r'\bAND\b',
            '&',
            expr,
            flags=re.IGNORECASE
        )

        expr = re.sub(
            r'\bOR\b',
            '|',
            expr,
            flags=re.IGNORECASE
        )

        # Equality
        expr = re.sub(
            r'(?<![<>=!])=(?!=)',
            '==',
            expr
        )

        # Convert column references
        expr = re.sub(
            r'\b([A-Za-z_][A-Za-z0-9_]*)\b',
            r'col("\1")',
            expr
        )

        return expr

    @staticmethod
    def convert_isnull(expr):

        return re.sub(
            r'ISNULL\((.*?)\)',
            r'col("\1").isNull()',
            expr,
            flags=re.IGNORECASE
        )

    # -------------------------------------------------------
    # IIF
    # -------------------------------------------------------

    @staticmethod
    def convert_iif(expr):

        match = re.match(
            r"IIF\((.*?),(.*?),(.*?)\)$",
            expr,
            flags=re.IGNORECASE
        )

        if not match:
            return expr

        condition = match.group(1).strip()
        true_value = match.group(2).strip()
        false_value = match.group(3).strip()

        condition = condition.replace("=", "==")

        return (
            f'when(expr("{condition}"), {true_value})'
            f'.otherwise({false_value})'
        )

    # -------------------------------------------------------
    # DECODE
    # -------------------------------------------------------

    @staticmethod
    def convert_decode(expr):

        if not expr.upper().startswith("DECODE("):
            return expr

        return "# TODO : Claude Conversion Required"