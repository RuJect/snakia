from abc import ABC, abstractmethod
from typing import Any, MutableSequence, Sequence, final


class Random[S](ABC):
    @abstractmethod
    def bits(self, k: int) -> int: ...

    @abstractmethod
    def set_state(self, value: S) -> None: ...

    @abstractmethod
    def get_state(self) -> S: ...

    @final
    def bytes(self, n: int) -> bytes:
        """Return n random bytes."""
        return self.bits(n * 8).to_bytes(n, "little")

    @final
    def below(self, n: int) -> int:
        """Return a random int in the range [0,n). Defined for n > 0."""
        k = n.bit_length()
        while True:  # TODO: remove loop
            x = self.bits(k)
            if x < n:
                return x

    @final
    def int(self, start: int, end: int) -> int:
        """Return a random int in the range [start, end]."""
        return self.below(end + 1 - start) + start

    @final
    def float(self) -> float:
        """Return a random float in the range [0.0, 1.0)."""
        return self.bits(32) / (1 << 32)

    @final
    def choice[T](self, seq: Sequence[T]) -> T:
        """Return a random element from a non-empty sequence."""
        return seq[self.below(len(seq))]

    @final
    def shuffle[T: MutableSequence[Any]](self, seq: T) -> T:
        """Shuffle a sequence in place."""
        for i in range(len(seq) - 1, 0, -1):
            j = self.below(i + 1)
            seq[i], seq[j] = seq[j], seq[i]
        return seq
