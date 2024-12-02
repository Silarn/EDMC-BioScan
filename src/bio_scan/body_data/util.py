from typing import Optional

from ExploData.explo_data.body_data.struct import PlanetData


def get_body_shorthand(body_type: str) -> str:
    """
    Return a shorthand for a given body type
    :param body_type: The ED journal string for a body type
    :return: A shorthand string representing the given body type
    """

    match body_type:
        case 'Icy body':
            return ' (I)'
        case 'Rocky body':
            return ' (R)'
        case 'Rocky ice body':
            return ' (RI)'
        case 'Metal rich body':
            return ' (MR)'
        case 'High metal content body':
            return ' (HMC)'
        case _:
            return ''


def body_check(required_types: list[str], bodies: dict[str, PlanetData]) -> bool:
    """
    Basic search function to check if one of the given body types is present in a dictionary of planet data.

    :param required_types: A list of ED Journal body type strings to search for
    :param bodies: A dictionary of planets names and ExploData PlanetData objects to search
    :return: Whether or not one of the required body types was found
    """

    for _, body_data in bodies.items():
        if body_data.get_type() in required_types:
            return True
    return False


def get_gravity_warning(gravity: Optional[float], with_gravity: bool = False) -> str:
    """
    Get gravity warning string based on provided gravity value. 2.7G is extreme gravity. 1G is high gravity.

    :param gravity: Surface gravity of a planet (in m/s^2)
    :param with_gravity: Whether or not to include the gravity value (in Gs)
    :return: Gravity warning string. ![#]G! for extreme gravity, ^[#]G^ for high gravity.
    """

    if gravity:
        g_gravity = round(gravity / 9.80665, 2)
        if g_gravity > 2.69:
            return f' !{g_gravity}G!' if with_gravity else ' !G!'
        if g_gravity >= 1.0:
            return f' ^{g_gravity}G^' if with_gravity else ' ^G^'
        return f' {g_gravity}G' if with_gravity else ''
    return ''


def star_check(star_query: str, star_type: str) -> bool:
    """
    Check if the given star type string (by ED journal value) matches a base type identifier.

    This is necessary because super giants have different type IDs from standard stars and certain star types have
    variations with qualifiers where a basic equality comparison is insufficient.

    :param star_query: Simple star type string (A, F, K, O, D, H, etc.)
    :param star_type: ED journal type string for comparison star
    :return: Whether the basic query type matches the ED journal type string
    """

    match star_query:
        case 'A':
            return star_type in ['A', 'A_BlueWhiteSuperGiant']
        case 'B':
            return star_type in ['B', 'B_BlueWhiteSuperGiant']
        case 'F':
            return star_type in ['F', 'F_WhiteSuperGiant']
        case 'G':
            return star_type in ['G', 'G_WhiteSuperGiant']
        case 'K':
            return star_type in ['K', 'K_OrangeGiant']
        case 'M':
            return star_type in ['M', 'M_RedGiant', 'M_RedSuperGiant']
        case 'D' | 'C' | 'W':
            return star_type.startswith(star_query)
        case _:
            return star_type == star_query
