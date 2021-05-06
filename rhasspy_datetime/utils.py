def round_to_x_minutes(minutes, base):
    """
    input a value in minutes
    return: a float rounded to the nearest 15min interval
            if base is 15 for example
    """
    rounded = base * int(float(minutes)/base)
    if rounded == 60.0:
        rounded = 0.0
    return int(rounded)
