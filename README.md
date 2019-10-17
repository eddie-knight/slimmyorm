# SlimMyORM

Mysql is capable of a million things. [`mysql-connector-python`](https://github.com/mysql/mysql-connector-python) allows you to do all of those things. **But sometimes we don't need all the things.** This package slims down the complexities of mysql into a few key options that are necessary for simple application logic.

Use the `MysqlConnector` to run raw statements, or use the `Select` object to do a bit of pre-parsing for you when you need to read information from the database.

As a bonus, slimmyorm features a helpful `BaseData` class as a super-general catch all that can be extended for all your data modelling needs. 

See below for more information on the SlimMyORM features.

*****

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

## BaseData

Building data models sucks. This class object simplifies that.

The `BaseData` model will take any row of data and turn it into a python object that you can manipulate however you need.

After the object is initialized (either with a data dict, or with a name to query from its table), every column and it's data become attributes on this object.

_**NOTE:** This is specifically designed to be extended. See below for examples._

- `_table` - When extending this class, be sure to add a `_table` value that can be used for fetching data.
- `__init__` - You may override this and use the `Super` functionality, but often it is better to simply add your setup logic to your own `setup()` method, which will be automatically called at the end of `__init__`
    - `name=False` - If you don't pass data when defining this object, it can automaticaly build itself by querying a row on the `_table` that has an exact match to in the `name` column. Further, if the row you're querying does not have a name, you may choose to manually add it using this parameter.
    - `data=False` - You will usually already have the data row from a `Select()` query. If so, pass that object in here to avoid hitting the database unecessarily.
- `setup` - This is automatically run at the end of `__init__`. It has no default logic, and is there specifically for building logic that is specific to different data types.
- `set_attributes` - This transforms data into attributes whenever data is added, but you can also manually run it to add a data set as attributes on this object.
- `data` - This will give a flat dictionary object that contains each attribute as a key-value pair.
- `associative_data` - This will give an associative dictionary with the row's `name` as the top level of the object.
- `remove_attribute` - Similar to popping a dict entry. Use this if you don't want a delete a particular piece of data before getting the final data output.
- `remove_attributes` - Same as above, but accepts a list.

Simple Example:

```
from slimmyorm.base_data import BaseData

class ArmorData(BaseData):
    _table = "armor"

    def setup(self):
        self.remove_attribute('id')

# Usage:

example_object = ArmorData('second skin')
print(ArmorData.name)  # output: "Second Skin"
print(ArmorData.type)  # output: "light armor"
print(ArmorData.data())

#  output:
#  {
#    "name": "Second Skin",
#    "type": "light armor",
#    "level": 2,
#    "id": 17
#  }
```

Complex Example:
```
from slimmyorm.base_data import BaseData
from slimmyorm.select import Select


class WeaponData(BaseData):
    def __init__(self, name=False, table=False, data=False, category=False):
        self._table = table
        if data and category:
            data['category'] = category
        super(WeaponData, self).__init__(name, data)

    def setup(self):
        self.set_category()
        self.remove_attribute('id')

    def set_category(self):
        if not hasattr(self, 'category'):
            return
        if not isinstance(self.category, str):
            data = Select(
                'category', 'weapon_categories', where=f'id={self.category}'
                ).one()
            self.category = data['category'].title()
```