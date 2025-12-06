from datetime import datetime
import sys

def log(s: str):
    now = datetime.now()
    timestamp = now.strftime("%H:%M:%S.%f")[:-3]  # truncate microseconds to milliseconds
    print(f"i[{timestamp}] {s}", file=sys.stderr)

def warn(s: str):
    now = datetime.now()
    timestamp = now.strftime("%H:%M:%S.%f")[:-3]  # truncate microseconds to milliseconds
    print(f"W[{timestamp}] WARN: {s}", file=sys.stderr)

def event(s: str):
    now = datetime.now()
    timestamp = now.strftime("%H:%M:%S.%f")[:-3]  # truncate microseconds to milliseconds
    print(f"e[{timestamp}] {s}", file=sys.stderr)

def is_scalar(v):
    return not isinstance(v, (dict, list, set, tuple))

def dmerge(d1: dict, d2: dict):
    """Merge d2 into d1 destructively.
    Non-scalars win over scalars; d1 wins on scalar conflicts."""

    result = d1.copy()
    for key, value in d2.items():
        if key in result:
            v1, v2 = result[key], value
            # Both dicts: recursive merge
            if isinstance(v1, dict) and isinstance(v2, dict):
                result[key] = dmerge(v1, v2)
            # Both lists: concatenate
            elif isinstance(v1, list) and isinstance(v2, list):
                result[key] = v1 + v2
            # One scalar, one non-scalar: non-scalar wins
            elif is_scalar(v1) and not is_scalar(v2):
                result[key] = v2  # d2's non-scalar wins
            elif not is_scalar(v1) and is_scalar(v2):
                result[key] = v1  # d1's non-scalar wins
            # Both scalars: d1 wins (keep result[key])
        else:
            result[key] = value
    return result


