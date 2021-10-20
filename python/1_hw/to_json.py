from functools import wraps
import json


def to_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data_to_convert = func(*args, **kwargs)
        converted_data = json.dumps(data_to_convert)
        return converted_data
    return wrapper


@to_json
def get_data():
    return {
        'data': 42
    }


print(get_data())
print(type(get_data()))
print(get_data.__name__)
