# suggests a turn is around 5 or so seconds
# allow for shooting and fighting too could be maybe 15-30 second per turn

SCALE = 64
INCH_TO_CM = 2.54
SECONDS_PER_TURN = 10


def to_real_scale(value: float) -> float:
    """Convert to scale in meters"""
    return value * SCALE * INCH_TO_CM / 100


def to_cm(value: float) -> float:
    """Convert table inches to cm"""
    return value * INCH_TO_CM


def to_seconds(value: float) -> float:
    """Convert turn count to seconds"""
    return value * SECONDS_PER_TURN
