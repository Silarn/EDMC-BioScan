# -*- coding: utf-8 -*-
# BioScan plugin for EDMC
# Source: https://github.com/Silarn/EDMC-BioScan
# Licensed under the [GNU Public License (GPL)](http://www.gnu.org/licenses/gpl-2.0.html) version 2 or later.

# Core imports
import sys
import threading
from typing import Mapping, MutableMapping
from urllib.parse import quote
import requests
import semantic_version
import math

# TKinter imports
import tkinter as tk
from tkinter import ttk

# Local imports
from bio_scan.nebula_coordinates import nebulae_coords
from bio_scan.nebulae_data import planetary_nebulae, nebulae_sectors
from bio_scan.status_flags import StatusFlags2, StatusFlags
from bio_scan.body_data import BodyData, get_body_shorthand, body_check, parse_edsm_star_class, \
    map_edsm_type, map_edsm_atmosphere
from bio_scan.bio_data import bio_genus, bio_types, get_species_from_codex, region_map, guardian_sectors
from bio_scan.format_util import Formatter

# EDMC imports
from config import config
from theme import theme
from EDMCLogging import get_main_logger
import myNotebook as nb
from ttkHyperlinkLabel import HyperlinkLabel

# 3rd Party
from RegionMap import findRegion


logger = get_main_logger()


class This:
    """Holds module globals."""

    def __init__(self):
        self.formatter = Formatter()

        self.VERSION = '1.2.0'

        # Settings vars
        self.focus_setting: tk.StringVar | None = None
        self.signal_setting: tk.StringVar | None = None
        self.debug_logging_enabled: tk.BooleanVar | None = None

        # GUI Objects
        self.frame: tk.Frame | None = None
        self.scroll_canvas: tk.Canvas | None = None
        self.scrollbar: ttk.Scrollbar | None = None
        self.scrollable_frame: ttk.Frame | None = None
        self.label: tk.Label | None = None
        self.values_label: tk.Label | None = None
        self.total_label: tk.Label | None = None
        self.edsm_button: tk.Label | None = None

        # Plugin state data
        self.bodies: dict[str, BodyData] = {}
        self.odyssey: bool = False
        self.game_version: semantic_version.Version = semantic_version.Version.coerce('0.0.0.0')
        self.main_star_type: str = ''
        self.coordinates: list[float, float, float] = [0.0, 0.0, 0.0]
        self.location_name: str = ''
        self.location_id: str = ''
        self.location_state: str = ''
        self.planet_radius: float = 0.0
        self.planet_latitude: float | None = None
        self.planet_longitude: float | None = None
        self.scan_latitude: list[float] = []
        self.scan_longitude: list[float] = []
        self.current_scan: str = ''
        self.starsystem: str = ''

        # EDSM vars
        self.edsm_session = None
        self.edsm_bodies = None
        self.fetched_edsm = False


this = This()


# Compatibility fallback
def plugin_start3(plugin_dir) -> str:
    """ EDMC start hook """

    return 'BioScan'


