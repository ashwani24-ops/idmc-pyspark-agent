from pathlib import Path
from lxml import etree


class XMLReader:
    """Reads and validates XML files."""

    @staticmethod
    def read_xml(file_path: str):
        """
        Reads an XML file and returns the root element.

        Args:
            file_path (str): Path to the XML file.

        Returns:
            etree._Element: Root element of the XML.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"XML file not found: {file_path}")

        try:
            tree = etree.parse(str(path))
            return tree.getroot()
        except etree.XMLSyntaxError as ex:
            raise ValueError(f"Invalid XML: {ex}") from ex