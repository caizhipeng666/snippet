from enum import Enum
from functools import partial


class Gate(Enum):

    # Fails at the first error or exception thrown from a job. (Default)
    FAIL_FAST = partial(lambda: True)
    # Silently captures the error or exception to execute all the jobs.
    EXECUTE_ALL = partial(lambda: True)


print(Gate.FAIL_FAST.value())
