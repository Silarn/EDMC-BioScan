import math


def system_distance(coordinate_a: tuple[float, float, float], coordinate_b: tuple[float, float, float]) -> float:
    """
    Calculate distance between 3D coordinates

    :param coordinate_a: x, y, z tuple
    :param coordinate_b: x, y, z tuple
    :return: Calculated distance between a and b
    """

    return math.sqrt((coordinate_a[0] - coordinate_b[0]) ** 2
                     + (coordinate_a[1] - coordinate_b[1]) ** 2
                     + (coordinate_a[2] - coordinate_b[2]) ** 2)
