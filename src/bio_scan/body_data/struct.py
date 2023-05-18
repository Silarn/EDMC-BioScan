from typing import Self


class PlanetData:
    """ Holds all attributes, getters, and setters for planet data. """

    def __init__(self, name):
        self._name: str = name
        self._type: str = ''
        self._id: int = -1
        self._atmosphere: str = ''
        self._gasses: dict[str, float] = {}
        self._volcanism: str = ''
        self._distance: float = 0.0
        self._gravity: float = 0.0
        self._temp: float = 0.0
        self._parent_stars: list[str] = []
        self._bio_signals: int = 0
        self._flora: dict[str, dict[str, any]] = {}
        self._materials: set[str] = set()
        self._mapped: bool = False

    def get_name(self) -> str:
        return self._name

    def get_type(self) -> str:
        return self._type

    def set_type(self, value: str) -> Self:
        self._type = value
        return self

    def get_id(self) -> int:
        return self._id

    def set_id(self, value: int) -> Self:
        self._id = value
        return self

    def get_atmosphere(self) -> str:
        return self._atmosphere

    def set_atmosphere(self, value: str) -> Self:
        self._atmosphere = value
        return self

    def add_gas(self, gas: str, percent: float) -> Self:
        self._gasses[gas] = percent
        return self

    def get_gas(self, gas: str) -> float:
        if gas in self._gasses:
            return self._gasses[gas]
        return 0.0

    def get_volcanism(self) -> str:
        return self._volcanism

    def set_volcanism(self, value: int) -> Self:
        self._volcanism = value
        return self

    def get_distance(self) -> float:
        return self._distance

    def set_distance(self, value: float) -> Self:
        self._distance = value
        return self

    def get_gravity(self) -> float:
        return self._gravity

    def set_gravity(self, value: float) -> Self:
        self._gravity = value
        return self

    def get_temp(self) -> float:
        return self._temp

    def set_temp(self, value: float) -> Self:
        self._temp = value
        return self

    def get_bio_signals(self) -> int:
        return self._bio_signals

    def set_bio_signals(self, value: int) -> Self:
        self._bio_signals = value
        return self

    def get_parent_stars(self) -> list[str]:
        return self._parent_stars

    def add_parent_star(self, value: str) -> Self:
        self._parent_stars.append(value)
        return self

    def get_flora(self, genus: str = None) -> dict[str, dict[str, any]] | dict[str, any] | None:
        if genus:
            if genus in self._flora:
                return self._flora[genus]
            else:
                return None
        return self._flora

    def add_flora(self, genus: str, species: str = '', color: str = '') -> Self:
        data = self._flora.get(genus, {})
        data['species'] = species
        data['color'] = color
        self._flora[genus] = data
        return self

    def set_flora_species_scan(self, genus: str, species: str, scan: int) -> Self:
        data = self._flora.get(genus, {})
        data['species'] = species
        data['scan'] = scan
        if scan == 3:
            data.pop('waypoints', None)
        self._flora[genus] = data
        return self

    def set_flora_color(self, genus: str, color: str) -> Self:
        data = self._flora.get(genus, {})
        data['color'] = color
        self._flora[genus] = data
        return self

    def add_flora_waypoint(self, genus: str, lat_long: tuple[float, float]) -> Self:
        data = self._flora.get(genus, {})
        if data.get('scan', 0) != 3:
            waypoints: list[tuple[float, float]] = data.get('waypoints', [])
            waypoints.append(lat_long)
            data['waypoints'] = waypoints
            self._flora[genus] = data
        return self

    def has_waypoint(self) -> bool:
        for _, data in self._flora.items():
            if 'waypoints' in data:
                return True
        return False

    def get_materials(self) -> set[str]:
        return self._materials

    def add_material(self, material: str) -> Self:
        self._materials.add(material)
        return self

    def clear_flora(self) -> Self:
        self._flora = {}
        return self

    def is_mapped(self) -> bool:
        return self._mapped

    def set_mapped(self, value: bool) -> Self:
        self._mapped = value
        return self


class StarData:
    """ Holds all attributes, getters, and setters for star data. """

    def __init__(self, name, star_id):
        self._name: str = name
        self._type: str = ''
        self._id: int = star_id
        self._luminosity: str = ''

    def get_name(self) -> str:
        return self._name

    def get_id(self) -> int:
        return self._id

    def get_type(self) -> str:
        return self._type

    def set_type(self, value: str) -> Self:
        self._type = value
        return self

    def get_luminosity(self):
        return self._luminosity

    def set_luminosity(self, value: str) -> Self:
        self._luminosity = value
        return self
