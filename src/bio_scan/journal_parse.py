import json
import re
from pathlib import Path
from typing import Any, BinaryIO, MutableMapping, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, scoped_session

from EDMCLogging import get_plugin_logger
from bio_scan.RegionMap import findRegion
from bio_scan.bio_data.codex import parse_variant, set_codex
from bio_scan.body_data.db import System, Commander, Planet
from bio_scan.body_data.struct import PlanetData, StarData

logger = get_plugin_logger('BioScan')


class JournalParse:
    def __init__(self, journal: Path, session_factory: scoped_session):
        self._journal: Path = journal
        self._session: Session = session_factory()
        self._session_factory: scoped_session = session_factory
        self._cmdr: Optional[Commander] = None
        self._system: Optional[System] = None

    def parse_journal(self) -> bool:
        logger.debug(f'Parsing: {self._journal}')
        log: BinaryIO = open(self._journal, 'rb', 0)
        for line in log:
            result = self.parse_entry(line)
            if not result:
                return False
        return True

    def parse_entry(self, line: bytes) -> bool:
        if line is None:
            return False

        try:
            entry: MutableMapping[str, Any] = json.loads(line)
            self.process_entry(entry)
        except Exception as ex:
            logger.debug(f'Invalid journal entry:\n{line!r}\n', exc_info=ex)
            return False
        return True

    def process_entry(self, entry: MutableMapping[str, Any]):
        event_type = entry['event'].lower()
        match event_type:
            case 'loadgame':
                self._session = self._session_factory()
                self.set_cmdr(entry['Commander'])
            case 'commander' | 'newcommander':
                self._session = self._session_factory()
                self.set_cmdr(entry['Name'])
            case 'location' | 'fsdjump' | 'carrierjump':
                self.set_system(entry['StarSystem'], entry.get('StarPos', None))
            case 'scan':
                body_short_name = self.get_body_name(entry['BodyName'])
                if 'StarType' in entry:
                    if body_short_name == entry['BodyName']:
                        self.add_star(entry)
                    else:
                        if re.search('^[A-Z]$', body_short_name):
                            self.add_star(entry)
                elif 'PlanetClass' in entry:
                    self.add_planet(entry)
            case 'fssbodysignals' | 'saasignalsfound':
                self.add_signals(entry)
            case 'scanorganic':
                self.add_scan(entry)
            case 'codexentry':
                if entry['Category'] == '$Codex_Category_Biology;' and 'BodyID' in entry:
                    planet = self._session.scalar(select(Planet).where(Planet.system_id == self._system.id)
                                                  .where(Planet.body_id == entry['BodyID']))
                    if not planet:
                        return

                    target_body = PlanetData(self._system, planet, self._session)

                    genus, species, color = parse_variant(entry['Name'])
                    if genus is not '' and species is not '':
                        target_body.add_flora(genus, species, color)

                    set_codex(self._session_factory, self._cmdr.id, entry['Name'], self._system.region)

    def get_body_name(self, fullname: str) -> str:
        """
        Remove the base system name from the body name if the body has a unique identifier.
        Usually only the main star has the same name as the system in one-star systems.

        :param fullname: The full name of the body including the system name
        :return: The short name of the body unless it matches the system name
        """
        if fullname.startswith(self._system.name + ' '):
            body_name = fullname[len(self._system.name + ' '):]
        else:
            body_name = fullname
        return body_name

    def set_cmdr(self, name: str) -> None:
        self._cmdr = self._session.scalar(select(Commander).where(Commander.name == name))
        if not self._cmdr:
            self._cmdr = Commander(name=name)
            self._session.add(self._cmdr)
            self._session.commit()

    def set_system(self, name: str, address: list[float]) -> None:
        self._system = self._session.scalar(select(System).where(System.name == name))
        if not self._system:
            self._system = System(name=name)
            self._session.add(self._system)
            self._session.commit()
        if address:
            self._system.x = address[0]
            self._system.y = address[1]
            self._system.z = address[2]
            region = findRegion(self._system.x, self._system.y, self._system.z)
            if region:
                self._system.region = region[0]
            self._session.commit()

    def add_star(self, entry: MutableMapping[str, Any]) -> None:
        """
        Add main star data from journal event

        :param entry: The journal event dict (must be a Scan event with star data)
        """

        body_short_name = self.get_body_name(entry['BodyName'])
        star_data = StarData.from_journal(self._system, body_short_name, entry['BodyID'], self._session)

        star_data.set_distance(entry['DistanceFromArrivalLS']) \
            .set_type(entry['StarType']) \
            .set_luminosity(entry['Luminosity'])

    def add_planet(self, entry: MutableMapping[str, Any]) -> None:
        body_short_name = self.get_body_name(entry['BodyName'])
        body_data = PlanetData.from_journal(self._system, body_short_name, entry['BodyID'], self._session)
        body_data.set_distance(float(entry['DistanceFromArrivalLS'])).set_type(entry['PlanetClass']) \
            .set_gravity(entry['SurfaceGravity']).set_temp(entry.get('SurfaceTemperature', None)) \
            .set_volcanism(entry.get('Volcanism', None))

        star_search = re.search('^([A-Z]+) .+$', body_short_name)
        if star_search:
            for star in star_search.group(1):
                body_data.add_parent_star(star)
        else:
            body_data.add_parent_star(self._system.name)

        if 'Materials' in entry:
            for material in entry['Materials']:
                body_data.add_material(material['Name'])

        if 'AtmosphereType' in entry:
            body_data.set_atmosphere(entry['AtmosphereType'])

        if 'AtmosphereComposition' in entry:
            for gas in entry['AtmosphereComposition']:
                body_data.add_gas(gas['Name'], gas['Percent'])

    def add_signals(self, entry: MutableMapping[str, Any]) -> None:
        body_short_name = self.get_body_name(entry['BodyName'])

        body_data = PlanetData.from_journal(self._system, body_short_name, entry['BodyID'], self._session)

        # Add bio signal number just in case
        for signal in entry['Signals']:
            if signal['Type'] == '$SAA_SignalType_Biological;':
                body_data.set_bio_signals(signal['Count'])

        # If signals include genuses, add them to the body data
        if 'Genuses' in entry:
            for genus in entry['Genuses']:
                if body_data.get_flora(genus['Genus']) is None:
                    body_data.add_flora(genus['Genus'])

    def add_scan(self, entry: MutableMapping[str, Any]) -> None:
        planet = self._session.scalar(select(Planet).where(Planet.system_id == self._system.id)
                                      .where(Planet.body_id == entry['Body']))
        if not planet:
            return

        target_body = PlanetData(self._system, planet, self._session)

        scan_level = 0
        match entry['ScanType']:
            case 'Log':
                scan_level = 1
            case 'Sample':
                scan_level = 2
            case 'Analyse':
                scan_level = 3

        if scan_level == 3:
            target_body.set_flora_species_scan(
                entry['Genus'], entry['Species'], scan_level, self._cmdr.id
            )

        if 'Variant' in entry:
            _, _, color = parse_variant(entry['Variant'])
            target_body.set_flora_color(entry['Genus'], color)


def parse_journal(journal: Path, session_factory: scoped_session) -> bool:
    return JournalParse(journal, session_factory).parse_journal()
