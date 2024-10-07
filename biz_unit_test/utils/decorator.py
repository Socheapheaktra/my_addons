from functools import wraps
from marshmallow import Schema


class Blueprint:
    def argument(self, schema):
        """
        Handling arguments passed into a function

        :param Schema schema: Marshmallow Schema
        :raise ValidationError: When data is failed to validate
        :return: func
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                data = self.load_schema(schema=schema, data=kwargs)
                return func(*args, **data)
            return wrapper
        return decorator

    @staticmethod
    def load_schema(schema, data):
        """
        Load Data from Schema

        :param Schema schema: Marshmallow Schema
        :param dict data: Data to Load
        :return: Validated Data
        :rtype: dict | list[dict]
        """
        return schema.load(data, unknown="include")


blueprint = Blueprint()