def plugin_app(parent: tk.Frame) -> tk.Frame:
    """ EDMC initialization """

    parse_config()
    this.frame = tk.Frame(parent)
    this.frame.bind('<<BioScanEDSMData>>', edsm_data)
    this.label = tk.Label(this.frame)
    this.label.grid(row=0, column=0, columnspan=2, sticky=tk.N)
    this.scroll_canvas = tk.Canvas(this.frame, height=80, highlightthickness=0)
    this.scrollbar = ttk.Scrollbar(this.frame, orient='vertical', command=this.scroll_canvas.yview)
    this.scrollable_frame = ttk.Frame(this.scroll_canvas)
    this.scrollable_frame.bind(
        '<Configure>',
        lambda e: this.scroll_canvas.configure(
            scrollregion=this.scroll_canvas.bbox('all')
        )
    )
    this.scroll_canvas.bind('<Enter>', bind_mousewheel)
    this.scroll_canvas.bind('<Leave>', unbind_mousewheel)
    this.scroll_canvas.create_window((0, 0), window=this.scrollable_frame, anchor='nw')
    this.scroll_canvas.configure(yscrollcommand=this.scrollbar.set)
    this.values_label = ttk.Label(this.scrollable_frame)
    this.values_label.pack(fill='both', side='left')
    this.scroll_canvas.grid(row=1, column=0, sticky=tk.EW)
    this.scroll_canvas.grid_rowconfigure(1, weight=0)
    this.frame.grid_columnconfigure(0, weight=1)
    this.scrollbar.grid(row=1, column=1, sticky=tk.NSEW)
    this.total_label = tk.Label(this.frame)
    this.total_label.grid(row=2, column=0, columnspan=2, sticky=tk.N)
    this.edsm_button = tk.Label(this.frame, text='Fetch EDSM Data', fg='white', cursor='hand2')
    this.edsm_button.grid(row=3, columnspan=2, sticky=tk.EW)
    this.edsm_button.bind('<Button-1>', lambda e: edsm_fetch())
    update_display()
    theme.register(this.values_label)
    return this.frame


def plugin_prefs(parent: ttk.Notebook, cmdr: str, is_beta: bool) -> tk.Frame:
    """ EDMC settings pane hook """

    x_padding = 10
    x_button_padding = 12
    y_padding = 2
    frame = nb.Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(20, weight=1)

    HyperlinkLabel(frame, text='BioScan', background=nb.Label().cget('background'),
                   url='https://github.com/Silarn/EDMC-BioScan', underline=True) \
        .grid(row=1, padx=x_padding, sticky=tk.W)
    nb.Label(frame, text = 'Version %s' % this.VERSION).grid(row=1, column=1, padx=x_padding, sticky=tk.E)

    ttk.Separator(frame).grid(row=5, columnspan=2, pady=y_padding*2, sticky=tk.EW)

    nb.Label(
        frame,
        text='Focus Body Signals:',
    ).grid(row=10, padx=x_padding, sticky=tk.W)
    focus_options = [
        'Never',
        'On Approach',
        'On Surface',
    ]
    nb.OptionMenu(
        frame,
        this.focus_setting,
        this.focus_setting.get(),
        *focus_options
    ).grid(row=11, padx=x_padding, pady=y_padding, column=0, sticky=tk.W)
    nb.Label(frame,
             text='Never: Never filter signal details\n' +
                  'On Approach: Show only local signals on approach\n' +
                  'On Surface: Show only local signals when on surface',
             justify=tk.LEFT) \
        .grid(row=12, padx=x_padding, column=0, sticky=tk.NW)

    nb.Label(
        frame,
        text='Display Signal Summary:'
    ).grid(row=10, column=1, sticky=tk.W)
    signal_options = [
        'Always',
        'In Flight',
    ]
    nb.OptionMenu(
        frame,
        this.signal_setting,
        this.signal_setting.get(),
        *signal_options
    ).grid(row=11, column=1, pady=y_padding, sticky=tk.W)
    nb.Label(frame,
             text='Always: Always display the body signal summary\n' +
                  'In Flight: Show the signal summary in flight only',
             justify=tk.LEFT) \
        .grid(row=12, column=1, sticky=tk.NW)

    nb.Checkbutton(
        frame,
        text='Enable Debug Logging',
        variable=this.debug_logging_enabled
    ).grid(row=20, column=1, padx=x_button_padding, sticky=tk.SE)
    return frame


def prefs_changed(cmdr: str, is_beta: bool) -> None:
    """ EDMC settings changed hook """

    config.set('bioscan_focus', this.focus_setting.get())
    config.set('bioscan_signal', this.signal_setting.get())
    config.set('bioscan_debugging', this.debug_logging_enabled.get())
    update_display()


def parse_config() -> None:
    """ Load saved settings vars """

    this.focus_setting = tk.StringVar(value=config.get_str(key='bioscan_focus', default='On Approach'))
    this.signal_setting = tk.StringVar(value=config.get_str(key='bioscan_signal', default='Always'))
    this.debug_logging_enabled = tk.BooleanVar(value=config.get_bool(key='bioscan_debugging', default=False))


