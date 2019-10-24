import json

from pathlib import Path

from .insert import dict_to_table_insert


class SlimMyJson:
    def __init__(self, json_dir='json', excluded=[]):
        self._target = Path.cwd().rglob(f"{json_dir}/*.json")
        self._excluded = excluded
        self.results = []
        self._json_dir_to_list()
        self._insert_tables()

    def _json_dir_to_list(self):
        """ Loads all .json files in json_dir """
        self._file_contents = [
            json.loads(path.read_text())
            for path in self._target
        ]  # Gets contents of all .json files

    def _insert_tables(self):
        """
        Expects associative data in each file
        ie. { "table_name" : {...} }
        """
        for file in self._file_contents:
            for key in file:
                table = file[key]
                if key in self._excluded:
                    continue  # Skip unsupported table
                result = dict_to_table_insert(key, table)
                self.results.append(result)
