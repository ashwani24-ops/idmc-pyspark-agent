import json


class IRReader:

    @staticmethod
    def read(file_path):

        with open(file_path, "r", encoding="utf-8") as fp:

            return json.load(fp)