def log(*args) -> None:
    """ Debug logger helper function """

    if this.debug_logging_enabled.get():
        logger.debug(args)


def edsm_fetch() -> None:
    """ EDSM system data fetch thread initialization """

    thread = threading.Thread(target=edsm_worker, name='EDSM worker', args=(this.starsystem,))
    thread.daemon = True
    thread.start()


def edsm_worker(system_name: str) -> None:
    """ Fetch system data from EDSM on a threaded function """

    if not this.edsm_session:
        this.edsm_session = requests.Session()

    try:
        r = this.edsm_session.get('https://www.edsm.net/api-system-v1/bodies?systemName=%s' % quote(system_name),
                                  timeout=10)
        r.raise_for_status()
        this.edsm_bodies = r.json() or {}
    except requests.exceptions.RequestException:
        this.edsm_bodies = None

    this.frame.event_generate('<<BioScanEDSMData>>', when='tail')


def edsm_data(event: tk.Event) -> None:
    """ Handle data retrieved from EDSM """

    if this.edsm_bodies is None:
        return

    for body in this.edsm_bodies.get('bodies', []):
        body_short_name = get_body_name(body['name'])
        if body['type'] == 'Star':
            if body['isMainStar']:
                this.main_star_type = '{}{}'.format(
                    parse_edsm_star_class(body['subType']),
                    body['luminosity']
                )

        elif body['type'] == 'Planet':
            try:
                if body_short_name not in this.bodies:
                    this.bodies[body_short_name] = BodyData(body_short_name)
                planet_type = map_edsm_type(body['subType'])
                this.bodies[body_short_name].set_type(planet_type)
                this.bodies[body_short_name].set_distance(body['distanceToArrival'])
                this.bodies[body_short_name].set_id(body['bodyId'])
                this.bodies[body_short_name].set_atmosphere(map_edsm_atmosphere(body['atmosphereType']))
                if body['volcanismType'] == 'No volcanism':
                    volcanism = ''
                else:
                    volcanism = body['volcanismType'].lower().capitalize() + ' volcanism'
                this.bodies[body_short_name].set_volcanism(volcanism)
                this.bodies[body_short_name].set_gravity(body['gravity'])
                this.bodies[body_short_name].set_temp(body['surfaceTemperature'])

            except Exception as e:
                logger.error(e)
    this.fetched_edsm = True
    update_display()


def scan_label(scans: int) -> str:
    """ Return the label for the scan stage """

    match scans:
        case 0:
            return 'Located'
        case 1:
            return 'Logged'
        case 2:
            return 'Sampled'
        case 3:
            return 'Analysed'


