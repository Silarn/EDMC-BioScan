import math


def system_distance(coordinate_a: tuple[float, float, float], coordinate_b: tuple[float, float, float]) -> float:
    return math.sqrt((coordinate_a[0] - coordinate_b[0]) ** 2
                     + (coordinate_a[1] - coordinate_b[0]) ** 2
                     + (coordinate_a[2] - coordinate_b[0]) ** 2)
