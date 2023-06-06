import json
import re
from pathlib import Path
from typing import Any, BinaryIO, MutableMapping, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from EDMCLogging import get_plugin_logger
from bio_scan.RegionMap import findRegion
from bio_scan.bio_data.codex import parse_variant, set_codex
from bio_scan.body_data.db import System, Planet, Star, Commander, PlanetFlora
from bio_scan.body_data.struct import PlanetData, StarData

logger = get_plugin_logger('BioScan')


class JournalData:
    cmdr: Optional[Commander]
    system: Optional[System]
    planets: Optional[dict[str, PlanetData]]
    stars: Optional[dict[str, StarData]]


class This:
    active_journal: JournalData = JournalData()


this = This()


def parse_journal(journal: Path, session: Session) -> bool:
    this.active_journal = JournalData()
    logger.debug(f'Parsing: {journal}')
    log: BinaryIO = open(journal, 'rb', 0)
    for line in log:
        result = parse_entry(line, session)
        if not result:
            return False
    return True


def parse_entry(line: bytes, session: Session) -> bool:
    if line is None:
        return False

    try:
        entry: MutableMapping[str, Any] = json.loads(line)
        process_entry(entry, session)
    except Exception as ex:
        logger.debug(f'Invalid journal entry:\n{line!r}\n', exc_info=ex)
        return False
    return True


def process_entry(entry: MutableMapping[str, Any], session: Session):
    event_type = entry['event'].lower()
    match event_type:
        case 'loadgame':
            session.close()
            this.active_journal = JournalData()
            set_cmdr(entry['Commander'], session)
        case 'commander' | 'newcommander':
            session.close()
            this.active_journal = JournalData()
            set_cmdr(entry['Name'], session)
        case 'location' | 'fsdjump' | 'carrierjump':
            session.commit()
            this.active_journal.stars = {}
            this.active_journal.planets = {}
            set_system(entry['StarSystem'], entry.get('StarPos', None), session)
        case 'scan':
            body_short_name = get_body_name(entry['BodyName'])
            if 'StarType' in entry:
                if body_short_name == entry['BodyName']:
                    add_star(entry, session)
                else:
                    if re.search('^[A-Z]$', body_short_name):
                        add_star(entry, session)
            elif 'PlanetClass' in entry:
                add_planet(entry, session)
        case 'fssbodysignals' | 'saasignalsfound':
            add_signals(entry, session)
        case 'scanorganic':
            add_scan(entry, session)
        case 'codexentry':
            if entry['Category'] == '$Codex_Category_Biology;' and 'BodyID' in entry:
                target_body = None
                for name, body in this.active_journal.planets.items():
                    if body.get_id() == entry['BodyID']:
                        target_body = name
                        break

                if target_body is not None:
                    genus, species, color = parse_variant(entry['Name'])
                    if genus is not '' and species is not '':
                        this.active_journal.planets[target_body].add_flora(genus, species, color)

                    set_codex(session, this.active_journal.cmdr.id, entry['Name'], this.active_journal.system.region)


def get_body_name(fullname: str = '') -> str:
    """
    Remove the base system name from the body name if the body has a unique identifier.
    Usually only the main star has the same name as the system in one-star systems.

    :param fullname: The full name of the body including the system name
    :return: The short name of the body unless it matches the system name
    """

    if fullname.startswith(this.active_journal.system.name + ' '):
        body_name = fullname[len(this.active_journal.system.name + ' '):]
    else:
        body_name = fullname
    return body_name


def set_cmdr(name: str, session) -> None:
    this.active_journal.cmdr = session.scalar(select(Commander).where(Commander.name == name))
    if not this.active_journal.cmdr:
        this.active_journal.cmdr = Commander(name=name)
        session.add(this.active_journal.cmdr)
        session.commit()


