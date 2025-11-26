from typing import Any, Callable, Literal, ParamSpec, TypeVar, final, overload

from typing_extensions import Self

from snakia.utils import get_attrs, get_or_set_attr

T = TypeVar("T")
M = TypeVar("M", bound="Marker")
P = ParamSpec("P")

MARKERS_ATTR = "__snakia_markers__"


def _get_all_markers(obj: Any) -> dict[type["Marker"], "Marker"]:
    return get_or_set_attr(obj, MARKERS_ATTR, dict())


class Marker:
    @overload
    @classmethod
    def get(cls, obj: Any, default: None = None) -> Self: ...
    @overload
    @classmethod
    def get(cls, obj: Any, default: T) -> Self | T: ...
    @final
    @classmethod
    def get(cls, obj: Any, default: Any = None) -> Any:
        markers = _get_all_markers(obj)
        return markers.get(cls, default)

    @final
    @classmethod
    def has(cls, obj: Any) -> bool:
        if not hasattr(obj, MARKERS_ATTR):
            return False
        _marker = obj.__dict__[MARKERS_ATTR].get(cls, None)
        return isinstance(_marker, cls)

    @final
    def set_mark(self, obj: T) -> T:
        markers = _get_all_markers(obj)
        markers[self.__class__] = self
        return obj

    @final
    @classmethod
    def mark(cls, *a: Any, **kw: Any) -> Callable[[T], T]:
        def inner(obj: T) -> T:
            return cls(*a, **kw).set_mark(obj)

        return inner

    @final
    @classmethod
    def unmark(cls, obj: T) -> T:
        markers = _get_all_markers(obj)
        if cls in markers:
            del markers[cls]
        return obj

    @overload
    @classmethod
    def get_marks(
        cls, container: Any, *, only_values: Literal[False] = False
    ) -> dict[str, tuple[Any, Self]]: ...
    @overload
    @classmethod
    def get_marks(
        cls, container: Any, *, only_values: Literal[True]
    ) -> dict[str, Self]: ...
    @final
    @classmethod
    def get_marks(
        cls, container: Any, *, only_values: bool = False
    ) -> dict[str, tuple[Any, Self]] | dict[str, Self]:
        markers = {}
        for k, v in get_attrs(container).items():
            if not cls.has(v):
                continue
            _marker = cls.get(v)
            if _marker is not None:
                markers[k] = _marker if only_values else (v, _marker)
        return markers  # type: ignore


def marker() -> type[Marker]:
    return type("<anonym marker>", (Marker,), {})


def mark(
    func: Callable[P, Marker], /, *args: P.args, **kwargs: P.kwargs
) -> Callable[[T], T]:
    def inner(obj: T) -> T:
        return func(*args, **kwargs).set_mark(obj)

    return inner
