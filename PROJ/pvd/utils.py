import math

def get_range_tuple(difference):
    """
        Range lookup function. 
    """
    lower, upper = None, None

    if 0 <= difference <= 7:
        lower, upper = 0,7
    elif 8<= difference <=15:
        lower,upper = 8,15
    elif 16 <=difference <=31:
        lower,upper = 16,31
    elif 32 <= difference <=63:
        lower,upper = 32,63
    elif 64 <= difference <= 127:
        lower,upper = 64,127

    width = upper-lower+1
    t = math.log(width, 2)

    return lower, upper, width, t 
