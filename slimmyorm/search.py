from .select import Select

def search(self, table, name, where=False):
    data = Select('*', table, multi=True, name=name, where=where).all()
    if data == []:
        return {"Error": f"'{name}' not found when searching"}
    return data

def search_high_low(self, table, column, number, high=False, low=False):
    if not high and not low:
        return {"Error": "Please provide a high or low value"}
    if high:
        search = f"{column} <= {maximum_price}"
    data = Select('*', table, multi=True, name=name, where=where).all()
    if data == []:
        return {"Error": f"'{name}' not found when searching"}
    return data