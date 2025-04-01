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
        case 'Aleoida Arcus':
            return tr.tl('Aleoida Arcus', bioscan_globals.translation_context)
        case 'Aleoida Coronamus':
            return tr.tl('Aleoida Coronamus', bioscan_globals.translation_context)
        case 'Aleoida Spica':
            return tr.tl('Aleoida Spica', bioscan_globals.translation_context)
        case 'Aleoida Laminiae':
            return tr.tl('Aleoida Laminiae', bioscan_globals.translation_context)
        case 'Aleoida Gravis':
            return tr.tl('Aleoida Gravis', bioscan_globals.translation_context)
        case 'Luteolum Anemone':
            return tr.tl('Luteolum Anemone', bioscan_globals.translation_context)
        case 'Croceum Anemone':
            return tr.tl('Croceum Anemone', bioscan_globals.translation_context)
        case 'Puniceum Anemone':
            return tr.tl('Puniceum Anemone', bioscan_globals.translation_context)
        case 'Roseum Anemone':
            return tr.tl('Roseum Anemone', bioscan_globals.translation_context)
        case 'Rubeum Bioluminescent Anemone':
            return tr.tl('Rubeum Bioluminescent Anemone', bioscan_globals.translation_context)
        case 'Prasinum Bioluminescent Anemone':
            return tr.tl('Prasinum Bioluminescent Anemone', bioscan_globals.translation_context)
        case 'Roseum Bioluminescent Anemone':
            return tr.tl('Roseum Bioluminescent Anemone', bioscan_globals.translation_context)
        case 'Blatteum Bioluminescent Anemone':
            return tr.tl('Blatteum Bioluminescent Anemone', bioscan_globals.translation_context)
        case 'Bacterium Aurasus':
            return tr.tl('Bacterium Aurasus', bioscan_globals.translation_context)
        case 'Bacterium Nebulus':
            return tr.tl('Bacterium Nebulus', bioscan_globals.translation_context)
        case 'Bacterium Scopulum':
            return tr.tl('Bacterium Scopulum', bioscan_globals.translation_context)
        case 'Bacterium Acies':
            return tr.tl('Bacterium Acies', bioscan_globals.translation_context)
        case 'Bacterium Vesicula':
            return tr.tl('Bacterium Vesicula', bioscan_globals.translation_context)
        case 'Bacterium Alcyoneum':
            return tr.tl('Bacterium Alcyoneum', bioscan_globals.translation_context)
        case 'Bacterium Tela':
            return tr.tl('Bacterium Tela', bioscan_globals.translation_context)
        case 'Bacterium Informem':
            return tr.tl('Bacterium Informem', bioscan_globals.translation_context)
        case 'Bacterium Volu':
            return tr.tl('Bacterium Volu', bioscan_globals.translation_context)
        case 'Bacterium Bullaris':
            return tr.tl('Bacterium Bullaris', bioscan_globals.translation_context)
        case 'Bacterium Omentum':
            return tr.tl('Bacterium Omentum', bioscan_globals.translation_context)
        case 'Bacterium Cerbrus':
            return tr.tl('Bacterium Cerbrus', bioscan_globals.translation_context)
        case 'Bacterium Verrata':
            return tr.tl('Bacterium Verrata', bioscan_globals.translation_context)
        case 'Roseum Brain Tree':
            return tr.tl('Roseum Brain Tree', bioscan_globals.translation_context)
        case 'Gypseeum Brain Tree':
            return tr.tl('Gypseeum Brain Tree', bioscan_globals.translation_context)
        case 'Ostrinum Brain Tree':
            return tr.tl('Ostrinum Brain Tree', bioscan_globals.translation_context)
        case 'Viride Brain Tree':
            return tr.tl('Viride Brain Tree', bioscan_globals.translation_context)
        case 'Aureum Brain Tree':
            return tr.tl('Aureum Brain Tree', bioscan_globals.translation_context)
        case 'Puniceum Brain Tree':
            return tr.tl('Puniceum Brain Tree', bioscan_globals.translation_context)
        case 'Lindigoticum Brain Tree':
            return tr.tl('Lindigoticum Brain Tree', bioscan_globals.translation_context)
        case 'Lividum Brain Tree':
            return tr.tl('Lividum Brain Tree', bioscan_globals.translation_context)
        case 'Cactoida Cortexum':
            return tr.tl('Cactoida Cortexum', bioscan_globals.translation_context)
        case 'Cactoida Lapis':
            return tr.tl('Cactoida Lapis', bioscan_globals.translation_context)
        case 'Cactoida Vermis':
            return tr.tl('Cactoida Vermis', bioscan_globals.translation_context)
        case 'Cactoida Pullulanta':
            return tr.tl('Cactoida Pullulanta', bioscan_globals.translation_context)
        case 'Cactoida Peperatis':
            return tr.tl('Cactoida Peperatis', bioscan_globals.translation_context)
        case 'Clypeus Lacrimam':
            return tr.tl('Clypeus Lacrimam', bioscan_globals.translation_context)
        case 'Clypeus Margaritus':
            return tr.tl('Clypeus Margaritus', bioscan_globals.translation_context)
        case 'Clypeus Speculumi':
            return tr.tl('Clypeus Speculumi', bioscan_globals.translation_context)
        case 'Concha Renibus':
            return tr.tl('Concha Renibus', bioscan_globals.translation_context)
        case 'Concha Aureolas':
            return tr.tl('Concha Aureolas', bioscan_globals.translation_context)
        case 'Concha Labiata':
            return tr.tl('Concha Labiata', bioscan_globals.translation_context)
        case 'Concha Biconcavis':
            return tr.tl('Concha Biconcavis', bioscan_globals.translation_context)
        case 'Electricae Pluma':
            return tr.tl('Electricae Pluma', bioscan_globals.translation_context)
        case 'Electricae Radialem':
            return tr.tl('Electricae Radialem', bioscan_globals.translation_context)
        case 'Fonticulua Segmentatus':
            return tr.tl('Fonticulua Segmentatus', bioscan_globals.translation_context)
        case 'Fonticulua Campestris':
            return tr.tl('Fonticulua Campestris', bioscan_globals.translation_context)
        case 'Fonticulua Upupam':
            return tr.tl('Fonticulua Upupam', bioscan_globals.translation_context)
        case 'Fonticulua Lapida':
            return tr.tl('Fonticulua Lapida', bioscan_globals.translation_context)
        case 'Fonticulua Fluctus':
            return tr.tl('Fonticulua Fluctus', bioscan_globals.translation_context)
        case 'Fonticulua Digitos':
            return tr.tl('Fonticulua Digitos', bioscan_globals.translation_context)
        case 'Frutexa Flabellum':
            return tr.tl('Frutexa Flabellum', bioscan_globals.translation_context)
        case 'Frutexa Acus':
            return tr.tl('Frutexa Acus', bioscan_globals.translation_context)
        case 'Frutexa Metallicum':
            return tr.tl('Frutexa Metallicum', bioscan_globals.translation_context)
        case 'Frutexa Flammasis':
            return tr.tl('Frutexa Flammasis', bioscan_globals.translation_context)
        case 'Frutexa Fera':
            return tr.tl('Frutexa Fera', bioscan_globals.translation_context)
        case 'Frutexa Sponsae':
            return tr.tl('Frutexa Sponsae', bioscan_globals.translation_context)
        case 'Frutexa Collum':
            return tr.tl('Frutexa Collum', bioscan_globals.translation_context)
        case 'Fumerola Carbosis':
            return tr.tl('Fumerola Carbosis', bioscan_globals.translation_context)
        case 'Fumerola Extremus':
            return tr.tl('Fumerola Extremus', bioscan_globals.translation_context)
        case 'Fumerola Nitris':
            return tr.tl('Fumerola Nitris', bioscan_globals.translation_context)
        case 'Fumerola Aquatis':
            return tr.tl('Fumerola Aquatis', bioscan_globals.translation_context)
        case 'Fungoida Setisis':
            return tr.tl('Fungoida Setisis', bioscan_globals.translation_context)
        case 'Fungoida Stabitis':
            return tr.tl('Fungoida Stabitis', bioscan_globals.translation_context)
        case 'Fungoida Bullarum':
            return tr.tl('Fungoida Bullarum', bioscan_globals.translation_context)
        case 'Fungoida Gelata':
            return tr.tl('Fungoida Gelata', bioscan_globals.translation_context)
        case 'Osseus Fractus':
            return tr.tl('Osseus Fractus', bioscan_globals.translation_context)
        case 'Osseus Discus':
            return tr.tl('Osseus Discus', bioscan_globals.translation_context)
        case 'Osseus Spiralis':
            return tr.tl('Osseus Spiralis', bioscan_globals.translation_context)
        case 'Osseus Pumice':
            return tr.tl('Osseus Pumice', bioscan_globals.translation_context)
        case 'Osseus Cornibus':
            return tr.tl('Osseus Cornibus', bioscan_globals.translation_context)
        case 'Osseus Pellebantus':
            return tr.tl('Osseus Pellebantus', bioscan_globals.translation_context)
        case 'Recepta Umbrux':
            return tr.tl('Recepta Umbrux', bioscan_globals.translation_context)
        case 'Recepta Deltahedronix':
            return tr.tl('Recepta Deltahedronix', bioscan_globals.translation_context)
        case 'Recepta Conditivus':
            return tr.tl('Recepta Conditivus', bioscan_globals.translation_context)
        case 'Stratum Aranaemus':
            return tr.tl('Stratum Aranaemus', bioscan_globals.translation_context)
        case 'Stratum Excutitus':
            return tr.tl('Stratum Excutitus', bioscan_globals.translation_context)
        case 'Stratum Paleas':
            return tr.tl('Stratum Paleas', bioscan_globals.translation_context)
        case 'Stratum Laminamus':
            return tr.tl('Stratum Laminamus', bioscan_globals.translation_context)
        case 'Stratum Limaxus':
            return tr.tl('Stratum Limaxus', bioscan_globals.translation_context)
        case 'Stratum Cucumisis':
            return tr.tl('Stratum Cucumisis', bioscan_globals.translation_context)
        case 'Stratum Tectonicas':
            return tr.tl('Stratum Tectonicas', bioscan_globals.translation_context)
        case 'Stratum Frigus':
            return tr.tl('Stratum Frigus', bioscan_globals.translation_context)
        case 'Roseum Sinuous Tubers':
            return tr.tl('Roseum Sinuous Tubers', bioscan_globals.translation_context)
        case 'Prasinum Sinuous Tubers':
            return tr.tl('Prasinum Sinuous Tubers', bioscan_globals.translation_context)
        case 'Albidum Sinuous Tubers':
            return tr.tl('Albidum Sinuous Tubers', bioscan_globals.translation_context)
        case 'Caeruleum Sinuous Tubers':
            return tr.tl('Caeruleum Sinuous Tubers', bioscan_globals.translation_context)
        case 'Lindigoticum Sinuous Tubers':
            return tr.tl('Lindigoticum Sinuous Tubers', bioscan_globals.translation_context)
        case 'Violaceum Sinuous Tubers':
            return tr.tl('Violaceum Sinuous Tubers', bioscan_globals.translation_context)
        case 'Viride Sinuous Tubers':
            return tr.tl('Viride Sinuous Tubers', bioscan_globals.translation_context)
        case 'Blatteum Sinuous Tubers':
            return tr.tl('Blatteum Sinuous Tubers', bioscan_globals.translation_context)
        case 'Tubus Conifer':
            return tr.tl('Tubus Conifer', bioscan_globals.translation_context)
        case 'Tubus Sororibus':
            return tr.tl('Tubus Sororibus', bioscan_globals.translation_context)
        case 'Tubus Cavas':
            return tr.tl('Tubus Cavas', bioscan_globals.translation_context)
        case 'Tubus Rosarium':
            return tr.tl('Tubus Rosarium', bioscan_globals.translation_context)
        case 'Tubus Compagibus':
            return tr.tl('Tubus Compagibus', bioscan_globals.translation_context)
        case 'Tussock Pennata':
            return tr.tl('Tussock Pennata', bioscan_globals.translation_context)
        case 'Tussock Ventusa':
            return tr.tl('Tussock Ventusa', bioscan_globals.translation_context)
        case 'Tussock Ignis':
            return tr.tl('Tussock Ignis', bioscan_globals.translation_context)
        case 'Tussock Cultro':
            return tr.tl('Tussock Cultro', bioscan_globals.translation_context)
        case 'Tussock Catena':
            return tr.tl('Tussock Catena', bioscan_globals.translation_context)
        case 'Tussock Pennatis':
            return tr.tl('Tussock Pennatis', bioscan_globals.translation_context)
        case 'Tussock Serrati':
            return tr.tl('Tussock Serrati', bioscan_globals.translation_context)
        case 'Tussock Albata':
            return tr.tl('Tussock Albata', bioscan_globals.translation_context)
        case 'Tussock Propagito':
            return tr.tl('Tussock Propagito', bioscan_globals.translation_context)
        case 'Tussock Divisa':
            return tr.tl('Tussock Divisa', bioscan_globals.translation_context)
        case 'Tussock Caputus':
            return tr.tl('Tussock Caputus', bioscan_globals.translation_context)
        case 'Tussock Triticum':
            return tr.tl('Tussock Triticum', bioscan_globals.translation_context)
        case 'Tussock Stigmasis':
            return tr.tl('Tussock Stigmasis', bioscan_globals.translation_context)
        case 'Tussock Virgam':
            return tr.tl('Tussock Virgam', bioscan_globals.translation_context)
        case 'Tussock Capillum':
            return tr.tl('Tussock Capillum', bioscan_globals.translation_context)
        case 'Crystalline Shards':
            return tr.tl('Crystalline Shards', bioscan_globals.translation_context)
        case 'Bark Mound':
            return tr.tl('Bark Mound', bioscan_globals.translation_context)
        case 'Amphora Plant':
            return tr.tl('Amphora Plant', bioscan_globals.translation_context)
        case _:
            return species
