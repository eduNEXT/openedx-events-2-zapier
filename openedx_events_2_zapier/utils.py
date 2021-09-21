"""
Utilities used by Open edX Events Receivers.
"""
import collections

from opaque_keys.edx.locator import CourseLocator


def flatten_dict(d, parent_key='', sep='_'):
    """
    This function returns a flatten dictionary-like object.
    """
    items = []
    for key, value in d.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, collections.MutableMapping):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def serialize_course_key(inst, field, value):  # pylint: disable=unused-argument
    """
    Serializes instances of CourseLocator, when value is anything else returns it
    without modification.
    """
    if isinstance(value, CourseLocator):
        return str(value)
    return value
