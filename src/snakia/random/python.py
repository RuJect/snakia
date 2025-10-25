import random

from .random import Random

type _State = tuple[int, tuple[int, ...], int | float | None]


class PythonRandom(Random[_State]):
    def bits(self, k: int) -> int:
        return random.getrandbits(k)

    def get_state(self) -> _State:
        return random.getstate()

    def set_state(self, value: _State) -> None:
        random.setstate(value)
