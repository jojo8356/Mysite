import sys
import inspect
from flask import *

sys.setrecursionlimit(1000)


class FunctionWrapperDecorator:
    def __init__(self, cls):
        global executed
        executed = False
        self.cls = cls

    def __call__(self, *args, **kwargs):
        function_names = [
            name for name, value in inspect.getmembers(self.cls, inspect.isfunction)
        ]
        for function_name in function_names:
            original_function = getattr(self.cls, function_name)
            wrapped_function = self.wrap(original_function)
            setattr(self.cls, function_name, wrapped_function)

        return self.cls(*args, **kwargs)

    def wrap(self, func):
        # Wrap the function
        def inner(self, *args, **kwargs):
            global executed
            if not executed:
                executed = True
                try:
                    self.verif_file()
                except:
                    pass
                # avt la fonction
            result = func(self, *args, **kwargs)
            # après la fonction
            return result

        return inner


def format_dictio(dictio):
    return {
        table: {key: value for x in dictio[table] for key, value in x.items()}
        for table in dictio
    }


def transform_tuples(lst):
    return [value[0] if value[0] is not None else "" for value in lst]


def format_data_for_sql(liste):
    return "(" + ", ".join([f"'{item.replace(' ','_')}'" for item in liste]) + ")"


def get_function_name():
    return inspect.stack()[1].function


def get_input(_input):
    return request.form[_input]


def get_roots():
    with open(__file__, "r") as file:
        lines = file.readlines()
    liste = [
        line.replace("def ", "").split("(")[0]
        for i, line in enumerate(lines)
        if "@app.route" in lines[i - 1] and "    " not in line and "app.rou" not in line
    ]
    return liste
