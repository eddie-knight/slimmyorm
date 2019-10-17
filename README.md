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

`Select(target, table, multi=False, db_id="", name=False, where=False):`

This prepares your statement, but does not run a query against the database.

#### Multi-use or single-use Select usage

Assign the result of `Select()` to a variable if you would like to run multiple methods on the same statement. Append a method to the end of the initialization to jump straight into your query.

Example of multiple queries with a single statement:
```
query = slimmyorm.Select('*', table) # prepares statement to query all columns for all rows in a table
first_result = query.one() # Gets the first row found
all_results = query.all() # Gets all rows from table
```
Example of a quick-use select query:
```
current_user = slimmyorm.Select('*', 'users', name=username).one()
```

## Search

`search(self, table, name=False, db_id=False where=False)`

Sometimes you just need to find an item by name. Or by id. That should be way easier than it is with more robust tools.

Example of searching by name and id:
```
all_the_bobs = slimmyorm.search('users', name='bob')
user_with_id = slimmyorm.search('users', db_id=123)
bob_with_id = slimmyorm.search('users', name='bob', db_id=123)
```

Sometimes you need just need to get entries that are above, below, or within a certain integer limit.

Here is an example where I want to check the "price" column in my "sodas" table:
```
expensive_pop = slimmyorm.search_high_low('sodas', 'price', low=1000)
cheap_pop = slimmyorm.search_high_low('sodas', 'price', high=1)
all_the_other_pop = slimmyorm.search_high_low('sodas', 'price', low=2, high=999)
```

Other times, you may need to get a bit more creative with your searching.

Here are a some examples:
```
crazy_bobs = slimmyorm.search('users', name='bob', where="children>4")
```
```
where="children > 1 AND children < 5"
reasonable_bobs = slimmyorm.search('users', name='bob', where=where)
```
```
where="name LIKE %bob% AND children=0 AND fish=1 AND languages>2"
complex_bobs = slimmyorm.search('users', where=where)
```
