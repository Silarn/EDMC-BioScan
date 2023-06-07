from typing import Self, Optional

from sqlalchemy.orm import Session, scoped_session
from sqlalchemy import select, delete
from bio_scan.body_data.db import Planet, System, PlanetFlora, PlanetGas, Waypoint, FloraScans, Star


class PlanetData:
    """ Holds all attributes, getters, and setters for planet data. """

    def __init__(self, system: System, data: Planet, session: Session):
        self._session: Session = session
        self._system: System = system
        self._data: Planet = data

    @classmethod
    def from_journal(cls, system: System, name: str, body_id: int, session: Session):
        data: Planet = session.scalar(select(Planet).where(Planet.name == name).where(Planet.system_id == system.id))
        if not data:
            data = Planet(name=name, body_id=body_id, system_id=system.id)
            session.add(data)
        session.commit()

        return cls(system, data, session)

    def get_name(self) -> str:
        return self._data.name

    def get_type(self) -> str:
        return self._data.type

    def set_type(self, value: str) -> Self:
        self._data.type = value
        self.commit()
        return self

    def get_id(self) -> int:
        return self._data.body_id

    def set_id(self, value: int) -> Self:
        self._data.body_id = value
        self.commit()
        return self

    def get_atmosphere(self) -> str:
        return self._data.atmosphere

    def set_atmosphere(self, value: str) -> Self:
        self._data.atmosphere = value
        self.commit()
        return self

    def add_gas(self, gas: str, percent: float) -> Self:
        for gas_data in self._data.gasses:  # type: PlanetGas
            if gas_data.gas_name == gas:
                gas_data.percent = percent
                self.commit()
                return self
        self._data.gasses.append(PlanetGas(gas_name=gas, percent=percent))
        self.commit()
        return self

    def get_gas(self, gas: str) -> float:
        for gas_data in self._data.gasses:  # type: PlanetGas
            if gas_data.gas_name == gas:
                return gas_data.percent
        return 0.0

    def get_volcanism(self) -> str:
        return self._data.volcanism

    def set_volcanism(self, value: Optional[int]) -> Self:
        self._data.volcanism = value
        self.commit()
        return self

    def get_distance(self) -> float:
        return self._data.distance

    def set_distance(self, value: float) -> Self:
        self._data.distance = value
        self.commit()
        return self

    def get_gravity(self) -> float:
        return self._data.gravity

    def set_gravity(self, value: float) -> Self:
        self._data.gravity = value
        self.commit()
        return self

    def get_temp(self) -> Optional[float]:
        return self._data.temp

    def set_temp(self, value: Optional[float]) -> Self:
        self._data.temp = value
        self.commit()
        return self

    def get_bio_signals(self) -> int:
        return self._data.bio_signals

    def set_bio_signals(self, value: int) -> Self:
        self._data.bio_signals = value
        self.commit()
        return self

    def get_parent_stars(self) -> list[str]:
        if self._data.parent_stars:
            return self._data.parent_stars.split(',')
        return []

    def add_parent_star(self, value: str) -> Self:
        if self._data.parent_stars:
            stars: list[str] = []
            stars += self._data.parent_stars.split(',')
            stars.append(value)
            stars = [*set(stars)]
            self._data.parent_stars = ','.join(stars)
        else:
            self._data.parent_stars = value
        self.commit()
        return self

    def get_flora(self, genus: str = None, create: bool = False) -> list[PlanetFlora] | PlanetFlora | None:
        if genus:
            for flora in self._data.floras:  # type: PlanetFlora
                if flora.genus == genus:
                    return flora
            else:
                if create:
                    new_flora = PlanetFlora(genus=genus)
                    self._data.floras.append(new_flora)
                    self.commit()
                    return new_flora
                return None
        return self._data.floras

    def add_flora(self, genus: str, species: str = '', color: str = '') -> Self:
        flora = self.get_flora(genus, create=True)
        flora.species = species
        flora.color = color
        self.commit()
        return self

    def set_flora_species_scan(self, genus: str, species: str, scan: int, commander: int) -> Self:
        flora = self.get_flora(genus, create=True)
        flora.species = species
        stmt = select(FloraScans).where(FloraScans.flora_id == flora.id).where(FloraScans.commander_id == commander)
        scan_data: Optional[FloraScans] = self._session.scalar(stmt)
        if not scan_data:
            scan_data = FloraScans(flora_id=flora.id, commander_id=commander)
            self._session.add(scan_data)
            self.commit()
        scan_data.count = scan
        if scan == 3:
            stmt = delete(Waypoint).where(Waypoint.commander_id == commander).where(Waypoint.flora_id == flora.id)
            self._session.execute(stmt)
        self.commit()
        return self

    def set_flora_color(self, genus: str, color: str) -> Self:
        flora = self.get_flora(genus, create=True)
        flora.color = color
        self.commit()
        return self

    def add_flora_waypoint(self, genus: str, lat_long: tuple[float, float], commander: int, scan: bool = False) -> Self:
        flora = self.get_flora(genus)
        if flora:
            scans: FloraScans = self._session.scalar(
                select(FloraScans).where(FloraScans.flora_id == flora.id).where(FloraScans.commander_id == commander)
            )
            if not scans or scans.count != 3:
                waypoint = Waypoint()
                waypoint.flora_id = flora.id
                waypoint.commander_id = commander
                waypoint.latitude = lat_long[0]
                waypoint.longitude = lat_long[1]
                if scan:
                    waypoint.type = 'scan'
                self._session.add(waypoint)
                self.commit()
        return self

    def has_waypoint(self, commander: id) -> bool:
        for flora in self._data.floras:  # type: PlanetFlora
            stmt = select(Waypoint) \
                .where(Waypoint.flora_id == flora.id) \
                .where(Waypoint.commander_id == commander) \
                .where(Waypoint.type == 'tag')
            if self._session.scalars(stmt):
                return True
        return False

    def get_materials(self) -> set[str]:
        if self._data.materials:
            return set(self._data.materials.split(','))
        return set()

    def add_material(self, material: str) -> Self:
        materials = self.get_materials()
        materials.add(material)
        self._data.materials = ','.join(materials)
        self.commit()
        return self

    def clear_flora(self) -> Self:
        self._session.execute(delete(PlanetFlora).where(PlanetFlora.planet_id == self._data.id))
        self.commit()
        return self

    def is_mapped(self) -> bool:
        return self._data.mapped

    def set_mapped(self, value: bool) -> Self:
        self._data.mapped = value
        return self

    def commit(self) -> None:
        self._session.commit()

    def __del__(self) -> None:
        self.commit()


