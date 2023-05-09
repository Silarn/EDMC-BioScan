from bio_scan.body_data.struct import PlanetData


def get_body_shorthand(body_type: str) -> str:
    match body_type:
        case 'Icy body':
            return ' (I)'
        case 'Rocky body':
            return ' (R)'
        case 'Rocky ice body':
            return ' (RI)'
        case 'Metal rich body':
            return ' (M)'
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


def get_gravity_warning(gravity: float) -> str:
    g_gravity = round(gravity / 9.80665, 2)
    if g_gravity > 2.69:
        return ' !G!'
    if g_gravity >= 1.0:
        return ' ^G^'
    return ''
