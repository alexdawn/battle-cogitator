# suggests a turn is around 5 or so seconds
# allow for shooting and fighting too could be maybe 15-30 second per turn

SCALE = 64
INCH_TO_CM = 2.54

def to_real_scale(value):
    return value * SCALE * INCH_TO_CM / 100
to_real_scale(7 + 6 + 2 * 6) / 6
