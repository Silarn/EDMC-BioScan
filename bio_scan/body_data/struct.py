from typing import Self


class PlanetData:
    def __init__(self, name):
        self.name: str = name
        self.type: str = ''
        self.id: int = -1
        self.atmosphere: str = ''
        self.volcanism: str = ''
        self.distance: float = 0.0
        self.gravity: float = 0.0
        self.temp: float = 0.0
        self.parent_star: int = -1
        self.bio_signals: int = 0
        self.flora: dict[str, tuple[str, int, str]] = {}
        self.materials: set[str] = set()
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

    def get_parent_star(self) -> int:
        return self.parent_star

    def set_parent_star(self, value: int) -> Self:
        self.parent_star = value
        return self

    def get_flora(self, genus: str = None) -> dict[str, tuple[str, int, str]] | tuple[str, int, str] | None:
        if genus:
            if genus in self.flora:
                return self.flora[genus]
            else:
                return None
        return self.flora

    def add_flora(self, genus: str, species: str = '', color: str = '') -> Self:
        scan = 0
        if genus in self.flora:
            scan = self.flora[genus][1]
        self.flora[genus] = (species, scan, color)
        return self

    def set_flora_species_scan(self, genus: str, species: str, scan: int) -> Self:
        if genus in self.flora:
            self.flora[genus] = (species, scan, self.flora[genus][2])
        else:
            self.flora[genus] = (species, scan, '')
        return self

    def set_flora_color(self, genus: str, color: str) -> Self:
        if genus in self.flora:
            self.flora[genus] = (self.flora[genus][0], self.flora[genus][1], color)
        else:
            self.flora[genus] = ('', 0, color)
        return self

    def get_materials(self) -> set[str]:
        return self.materials

    def add_material(self, material: str) -> Self:
        self.materials.add(material)
        return self

    def clear_flora(self) -> Self:
        self.flora = {}
        return self

    def is_mapped(self) -> bool:
        return self.mapped

    def set_mapped(self, value: bool) -> Self:
        self.mapped = value
        return self


class StarData:
    def __init__(self, name, star_id):
        self.name: str = name
        self.type: str = ''
        self.id: int = star_id
        self.luminosity: str = ''

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> int:
        return self.id

    def get_type(self) -> str:
        return self.type

    def set_type(self, value: str) -> Self:
        self.type = value
        return self

    def get_luminosity(self):
        return self.luminosity

    def set_luminosity(self, value: str) -> Self:
        self.luminosity = value
        return self
