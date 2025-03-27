import math

from l10n import translations as tr

from bio_scan.globals import bioscan_globals

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

    match color:
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


def translate_body(body_type: str) -> str:
    """
    Return translation for a given body type
    :param body_type: The ED journal string for a body type
    :return: The translated body type
    """

    match body_type:
        case 'Icy body':
            return tr.tl('Icy body', bioscan_globals.translation_context)  # LANG: Body type icy body
        case 'Rocky body':
            return tr.tl('Rocky body', bioscan_globals.translation_context)  # LANG: Body type rocky body
        case 'Rocky ice body':
            return tr.tl('Rocky ice body', bioscan_globals.translation_context)  # LANG: Body type rocky ice body
        case 'Metal rich body':
            return tr.tl('Metal rich body', bioscan_globals.translation_context)  # LANG: Body type metal rich body
        case 'High metal content body':
            return tr.tl('High metal content body', bioscan_globals.translation_context)  # LANG: Body type high metal content body
        case _:
            return body_type


def translate_genus(genus: str) -> str:
    """
    Return translation for a given genus
    :param genus: The ED journal string for a genus
    :return: The translated genus
    """

    match genus:
        case 'Aleoida':
            return tr.tl('Aleoida', bioscan_globals.translation_context)  # LANG: Genus aleoida
        case 'Bacterium':
            return tr.tl('Bacterium', bioscan_globals.translation_context)  # LANG: Genus bacterium
        case 'Cactoida':
            return tr.tl('Cactoida', bioscan_globals.translation_context)  # LANG: Genus cactoida
        case 'Clypeus':
            return tr.tl('Clypeus', bioscan_globals.translation_context)  # LANG: Genus clypeus
        case 'Concha':
            return tr.tl('Concha', bioscan_globals.translation_context)  # LANG: Genus concha
        case 'Electricae':
            return tr.tl('Electricae', bioscan_globals.translation_context)  # LANG: Genus electricae
        case 'Fonticulua':
            return tr.tl('Fonticulua', bioscan_globals.translation_context)  # LANG: Genus fonticula
        case 'Fumerola':
            return tr.tl('Fumerola', bioscan_globals.translation_context)  # LANG: Genus fumerola
        case 'Fungoida':
            return tr.tl('Fungoida', bioscan_globals.translation_context)  # LANG: Genus fungoida
        case 'Osseus':
            return tr.tl('Osseus', bioscan_globals.translation_context)  # LANG: Genus osseus
        case 'Recepta':
            return tr.tl('Recepta', bioscan_globals.translation_context)  # LANG: Genus recepta
        case 'Frutexa':
            return tr.tl('Frutexa', bioscan_globals.translation_context)  # LANG: Genus frutexa
        case 'Stratum':
            return tr.tl('Stratum', bioscan_globals.translation_context)  # LANG: Genus stratum
        case 'Tubus':
            return tr.tl('Tubus', bioscan_globals.translation_context)  # LANG: Genus tubus
        case 'Tussock':
            return tr.tl('Tussock', bioscan_globals.translation_context)  # LANG: Genus tussock
        case 'Anemone':
            return tr.tl('Anemone', bioscan_globals.translation_context)  # LANG: Genus anemone
        case 'Amphora Plant':
            return tr.tl('Amphora Plant', bioscan_globals.translation_context)  # LANG: Genus amphora plant
        case 'Bark Mound':
            return tr.tl('Bark Mound', bioscan_globals.translation_context)  # LANG: Genus bark mound
        case 'Brain Tree':
            return tr.tl('Brain Tree', bioscan_globals.translation_context)  # LANG: Genus brain tree
        case 'Crystalline Shards':
            return tr.tl('Crystalline Shards', bioscan_globals.translation_context)  # LANG: Genus crystalline shards
        case 'Sinuous Tubers':
            return tr.tl('Sinuous Tubers', bioscan_globals.translation_context)  # LANG: Genus sinuous tubers
        case _:
            return genus


def translate_species(species: str) -> str:
    """
    Return translation for a given species
    :param species: The ED journal string for a species
    :return: The translated species
    """

    match species:
        case 'Crystalline Shards':
            return tr.tl('Crystalline Shards', bioscan_globals.translation_context)  # LANG: Species crystalline shards
        case _:
            return species
