from sys import stderr


def eprint(*args, **kwargs):
    """
    Passes arguments and keyword argumenst to the "print"-function,
    and then redirects the output to "stderr".
    """
    print(*args, file=stderr, **kwargs)


def parse_int(string):
    """
    Attempts parsing a string to an int to then return it.
    Returns None if unsuccessful.
    """
    try:
        #Attempt parsing string to int
        return int(string)
    except ValueError:
        return None

def parse_float(string):
    """
    Attempts parsing a string to a float to then return it.
    Returns None if unsuccessful.
    """
    try:
        #Attempt parsing string to float
        return float(string)
    except ValueError:
        return None
