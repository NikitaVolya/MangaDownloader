
class Counter:

    def __init__(self, value: int):
        self._value: int = value

    def __add__(self, value: int):
        self._value += value

    @property
    def Value(self) -> int:
        return self._value