def value_estimate(body: BodyData, genus: str) -> tuple[str, int, int]:
    """ Main function to make species determinations from body data.
    Returns the display name and the minimum and maximum values """

    possible_species = set()
    eliminated_species = set()
    log('Running checks for {}:'.format(bio_genus[genus]['name']))
    for species, reqs in bio_types[genus].items():
        possible_species.add(species)
        log(species)
        if reqs[2] is not None:
            if reqs[2] == 'Any' and body.get_atmosphere() in ['', 'None']:
                log('Eliminated for no atmos')
                eliminated_species.add(species)
                continue
            elif body.get_atmosphere() not in reqs[2]:
                log('Eliminated for atmos')
                eliminated_species.add(species)
                continue
        if reqs[3] is not None:
            if body.get_gravity() / 9.80665 > reqs[3]:
                log('Eliminated for grav')
                eliminated_species.add(species)
                continue
        if reqs[4] is not None:
            if body.get_temp() > reqs[4]:
                log('Eliminated for high heat')
                eliminated_species.add(species)
                continue
        if reqs[5] is not None:
            if body.get_temp() < reqs[5]:
                log('Eliminated for low heat')
                eliminated_species.add(species)
                continue
        if reqs[6] is not None:
            if reqs[6] == 'Any' and body.get_volcanism() == '':
                log('Eliminated for no volcanism')
                eliminated_species.add(species)
                continue
            else:
                found = False
                for volc_type in reqs[6]:
                    if body.get_volcanism().find(volc_type) != -1:
                        found = True
                if not found:
                    log('Eliminated for volcanism')
                    eliminated_species.add(species)
                    continue
        if reqs[7] is not None:
            if body.get_type() not in reqs[7]:
                log('Eliminated for body type')
                eliminated_species.add(species)
                continue
        if reqs[8] is not None:
            if this.coordinates is not None:
                found = None
                for region in reqs[8]:
                    region_id = findRegion(*this.coordinates)
                    if region_id is not None:
                        log('Current region: {} - {}'.format(region_id[0], region_id[1]))
                        if region.startswith('!'):
                            if region_id[0] in region_map[region[1:]]:
                                log('Eliminated by region')
                                eliminated_species.add(species)
                                continue
                        else:
                            found = False if found is None else found
                            if region_id[0] in region_map[region]:
                                found = True
                if not found and found is not None:
                    log('Eliminated by region')
                    eliminated_species.add(species)
                    continue
        if reqs[9] is not None:
            match reqs[9]:
                case '2500ls':
                    if body.get_distance() < 2500.0:
                        eliminated_species.add(species)
                case 'guardian':
                    found = False
                    for sector in guardian_sectors:
                        if this.starsystem.startswith(sector):
                            found = True
                            break
                    if not found:
                        log('Eliminated for not being in a guardian sector')
                        eliminated_species.add(species)
                case 'guardian+life':
                    found = False
                    for sector in guardian_sectors:
                        if this.starsystem.startswith(sector):
                            found = True
                            break
                    if not found:
                        log('Eliminated for not being in a guardian sector')
                        eliminated_species.add(species)
                    if not body_check(this.bodies):
                        log('Eliminated for missing body type(s)')
                        eliminated_species.add(species)
                case 'life':
                    if not body_check(this.bodies):
                        log('Eliminated for missing body type(s)')
                        eliminated_species.add(species)
                case 'A+life':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type[0] != 'A':
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                            continue
                    if not body_check(this.bodies):
                        log('Eliminated for missing body type(s)')
                        eliminated_species.add(species)
                case 'AV':
                    if len(this.main_star_type) > 0:
                        if not this.main_star_type.startswith('A') and not this.main_star_type.startswith('N'):
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                            continue
                        elif this.main_star_type.startswith('AVI'):
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                case 'A':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type[0] != 'A':
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                case 'B':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type[0] != 'B':
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                case 'AB':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type[0] not in ['A', 'B']:
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                case 'O':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type[0] != 'O':
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                case 'AFGKMSS':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type[0] not in ['A', 'F', 'G', 'K', 'S'] and \
                                not this.main_star_type.startswith('MS'):
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                            continue
                        if body.get_distance() < 12000.0:
                            log('Eliminated for distance')
                            eliminated_species.add(species)
                            continue
                        if not body_check(this.bodies, True):
                            log('Eliminated for missing body type(s)')
                            eliminated_species.add(species)
                case 'nebula':
                    found = False
                    if this.starsystem in planetary_nebulae:
                        found = True
                    for sector in nebulae_sectors:
                        if this.starsystem.startswith(sector):
                            found = True
                            break
                    for system, coords in nebulae_coords.items():
                        distance = math.sqrt((coords[0]-this.coordinates[0])**2
                                             + (coords[1]-this.coordinates[1])**2
                                             + (coords[2]-this.coordinates[2])**2)
                        log('Distance to {0} from {1}: {2:n} ly'.format(system, this.starsystem, distance))
                        if distance < 100.0:
                            found = True
                            break
                    if not found:
                        log('Eliminated for lack of nebula')
                        eliminated_species.add(species)

    final_species = possible_species - eliminated_species
    sorted_species = sorted(final_species, key=lambda target_species: bio_types[genus][target_species][1])

    if len(sorted_species) == 1:
        return bio_types[genus][sorted_species[0]][0], \
            bio_types[genus][sorted_species[0]][1], \
            bio_types[genus][sorted_species[0]][1]
    if len(sorted_species) > 0:
        return bio_genus[genus]['name'], \
            bio_types[genus][sorted_species[0]][1], \
            bio_types[genus][sorted_species[-1]][1]
    return '', 0, 0


