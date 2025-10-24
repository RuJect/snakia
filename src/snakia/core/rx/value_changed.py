from typing import NamedTuple


class ValueChanged[T](NamedTuple):
    old_value: T
    new_value: T
