from typing import Any, NoReturn, overload

from snakia.types.unset import Unset


@overload
def throw[T: Exception](
    *exceptions: T,  # pyright: ignore[reportInvalidTypeVarUse]
    from_: Unset | BaseException = Unset(),
) -> NoReturn: ...


@overload
def throw(
    exception: BaseException, from_: Unset | BaseException = Unset(), /
) -> NoReturn: ...


def throw(
    *exceptions: Any, from_: Unset | BaseException = Unset()
) -> NoReturn:
    """Throw an exception."""
    if isinstance(from_, Unset):
        if len(exceptions) == 1:
            raise exceptions[0]
        raise ExceptionGroup("", exceptions)
    else:
        if len(exceptions) == 1:
            raise exceptions[0] from from_
        raise ExceptionGroup("", exceptions) from from_