def get_possible_values(body: BodyData) -> dict[str, tuple]:
    """ For unmapped planets, run through every genus and make species determinations """

    possible_genus = {}
    for genus, species_reqs in bio_types.items():
        name, min_potential_value, max_potential_value = value_estimate(body, genus)
        if min_potential_value != 0:
            possible_genus[name] = (min_potential_value, max_potential_value)

    return dict(sorted(possible_genus.items(), key=lambda gen_v: gen_v[0]))


def get_body_name(fullname: str = '') -> str:
    """ Remove the base system name from the body name if the body has a unique identifier.
    Usually only the main star has the same name as the system in one-star systems. """

    if fullname.startswith(this.starsystem + ' '):
        body_name = fullname[len(this.starsystem + ' '):]
    else:
        body_name = fullname
    return body_name


def reset() -> None:
    """ Reset system data when location changes """

    this.starsystem = ''
    this.main_star_type = ''
    this.location_name = ''
    this.location_id = -1
    this.location_state = ''
    this.fetched_edsm = False
    this.bodies = {}
    this.scroll_canvas.yview_moveto(0.0)


def journal_entry(
        cmdr: str, is_beta: bool, system: str, station: str, entry: Mapping[str, any], state: MutableMapping[str, any]
) -> str:
    """ EDMC journal entry hook. Primary journal data handler. """

    system_changed = False
    this.game_version = semantic_version.Version.coerce(state.get('GameVersion', '0.0.0'))
    this.odyssey = state.get('Odyssey', False)
    if system and system != this.starsystem:
        reset()
        system_changed = True
        this.starsystem = system

    elif entry['event'] in ['Location', 'FSDJump']:
        this.coordinates = entry['StarPos']

    elif entry['event'] == 'Scan':
        body_short_name = get_body_name(entry['BodyName'])
        if 'StarType' in entry:
            if entry['DistanceFromArrivalLS'] == 0.0:
                this.main_star_type = '{}{}'.format(entry['StarType'], entry['Luminosity'])
        if 'PlanetClass' in entry:
            if body_short_name not in this.bodies:
                body_data = BodyData(body_short_name)
            else:
                body_data = this.bodies[body_short_name]
            body_data.set_distance(float(entry['DistanceFromArrivalLS'])).set_type(entry['PlanetClass']) \
                .set_id(entry['BodyID']).set_gravity(entry['SurfaceGravity']) \
                .set_temp(entry['SurfaceTemperature']).set_volcanism(entry['Volcanism'])

            if 'AtmosphereType' in entry:
                body_data.set_atmosphere(entry['AtmosphereType'])

            this.bodies[body_short_name] = body_data

            update_display()

    elif entry['event'] == 'FSSBodySignals':
        body_short_name = get_body_name(entry['BodyName'])
        if body_short_name not in this.bodies:
            this.bodies[body_short_name] = BodyData(body_short_name)
        for signal in entry['Signals']:
            if signal['Type'] == '$SAA_SignalType_Biological;':
                this.bodies[body_short_name].set_bio_signals(signal['Count'])

        update_display()

    elif entry['event'] == 'SAASignalsFound':
        body_short_name = get_body_name(entry['BodyName'])

        if body_short_name not in this.bodies:
            body_data = BodyData(body_short_name).set_id(entry['BodyID'])
        else:
            body_data = this.bodies[body_short_name].set_id(entry['BodyID'])

        # Add bio signal number just in case
        for signal in entry['Signals']:
            if signal['Type'] == '$SAA_SignalType_Biological;':
                body_data.set_bio_signals(signal['Count'])

        # If signals include genuses, add them to the body data
        if 'Genuses' in entry:
            for genus in entry['Genuses']:
                if body_data.get_flora(genus['Genus']) is None:
                    body_data.add_flora(genus['Genus'])
        this.bodies[body_short_name] = body_data

        update_display()

    elif entry['event'] == 'ScanOrganic':
        target_body = None
        for name, body in this.bodies.items():
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
            this.bodies[target_body].set_flora(entry['Genus'], entry['Species'], scan_level)
            if this.current_scan != '' and this.current_scan != entry['Genus']:
                species = this.bodies[target_body].get_flora(this.current_scan)[0]
                this.bodies[target_body].set_flora(this.current_scan, species, 0)
                this.scan_latitude.clear()
                this.scan_longitude.clear()
            this.current_scan = entry['Genus']

        match scan_level:
            case 1 | 2:
                this.scan_latitude.append(this.planet_latitude)
                this.scan_longitude.append(this.planet_longitude)
            case _:
                this.scan_latitude.clear()
                this.scan_longitude.clear()
                this.current_scan = ''

        update_display()

    elif entry['event'] == 'CodexEntry' and \
            entry['BodyID'] == this.location_id and \
            entry['Category'] == '$Codex_Category_Biology;':
        target_body = None
        for name, body in this.bodies.items():
            if body.get_id() == entry['BodyID']:
                target_body = name
                break

        if target_body is not None:
            genus, species = get_species_from_codex(entry['Name'])
            if genus is not '' and species is not '':
                this.bodies[target_body].add_flora(genus, species)

        update_display()

    elif entry['event'] in ['ApproachBody', 'Touchdown', 'Liftoff']:
        if entry['event'] in ['Liftoff', 'Touchdown'] and entry['PlayerControlled'] is False:
            return ''
        body_name = get_body_name(entry['Body'])
        if body_name in this.bodies:
            this.location_name = body_name
            this.location_id = entry['BodyID']

        if entry['event'] in ['ApproachBody', 'Liftoff']:
            this.location_state = 'approach'
        else:
            this.location_state = 'surface'

        update_display()

        if this.focus_setting.get() == 'On Approach' and entry['event'] == 'ApproachBody':
            this.scroll_canvas.yview_moveto(0.0)

        if this.focus_setting.get() == 'On Surface' and entry['event'] in ['Touchdown', 'Liftoff']:
            this.scroll_canvas.yview_moveto(0.0)

    elif entry['event'] == 'LeaveBody':
        this.location_name = ''
        this.location_id = -1
        this.location_state = ''

        update_display()
        this.scroll_canvas.yview_moveto(0.0)

    if system_changed:
        update_display()

    return ''  # No error


