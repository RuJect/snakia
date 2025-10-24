def singleton[T](cls: type[T]) -> T:
    return cls()