def set_system(name: str, address: list[float], session: Session) -> None:
    this.active_journal.system = session.scalar(select(System).where(System.name == name))
    if not this.active_journal.system:
        this.active_journal.system = System(name=name)
        session.add(this.active_journal.system)
    if address:
        this.active_journal.system.x = address[0]
        this.active_journal.system.y = address[1]
        this.active_journal.system.z = address[2]
        region = findRegion(address[0], address[1], address[2])
        if region:
            this.active_journal.system.region = region[0]
    session.commit()


def add_star(entry: MutableMapping[str, Any], session: Session) -> None:
    """
    Add main star data from journal event

    :param entry: The journal event dict (must be a Scan event with star data)
    :param session: The DB session
    """

    body_short_name = get_body_name(entry['BodyName'])

    if body_short_name not in this.active_journal.stars:
        star_data = StarData.from_journal(this.active_journal.system, body_short_name, entry['BodyID'], session)
    else:
        star_data = this.active_journal.stars[body_short_name]

    star_data.set_distance(entry['DistanceFromArrivalLS']) \
        .set_type(entry['StarType']) \
        .set_luminosity(entry['Luminosity'])

    session.commit()

    this.active_journal.stars[body_short_name] = star_data


def add_planet(entry: MutableMapping[str, Any], session: Session) -> None:
    body_short_name = get_body_name(entry['BodyName'])
    if body_short_name not in this.active_journal.planets:
        body_data = PlanetData.from_journal(this.active_journal.system, body_short_name, entry['BodyID'], session)
    else:
        body_data = this.active_journal.planets[body_short_name]
    body_data.set_distance(float(entry['DistanceFromArrivalLS'])).set_type(entry['PlanetClass']) \
        .set_gravity(entry['SurfaceGravity']).set_temp(entry.get('SurfaceTemperature', None)) \
        .set_volcanism(entry.get('Volcanism', None))

    star_search = re.search('^([A-Z]+) .+$', body_short_name)
    if star_search:
        for star in star_search.group(1):
            body_data.add_parent_star(star)
    else:
        body_data.add_parent_star(this.active_journal.system.name)

    if 'Materials' in entry:
        for material in entry['Materials']:
            body_data.add_material(material['Name'])

    if 'AtmosphereType' in entry:
        body_data.set_atmosphere(entry['AtmosphereType'])

    if 'AtmosphereComposition' in entry:
        for gas in entry['AtmosphereComposition']:
            body_data.add_gas(gas['Name'], gas['Percent'])

    session.commit()

    this.active_journal.planets[body_short_name] = body_data


def add_signals(entry: MutableMapping[str, Any], session: Session) -> None:
    body_short_name = get_body_name(entry['BodyName'])

    if body_short_name not in this.active_journal.planets:
        body_data = PlanetData.from_journal(this.active_journal.system, body_short_name, entry['BodyID'], session)
    else:
        body_data = this.active_journal.planets[body_short_name].set_id(entry['BodyID'])

    # Add bio signal number just in case
    for signal in entry['Signals']:
        if signal['Type'] == '$SAA_SignalType_Biological;':
            body_data.set_bio_signals(signal['Count'])

    # If signals include genuses, add them to the body data
    if 'Genuses' in entry:
        for genus in entry['Genuses']:
            if body_data.get_flora(genus['Genus']) is None:
                body_data.add_flora(genus['Genus'])

    this.active_journal.planets[body_short_name] = body_data

    session.commit()


def add_scan(entry: MutableMapping[str, Any], session: Session) -> None:
    target_body = None
    for name, body in this.active_journal.planets.items():
        if body.get_id() == entry['Body']:
            target_body = name
            break

    scan_level = 0
    match entry['ScanType']:
        case 'Log':
            scan_level = 1
        case 'Sample':
            scan_level = 2
        case 'Analyse':
            scan_level = 3

    if target_body is not None:
        if scan_level == 3:
            this.active_journal.planets[target_body].set_flora_species_scan(
                entry['Genus'], entry['Species'], scan_level, this.active_journal.cmdr.id
            )

        if 'Variant' in entry:
            _, _, color = parse_variant(entry['Variant'])
            this.active_journal.planets[target_body].set_flora_color(entry['Genus'], color)