def dashboard_entry(cmdr: str, is_beta: bool, entry: dict[str, any]) -> str:
    """ EDMC dashboard entry hook. Parses updates to the Status.json. """

    status = StatusFlags(entry['Flags'])
    status2 = StatusFlags2(0)
    if 'Flags2' in entry:
        status2 = StatusFlags2(entry['Flags2'])
    refresh = False

    current_state = this.location_state
    this.location_state = ''
    if StatusFlags.HAVE_LATLONG in status:
        if StatusFlags.IN_SHIP in status:
            if StatusFlags.LANDED in status:
                this.location_state = 'surface'
            else:
                this.location_state = 'approach'
        elif StatusFlags.IN_SRV in status or StatusFlags.LANDED in status:
            this.location_state = 'surface'
        elif StatusFlags2.ON_FOOT in status2 and StatusFlags2.PLANET_ON_FOOT in status2 \
                and StatusFlags2.SOCIAL_ON_FOOT not in status2 and StatusFlags2.STATION_ON_FOOT not in status2:
            this.location_state = 'surface'

    if current_state != this.location_state:
        refresh = True

    if StatusFlags.HAVE_LATLONG in status:
        if StatusFlags.HAVE_ALTITUDE in status:
            this.planet_altitude = entry['Altitude'] if 'Altitidue' in entry else 0
        this.planet_latitude = entry['Latitude']
        this.planet_longitude = entry['Longitude']
        this.planet_radius = entry['PlanetRadius']
        if this.location_name != '' and this.current_scan != '':
            refresh = True
    else:
        this.planet_latitude = None
        this.planet_longitude = None
        this.planet_altitude = 0
        this.planet_radius = 0

    if refresh:
        update_display()

    return ''


