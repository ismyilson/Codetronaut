import sys
import inspect


def get_classes_in_module(module_name, subclass_of=None):
    classes = []
    check_subclass = False if subclass_of is None else True

    module = sys.modules[module_name]
    for c in dir(module):
        klass = getattr(module, c)

        if not inspect.isclass(klass):
            continue

        if check_subclass:
            if not issubclass(klass, subclass_of):
                continue

        if klass is subclass_of:
            continue

        classes.append(klass)

    return classes
