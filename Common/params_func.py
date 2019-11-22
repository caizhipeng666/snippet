from enum import Enum
from functools import partial


class Gate(Enum):
    FAIL_FAST = partial(lambda: True)
    EXECUTE_ALL = partial(lambda: True)


print(Gate.FAIL_FAST.value())
