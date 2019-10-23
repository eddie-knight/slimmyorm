from .select import Select


def search(self, table, name=False, db_id=False, where=False):
    slct = Select('*', table, multi=True, db_id=db_id, name=name, where=where)
    data = slct.all()
    if data == []:
        return {"Error": f"'{name}' not found when searching"}
    return data


def search_high_low(table, column, name=False, high=False, low=False):
    # Ensure at least one has a value
    if not isinstance(high, int) and not isinstance(low, int):
        return {"Error": "Please provide a high or low value"}

    high_limit = f"{column} <= {high}" if high else ""
    low_limit = f"{column} >= {low}" if low else ""

    if high_limit and low_limit:  # If both have a value
        where = f"{high_limit} AND {low_limit}"
    else:
        where = high_limit + low_limit  # If one is empty string

    data = Select('*', table, multi=True, name=name, where=where).all()

    if data == []:
        return {"Error": f"'{name}' not found when searching"}
    return data