def get_distance() -> float | None:
    """ Use the haversine formula to do distance calculations against your scan locations
    and return the shortest distance. """

    distance_list = []
    if this.planet_latitude is not None and this.planet_longitude is not None:
        if len(this.scan_latitude) == len(this.scan_longitude) and len(this.scan_latitude) > 0:
            for i, _ in enumerate(this.scan_latitude):
                phi_1 = math.radians(this.planet_latitude)
                phi_2 = math.radians(this.scan_latitude[i])
                delta_phi = math.radians(this.scan_latitude[i] - this.planet_latitude)
                delta_lambda = math.radians(this.scan_longitude[i] - this.planet_longitude)
                a = math.sin(delta_phi / 2.0) ** 2 + \
                    math.cos(phi_1) * math.cos(phi_2) * \
                    math.sin(delta_lambda / 2.0) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance_list.append(this.planet_radius * c)
            return min(distance_list)
    return None


def get_bodies_summary(bodies: dict[str, BodyData], focused: bool = False) -> tuple[str, int]:
    """ Get body genus estimate display text for the scroll pane """

    detail_text = ''
    value_sum = 0
    for name, body in bodies.items():
        if not focused:
            detail_text += '{}:\n'.format(name)
        if len(body.get_flora()) > 0:
            count = 0
            for genus, data in body.get_flora().items():
                count += 1
                if data[1] == 3:
                    value_sum += bio_types[genus][data[0]][1]
                if data[0] != '':
                    detail_text += '{} ({}): {}{}\n'.format(
                        bio_types[genus][data[0]][0],
                        scan_label(data[1]),
                        this.formatter.format_credits(bio_types[genus][data[0]][1]),
                        u' 🗸' if data[1] == 3 else ''
                    )
                else:
                    bio_name, min_val, max_val = value_estimate(body, genus)
                    detail_text += '{} (Not located): {}\n'.format(
                        bio_name,
                        this.formatter.format_credit_range(min_val, max_val))
                if len(body.get_flora()) == count:
                    detail_text += '\n'

        else:
            types = get_possible_values(body)
            detail_text += '{} Signals - Possible Types:\n'.format(body.get_bio_signals())
            count = 0
            for bio_name, values in types.items():
                count += 1
                detail_text += '{}: {}\n'.format(
                    bio_name,
                    this.formatter.format_credit_range(values[0], values[1])
                )
                if len(types) == count:
                    detail_text += '\n'

    return detail_text, value_sum


