from .select import Select


class BaseData():
    def __init__(self, name=False, data=False):
        """ Either name or data must be provided """
        if name:
            self.name = name
        if data:
            self.set_attributes(data)
        else:
            self.set_attributes(self.get_base_data())
        self.setup()

    def setup(self):
        """ Placeholder """

    def get_base_data(self):
        """ Select row from table by name """
        return Select('*', self._table, name=self.name).one()

    def set_attributes(self, data):
        """ Get table data and set columns as attributes """
        try:
            for name in data:
                setattr(self, name, data[name])
        except BaseException as e:
            self.error = str(e)

    def list_public_attributes(self):
        """ Return non-callable non-private attributes """
        return [attribute for attribute, value in vars(self).items() if
                not (attribute.startswith('_') or callable(attribute))]

    def data(self):
        """ Format all attributes into a dictionary """
        data = {}
        for attribute in self.list_public_attributes():
            data[attribute] = getattr(self, attribute)
        return data

    def associative_data(self):
        """ Return an object associated by name """
        data = self.data()
        if data:
            data.pop('name')
            return {self.name: data}

    def remove_attribute(self, attribute):
        """ Delete a single attribute """
        if hasattr(self, attribute):
            delattr(self, attribute)

    def remove_attributes(self, attribute_list):
        """ Delete a list of attributes """
        for attribute in attribute_list:
            self.remove_attribute(attribute)
