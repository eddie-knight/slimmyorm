import mysql.connector

from .mysql_connection import MysqlConnection


connection = MysqlConnection()


class Select:
    """
    Build and run a select statement.
    Statement can be run using all() or one()
    Connection resets after each run, so
    a Select can be modified and/or re-run.
    Modify by targeting an attribute, then
    use build_select_statement() before re-run
    """

    def __init__(self,
                 target,
                 table,
                 multi=False,  # Non-specific order if multi-word names
                 db_id="",
                 name=False,
                 where=False):
        self.target = target
        self.table = table
        self.id = db_id
        self.name = name
        self.where = where if where else ""
        self.multi = multi
        self.build_select_statement()

    def all(self):
        try:
            data = connection.fetch_all(self.statement)
        except mysql.connector.ProgrammingError as e:
            return {"Error": str(e)}
        return data

    def one(self):
        try:
            data = connection.fetch_one(self.statement)
        except mysql.connector.ProgrammingError as e:
            return {"Error": str(e)}
        return data

    def build_select_statement(self):
        if self.name:  # for imprecise searches
            self.format_name_search()
        if self.id or self.where or self.name:
            self.format_where_statement()
        self.parse_statement()
        return self.statement

    def parse_statement(self):
        self.statement = f"SELECT {self.target} FROM {self.table} {self.where}"

    def format_name_search(self):
        """ Find literal, or %x% search. """
        if not self.name:
            return

        if not self.multi:
            self.name = f"name='{self.name}'"
            return

        statement = f"name LIKE '%{self.name}%'"
        # split line to search mis-arranged words
        line = self.name.replace(",", "")
        words = line.split()
        if len(words) < 2:
            self.name = statement
            return

        first = True
        stmt = statement
        for word in words:
            if first:
                first = False
                stmt = f"{stmt} OR ((INSTR(name, '{word}') > 0)"
            else:
                stmt = f"{stmt} AND (INSTR(name, '{word}') > 0)"
        self.name = f"{stmt})"

    def format_where_statement(self):
        """ Search by id, name, or provided search value """
        if self.id:  # Intentionally overwrites 'where' value
            statement = f"WHERE id='{self.id}'"
        elif self.name and self.where:
            statement = f"WHERE {self.name} AND {self.where}"
        elif self.where and not self.name:
            statement = f"WHERE {self.where}"
        else:
            statement = f"WHERE {self.name}"
        self.where = statement