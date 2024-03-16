from typing import Optional

from ExploData.explo_data.body_data.struct import PlanetData


def get_body_shorthand(body_type: str) -> str:
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


def body_check(bodies: dict[str, PlanetData], extra: bool = False) -> bool:
    required_types = [
        'Earthlike body',
        'Gas giant with water based life',
        'Gas giant with ammonia based life'
    ]
    if extra:
        required_types += [
            'Ammonia world',
            'Water world',
            'Water giant',
            'Water giant with life',
        ]
    for _, body_data in bodies.items():
        if body_data.get_type() in required_types:
            return True
    return False


def get_gravity_warning(gravity: Optional[float], with_gravity: bool = False) -> str:
    if gravity:
        g_gravity = round(gravity / 9.80665, 2)
        if g_gravity > 2.69:
            return f'!{g_gravity}G!' if with_gravity else ' !G!'
        if g_gravity >= 1.0:
            return f' ^{g_gravity}G^' if with_gravity else ' ^G^'
        return f' {g_gravity}G' if with_gravity else ''
    return ''


def star_check(star_query: str, star_type: str) -> bool:
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