def update_display() -> None:
    """ Primary display update function. This is run whenever we get an event that would change the display state. """

    if this.fetched_edsm or this.starsystem == '':
        this.edsm_button.grid_remove()
    else:
        this.edsm_button.grid()

    bio_bodies = dict(sorted(dict(filter(lambda fitem: fitem[1].get_bio_signals() > 0 or len(fitem[1].get_flora()) > 0, this.bodies.items())).items(),
                        key=lambda item: item[1].get_id()))
    exobio_body_names = [
        '%s%s: %d' % (body_name, get_body_shorthand(body_data.get_type()), body_data.get_bio_signals())
        for body_name, body_data
        in bio_bodies.items()
    ]

    if (this.location_name != '' and this.location_name in bio_bodies) and this.focus_setting.get() != 'Never' and \
            ((this.focus_setting.get() == 'On Approach' and this.location_state in ['approach', 'surface'])
             or (this.focus_setting.get() == 'On Surface' and this.location_state == 'surface')):
        detail_text, total_value = get_bodies_summary({this.location_name: this.bodies[this.location_name]}, True)
    else:
        detail_text, total_value = get_bodies_summary(bio_bodies)

    if len(bio_bodies) > 0:
        this.scroll_canvas.grid()
        this.scrollbar.grid()
        this.total_label.grid()
        text = 'BioScan Estimates:\n'

        if this.signal_setting.get() == 'Always' or this.location_state != 'surface':
            while True:
                exo_list = exobio_body_names[:5]
                exobio_body_names = exobio_body_names[5:]
                text += ' ⬦ '.join([b for b in exo_list])
                if len(exobio_body_names) == 0:
                    break
                else:
                    text += '\n'

        if (this.location_name != '' and this.location_name in bio_bodies) and this.focus_setting.get() != 'Never' and \
                ((this.focus_setting.get() == 'On Approach' and this.location_state in ['approach', 'surface'])
                 or (this.focus_setting.get() == 'On Surface' and this.location_state == 'surface')):
            if text[-1] != '\n':
                text += '\n'
            complete = len(dict(filter(lambda x: x[1][1] == 3, bio_bodies[this.location_name].get_flora().items())))
            text += '{} - {} [{}G] - {}/{} Analysed'.format(
                bio_bodies[this.location_name].get_name(),
                bio_bodies[this.location_name].get_type(),
                '{:.2f}'.format(bio_bodies[this.location_name].get_gravity() / 9.80665).rstrip('0').rstrip('.'),
                complete, len(bio_bodies[this.location_name].get_flora())
            )
            for genus, data in this.bodies[this.location_name].get_flora().items():
                if 0 < data[1] < 3:
                    distance = get_distance()
                    distance_format = '{:.2f}'.format(distance) if distance is not None else 'unk'
                    distance = distance if distance is not None else 0
                    text += '\nIn Progress: {} - {} ({}/3) [{}]'.format(
                        bio_types[genus][data[0]][0],
                        scan_label(data[1]),
                        data[1],
                        '{}/{}m'.format(
                            distance_format
                            if distance < bio_genus[genus]['distance']
                            else '> {}'.format(bio_genus[genus]['distance']),
                            bio_genus[genus]['distance']
                        )
                    )
                    break

        this.total_label['text'] = 'Analysed System Samples:\n{} | FF: {}'.format(
            this.formatter.format_credits(total_value),
            this.formatter.format_credits((total_value * 5)))
    else:
        this.scroll_canvas.grid_remove()
        this.scrollbar.grid_remove()
        this.total_label.grid_remove()
        text = 'BioScan: No Signals Found'
        this.total_label['text'] = ''

    this.label['text'] = text
    this.values_label['text'] = detail_text

    # if this.show_details.get():
    #     this.scroll_canvas.grid()
    #     this.scrollbar.grid()
    # else:
    #     this.scroll_canvas.grid_remove()
    #     this.scrollbar.grid_remove()


def bind_mousewheel(event: tk.Event) -> None:
    """ Scroll pane mousewheel bind on mouseover """

    if sys.platform in ('linux', 'cygwin', 'msys'):
        this.scroll_canvas.bind_all('<Button-4>', on_mousewheel)
        this.scroll_canvas.bind_all('<Button-5>', on_mousewheel)
    else:
        this.scroll_canvas.bind_all('<MouseWheel>', on_mousewheel)


def unbind_mousewheel(event: tk.Event) -> None:
    """ Scroll pane mousewheel unbind on mouseout """

    if sys.platform in ('linux', 'cygwin', 'msys'):
        this.scroll_canvas.unbind_all('<Button-4>')
        this.scroll_canvas.unbind_all('<Button-5>')
    else:
        this.scroll_canvas.unbind_all('<MouseWheel>')


def on_mousewheel(event: tk.Event) -> None:
    """ Scroll pane mousewheel event handler """

    shift = (event.state & 0x1) != 0
    scroll = 0
    if event.num == 4 or event.delta == 120:
        scroll = -1
    if event.num == 5 or event.delta == -120:
        scroll = 1
    if shift:
        this.scroll_canvas.xview_scroll(scroll, 'units')
    else:
        this.scroll_canvas.yview_scroll(scroll, 'units')
