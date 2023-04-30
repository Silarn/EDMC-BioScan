from typing import Self


class BodyData:
    def __init__(self, name):
        self.name: str = name
        self.type: str = ""
        self.id: int = -1
        self.atmosphere: str = ""
        self.volcanism: str = ""
        self.distance: float = 0.0
        self.gravity: float = 0.0
        self.temp: float = 0.0
        self.bio_signals: int = 0
        self.flora: dict[str, tuple[str, int]] = {}
        self.mapped: bool = False

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> str:
        return self.type

    def set_type(self, value: str) -> Self:
        self.type = value
        return self

    def get_id(self) -> int:
        return self.id

    def set_id(self, value: int) -> Self:
        self.id = value
        return self

    def get_atmosphere(self) -> str:
        return self.atmosphere

    def set_atmosphere(self, value: str) -> Self:
        self.atmosphere = value
        return self

    def get_volcanism(self) -> str:
        return self.volcanism

    def set_volcanism(self, value: int) -> Self:
        self.volcanism = value
        return self

    def get_distance(self) -> float:
        return self.distance

    def set_distance(self, value: float) -> Self:
        self.distance = value
        return self

    def get_gravity(self) -> float:
        return self.gravity

    def set_gravity(self, value: float) -> Self:
        self.gravity = value
        return self

    def get_temp(self) -> float:
        return self.temp

    def set_temp(self, value: float) -> Self:
        self.temp = value
        return self

    def get_bio_signals(self) -> int:
        return self.bio_signals

    def set_bio_signals(self, value: int) -> Self:
        self.bio_signals = value
        return self

    def get_flora(self, genus: str = None) -> dict[str, tuple[str, int]] | tuple[str, int] | None:
        if genus:
            if genus in self.flora:
                return self.flora[genus]
            else:
                return None
        return self.flora

    def add_flora(self, genus: str, species: str = "") -> Self:
        scan = 0
        if genus in self.flora:
            scan = self.flora[genus][1]
        self.flora[genus] = (species, scan)
        return self

    def set_flora(self, genus: str, species: str, scan: int) -> Self:
        self.flora[genus] = (species, scan)
        return self

    def clear_flora(self) -> Self:
        self.flora = {}
        return self

    def is_mapped(self) -> bool:
        return self.mapped

    def set_mapped(self, value: bool) -> Self:
        self.mapped = value
        return self


def get_body_shorthand(body_type: str) -> str:
    match body_type:
        case 'Icy body':
            return " (I)"
        case 'Rocky body':
            return " (R)"
        case 'Rocky ice body':
            return " (RI)"
        case 'Metal rich body':
            return " (M)"
        case 'High metal content body':
            return " (HMC)"
        case _:
            return ''


def body_check(bodies: dict[str, BodyData], extra: bool = False) -> bool:
    required_types = [
        "Earthlike body",
        "Gas giant with water based life",
        "Gas giant with ammonia based life"
    ]
    if extra:
        required_types += [
            "Ammonia world",
            "Water world",
            "Water giant",
            "Water giant with life",
        ]
    for _, body_data in bodies.items():
        if body_data.get_type() in required_types:
            return True
    return False


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


def parse_edsm_star_class(subtype: str) -> tuple[str, str]:
    star_class = ""
    subclass = "0"
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
        case 'Neutron Star':
            star_class = 'N'
        case 'Black Hole':
            star_class = 'H'
        case 'Supermassive Black Hole':
            star_class = 'SupermassiveBlackHole'

    return star_class, subclass


def map_edsm_atmosphere(atmosphere: str) -> str:
    if atmosphere.endswith("Ammonia"):
        return "Ammonia"
    if atmosphere.endswith("Water"):
        return "Water"
    if atmosphere.endswith("Carbon dioxide"):
        return "CarbonDioxide"
    if atmosphere.endswith("Sulphur dioxide"):
        return "SulphurDioxide"
    if atmosphere.endswith("Nitrogen"):
        return "Nitrogen"
    if atmosphere.endswith("Water-rich"):
        return "WaterRich"
    if atmosphere.endswith("Methane-rich"):
        return "MethaneRich"
    if atmosphere.endswith("Ammonia-rich"):
        return "AmmoniaRich"
    if atmosphere.endswith("Carbon dioxide-rich"):
        return "CarbonDioxideRich"
    if atmosphere.endswith("Methane"):
        return "Methane"
    if atmosphere.endswith("Helium"):
        return "Helium"
    if atmosphere.endswith("Silicate vapour"):
        return "SilicateVapour"
    if atmosphere.endswith("Metallic vapour"):
        return "MetallicVapour"
    if atmosphere.endswith("Neon-rich"):
        return "NeonRich"
    if atmosphere.endswith("Argon-rich"):
        return "ArgonRich"
    if atmosphere.endswith("Neon"):
        return "Neon"
    if atmosphere.endswith("Argon"):
        return "Argon"
    if atmosphere.endswith("Oxygen"):
        return "Oxygen"
    if atmosphere == "No atmosphere":
        return "None"
    return atmosphere