class StarData:
    """ Holds all attributes, getters, and setters for star data. """

    def __init__(self, system: System, data: Star, session: Session):
        self._session = session
        self._system = system
        self._data = data

    @classmethod
    def from_journal(cls, system: System, name: str, body_id: int, session: Session):
        data: Star = session.scalar(
            select(Star).where(Star.name == name).where(Star.system_id == system.id)
        )
        if not data:
            data = Star()
            data.name = name
            data.system_id = system.id
            data.body_id = body_id
            session.add(data)
        session.commit()

        return cls(system, data, session)

    def get_name(self) -> str:
        return self._data.name

    def get_id(self) -> int:
        return self._data.body_id

    def get_distance(self) -> Optional[float]:
        return self._data.distance

    def set_distance(self, value: float) -> Self:
        self._data.distance = value
        self.commit()
        return self

    def get_type(self) -> str:
        return self._data.type

    def set_type(self, value: str) -> Self:
        self._data.type = value
        self.commit()
        return self

    def get_luminosity(self):
        return self._data.luminosity

    def set_luminosity(self, value: str) -> Self:
        self._data.luminosity = value
        self.commit()
        return self

    def commit(self) -> None:
        self._session.commit()

    def __del__(self) -> None:
        self.commit()


def load_planets(system: System, session: Session) -> dict[str, PlanetData]:
    planet_data: dict[str, PlanetData] = {}
    if system and system.id:
        planets = session.scalars(select(Planet).where(Planet.system_id == system.id))
        for planet in planets:  # type: Planet
            planet_data[planet.name] = PlanetData(system, planet, session)
    session.commit()
    return planet_data


def load_stars(system: System, session: Session) -> dict[str, StarData]:
    star_data: dict[str, StarData] = {}
    if system and system.id:
        stars = session.scalars(select(Star).where(Star.system_id == system.id))
        for star in stars:  # type: Star
            star_data[star.name] = StarData(system, star, session)
    session.commit()
    return star_data


def get_main_star(system: System, session: Session) -> Optional[Star]:
    if system and system.id:
        return session.scalar(select(Star).where(Star.system_id == system.id).where(Star.distance == 0.0))
    return None
