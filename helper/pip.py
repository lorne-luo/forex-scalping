from math import fabs


def get_pip(value1, value2=0, abs=False):
    places = 4 if value1 < 10 else 2
    value = value1 - value2
    value = value * 10 ** places
    if abs:
        value = fabs(value)
    format = "{0:.%sf}" % places
    value = float(format.format(value))
    return value


if __name__ == "__main__":
    print(get_pip(109.44, 108.33))
    print(get_pip(1.2734, 1.2787))
