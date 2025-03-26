import math

from l10n import translations as tr

from .globals import bioscan_globals

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


def translate_colors(color: str) -> str:
    """
    Translates color strings

    :param color: Original (UK English) color
    :return: Translated color
    """

    match str:
        case 'Amethyst':
            return tr.tl('Amethyst', bioscan_globals.translation_context)  # LANG: Color amethyst
        case 'Aquamarine':
            return tr.tl('Aquamarine', bioscan_globals.translation_context)  # LANG: Color aquamarine
        case 'Blue':
            return tr.tl('Blue', bioscan_globals.translation_context)  # LANG: Color blue
        case 'Cobalt':
            return tr.tl('Cobalt', bioscan_globals.translation_context)  # LANG: Color cobalt
        case 'Cyan':
            return tr.tl('Cyan', bioscan_globals.translation_context)  # LANG: Color cyan
        case 'Emerald':
            return tr.tl('Emerald', bioscan_globals.translation_context)  # LANG: Color emerald
        case 'Gold':
            return tr.tl('Gold', bioscan_globals.translation_context)  # LANG: Color gold
        case 'Green':
            return tr.tl('Green', bioscan_globals.translation_context)  # LANG: Color green
        case 'Grey':
            return tr.tl('Grey', bioscan_globals.translation_context)  # LANG: Color grey
        case 'Indigo':
            return tr.tl('Indigo', bioscan_globals.translation_context)  # LANG: Color indigo
        case 'Lime':
            return tr.tl('Lime', bioscan_globals.translation_context)  # LANG: Color lime
        case 'Magenta':
            return tr.tl('Magenta', bioscan_globals.translation_context)  # LANG: Color magenta
        case 'Maroon':
            return tr.tl('Maroon', bioscan_globals.translation_context)  # LANG: Color maroon
        case 'Mauve':
            return tr.tl('Mauve', bioscan_globals.translation_context)  # LANG: Color mauve
        case 'Mulberry':
            return tr.tl('Mulberry', bioscan_globals.translation_context)  # LANG: Color mulberry
        case 'Ocher':
            return tr.tl('Ocher', bioscan_globals.translation_context)  # LANG: Color ocher
        case 'Orange':
            return tr.tl('Orange', bioscan_globals.translation_context)  # LANG: Color orange
        case 'Peach':
            return tr.tl('Peach', bioscan_globals.translation_context)  # LANG: Color peach
        case 'Red':
            return tr.tl('Red', bioscan_globals.translation_context)  # LANG: Color red
        case 'Sage':
            return tr.tl('Sage', bioscan_globals.translation_context)  # LANG: Color sage
        case 'Teal':
            return tr.tl('Teal', bioscan_globals.translation_context)  # LANG: Color teal
        case 'Turquoise':
            return tr.tl('Turquoise', bioscan_globals.translation_context)  # LANG: Color turquoise
        case 'White':
            return tr.tl('White', bioscan_globals.translation_context)  # LANG: Color white
        case 'Yellow':
            return tr.tl('Yellow', bioscan_globals.translation_context)  # LANG: Color yellow
        case _:
            return color
