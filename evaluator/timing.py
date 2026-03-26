


def timing_error(expected_time, actual_time):

    error = actual_time - expected_time

    if abs(error) < 0.2:
        return "perfect"

    if error < 0:
        return "early"

    return "late"