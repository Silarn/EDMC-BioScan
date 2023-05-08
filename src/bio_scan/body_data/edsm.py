def map_edsm_type(edsm_class: str) -> str:
    match edsm_class:
        case 'Earth-like world':
            return 'Earthlike body'
        case 'Metal-rich body':
            return 'Metal rich body'
        case 'High metal content world':
            return 'High metal content body'
        case 'Rocky Ice world':
            return 'Rocky ice body'
        case 'Class I gas giant':
            return 'Sudarsky class I gas giant'
        case 'Class II gas giant':
            return 'Sudarsky class II gas giant'
        case 'Class III gas giant':
            return 'Sudarsky class III gas giant'
        case 'Class IV gas giant':
            return 'Sudarsky class IV gas giant'
        case 'Class V gas giant':
            return 'Sudarsky class V gas giant'
        case 'Gas giant with ammonia-based life':
            return 'Gas giant with ammonia based life'
        case 'Gas giant with water-based life':
            return 'Gas giant with water based life'
        case 'Helium-rich gas giant':
            return 'Helium rich gas giant'
        case _:
            return edsm_class


def parse_edsm_star_class(subtype: str) -> str:
    star_class = ''
    match subtype:
        case 'White Dwarf (D) Star':
            star_class = 'D'
        case 'White Dwarf (DA) Star':
            star_class = 'DA'
        case 'White Dwarf (DAB) Star':
            star_class = 'DAB'
        case 'White Dwarf (DAO) Star':
            star_class = 'DAO'
        case 'White Dwarf (DAZ) Star':
            star_class = 'DAZ'
        case 'White Dwarf (DB) Star':
            star_class = 'DB'
        case 'White Dwarf (DBZ) Star':
            star_class = 'DBZ'
        case 'White Dwarf (DBV) Star':
            star_class = 'DBV'
        case 'White Dwarf (DO) Star':
            star_class = 'DO'
        case 'White Dwarf (DOV) Star':
            star_class = 'DOV'
        case 'White Dwarf (DQ) Star':
            star_class = 'DQ'
        case 'White Dwarf (DC) Star':
            star_class = 'DC'
        case 'White Dwarf (DCV) Star':
            star_class = 'DCV'
        case 'White Dwarf (DX) Star':
            star_class = 'DX'
        case 'CS Star':
            star_class = 'CS'
        case 'C Star':
            star_class = 'C'
        case 'CN Star':
            star_class = 'CN'
        case 'CJ Star':
            star_class = 'CJ'
        case 'CH Star':
            star_class = 'CH'
        case 'CHd Star':
            star_class = 'CHd'
        case 'MS-type Star':
            star_class = 'MS'
        case 'S-type Star':
            star_class = 'S'
        case 'Herbig Ae/Be Star':
            star_class = 'AeBe'
        case 'Wolf-Rayet Star':
            star_class = 'W'
        case 'Wolf-Rayet N Star':
            star_class = 'WN'
        case 'Wolf-Rayet NC Star':
            star_class = 'WNC'
        case 'Wolf-Rayet C Star':
            star_class = 'WC'
        case 'Wolf-Rayet O Star':
            star_class = 'WO'
        case 'Neutron Star':
            star_class = 'N'
        case 'Black Hole':
            star_class = 'H'
        case 'Supermassive Black Hole':
            star_class = 'SupermassiveBlackHole'

    return star_class


def map_edsm_atmosphere(atmosphere: str) -> str:
    if atmosphere.endswith('Ammonia'):
        return 'Ammonia'
    if atmosphere.endswith('Water'):
        return 'Water'
    if atmosphere.endswith('Carbon dioxide'):
        return 'CarbonDioxide'
    if atmosphere.endswith('Sulphur dioxide'):
        return 'SulphurDioxide'
    if atmosphere.endswith('Nitrogen'):
        return 'Nitrogen'
    if atmosphere.endswith('Water-rich'):
        return 'WaterRich'
    if atmosphere.endswith('Methane-rich'):
        return 'MethaneRich'
    if atmosphere.endswith('Ammonia-rich'):
        return 'AmmoniaRich'
    if atmosphere.endswith('Carbon dioxide-rich'):
        return 'CarbonDioxideRich'
    if atmosphere.endswith('Methane'):
        return 'Methane'
    if atmosphere.endswith('Helium'):
        return 'Helium'
    if atmosphere.endswith('Silicate vapour'):
        return 'SilicateVapour'
    if atmosphere.endswith('Metallic vapour'):
        return 'MetallicVapour'
    if atmosphere.endswith('Neon-rich'):
        return 'NeonRich'
    if atmosphere.endswith('Argon-rich'):
        return 'ArgonRich'
    if atmosphere.endswith('Neon'):
        return 'Neon'
    if atmosphere.endswith('Argon'):
        return 'Argon'
    if atmosphere.endswith('Oxygen'):
        return 'Oxygen'
    if atmosphere == 'No atmosphere':
        return 'None'
    return atmosphere
