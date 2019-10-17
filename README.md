# SlimMyORM

Mysql is capable of a million things. [`mysql-connector-python`](https://github.com/mysql/mysql-connector-python) allows you to do all of those things. **But sometimes we don't need all the things.** This package slims down the complexities of mysql into a few key options that are necessary for simple application logic.

Use the `MysqlConnector` to run raw statements, or use the `Select` object to do a bit of pre-parsing for you when you need to read information from the database.

## ORM

The `ORM` object makes a minimalistic connection to your mysql database. Connection information must be provided via environment variables. I prefer to use a `.env` file that is specified in my `docker-compose.yml`, but you can google any number of solutions for your preferred deployment.

```
ORM = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    port=os.getenv('MYSQL_PORT', "3306"),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=DB_NAME)
```

## MysqlConnection

This object utilizes the aforementioned `ORM` connection.

- `run_statement(statement, multi=False)` - This is at the core of inserting and fetching data. If `mutli` is left to `False`, it will protect from any `;` that might sneak in to your statements. Leaves the cursor open and uncommitted.

- `insert(statement, multi=False)` - Commits a statement (or multiple statements) and then immediately closes the cursor. Use `multi=True` only if you have properly cleaned your incoming data from potentially malicious or malfunctioning input.

- `update(statement, multi=False)` - Pseudonym for `insert`.

- `fetch_one(statement)` - Commits a statment and then immediately returns the first row from the results, if any are found.

- `fetch_all(statement)` - Commits a statment and then immediately returns all results, if any are found.

## Select

This object utilizes the aforementioned `ORM` connection.

```Select(target, table, multi=False, db_id="", name=False, where=False):``` 

This prepares your statement, but does not run a query against the database.

Assign the result of `Select()` to a variable if you would like to run multiple methods on the same statement. Append a method to the end of the initialization to jump straight into your query.

Example:
```
query = Select(target, table) # prepares statement to query a table for an object by name
first_result = query.one() # Runs fetch_one using the prepared statement
all_results = query.all() # Runs fetch_all using the prepared statement
```
