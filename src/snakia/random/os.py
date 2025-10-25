import os

from .random import Random


class OSRandom(Random[None]):
    """
    A random number generator that uses the OS (cryptographically secure) to generate random bytes.
    """

    def bits(self, k: int) -> int:
        return int.from_bytes(os.urandom((k + 7) // 8)) & ((1 << k) - 1)

    def get_state(self) -> None:
        return None

    def set_state(self, value: None) -> None:
        pass
