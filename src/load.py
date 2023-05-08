# -*- coding: utf-8 -*-
# BioScan plugin for EDMC
# Source: https://github.com/Silarn/EDMC-BioScan
# Licensed under the [GNU Public License (GPL)](http://www.gnu.org/licenses/gpl-2.0.html) version 2 or later.

# Core imports
import sys
import threading
from traceback import print_exc
from typing import Mapping, MutableMapping
from urllib.parse import quote
import requests
import semantic_version
import math

# TKinter imports
import tkinter as tk
from tkinter import ttk

# Local imports
from bio_scan.nebula_data.reference_stars import coordinates as nebula_coords
from bio_scan.nebula_data.sectors import planetary_nebulae, data as nebula_sectors
from bio_scan.status_flags import StatusFlags2, StatusFlags
from bio_scan.body_data.struct import PlanetData, StarData
from bio_scan.body_data.util import get_body_shorthand, body_check
from bio_scan.body_data.edsm import parse_edsm_star_class, map_edsm_type, map_edsm_atmosphere
from bio_scan.bio_data.codex import get_species_from_codex
from bio_scan.bio_data.genus import data as bio_genus
from bio_scan.bio_data.regions import region_map, guardian_sectors
from bio_scan.bio_data.species import rules as bio_types
from bio_scan.format_util import Formatter

# EDMC imports
from config import config
from theme import theme
from EDMCLogging import get_main_logger
import myNotebook as nb
from ttkHyperlinkLabel import HyperlinkLabel

# 3rd Party
from bio_scan.RegionMap import findRegion


logger = get_main_logger()


class This:
    """Holds module globals."""

    def __init__(self):
        self.formatter = Formatter()

        self.VERSION = semantic_version.Version('1.5.0')

        # Settings vars
        self.focus_setting: tk.StringVar | None = None
        self.signal_setting: tk.StringVar | None = None
        self.focus_breakdown: tk.BooleanVar | None = None
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
        self.edsm_failed: tk.Label | None = None

        # Plugin state data
        self.planets: dict[str, PlanetData] = {}
        self.stars: dict[int, StarData] = {}
        self.planet_cache: dict[str, dict[str, tuple[bool, tuple[str, int, int, list[tuple[str, str, int]]]]]] = {}
        self.barycenters: dict[int, list[id]] = {}

        # self.odyssey: bool = False
        # self.game_version: semantic_version.Version = semantic_version.Version.coerce('0.0.0.0')
        self.main_star_type: str = ''
        self.main_star_luminosity: str = ''
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
    this.edsm_failed = tk.Label(this.frame, text='No EDSM Data Found')
    update = version_check()
    if update != '':
        text = 'Version {} is now available'.format(update)
        url = 'https://github.com/Silarn/EDMC-BioScan/releases/tag/v{}'.format(update)
        this.update_button = HyperlinkLabel(this.frame, text=text, url=url)
        this.update_button.grid(row=4, columnspan=2, sticky=tk.N)
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
    nb.Checkbutton(
        frame,
        text='Show complete breakdown of genera with multiple matches',
        variable=this.focus_breakdown
    ).grid(row=13, column=0, padx=x_button_padding, sticky=tk.W)

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
    config.set('bioscan_focus_breakdown', this.focus_breakdown.get())
    config.set('bioscan_signal', this.signal_setting.get())
    config.set('bioscan_debugging', this.debug_logging_enabled.get())
    update_display()


def parse_config() -> None:
    """ Load saved settings vars """

    this.focus_setting = tk.StringVar(value=config.get_str(key='bioscan_focus', default='On Approach'))
    this.focus_breakdown = tk.BooleanVar(value=config.get_bool(key='bioscan_focus_breakdown', default=False))
    this.signal_setting = tk.StringVar(value=config.get_str(key='bioscan_signal', default='Always'))
    this.debug_logging_enabled = tk.BooleanVar(value=config.get_bool(key='bioscan_debugging', default=False))


def version_check() -> str:
    try:
        req = requests.get(url='https://api.github.com/repos/Silarn/EDMC-BioScan/releases/latest')
        data = req.json()
        if req.status_code != requests.codes.ok:
            raise requests.RequestException
    except requests.RequestException | requests.JSONDecodeError:
        print_exc()
        return ''

    version = semantic_version.Version(data['tag_name'][1:])
    if version > this.VERSION:
        return str(version)
    return ''


def log(*args) -> None:
    """
    Debug logger helper function. Only writes to log if debug logging is enabled for BioScan.
    :param args: Arguments to be passed to the EDMC logger
    """

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

    if len(this.edsm_bodies.get('bodies', [])) == 0:
        this.edsm_failed.grid(row=3, columnspan=2, sticky=tk.EW)

    for body in this.edsm_bodies.get('bodies', []):
        body_short_name = get_body_name(body['name'])
        if body['type'] == 'Star':
            if body['isMainStar']:
                if body['spectralClass']:
                    this.main_star_type = body['spectralClass'][:-1]
                else:
                    this.main_star_type = parse_edsm_star_class(body['subType'])
                this.main_star_luminosity = body['luminosity']

        elif body['type'] == 'Planet':
            try:
                if body_short_name not in this.planets:
                    this.planets[body_short_name] = PlanetData(body_short_name)
                planet_type = map_edsm_type(body['subType'])
                this.planets[body_short_name].set_type(planet_type)
                this.planets[body_short_name].set_distance(body['distanceToArrival'])
                this.planets[body_short_name].set_id(body['bodyId'])
                this.planets[body_short_name].set_atmosphere(map_edsm_atmosphere(body['atmosphereType']))
                if body['volcanismType'] == 'No volcanism':
                    volcanism = ''
                else:
                    volcanism = body['volcanismType'].lower().capitalize() + ' volcanism'
                this.planets[body_short_name].set_volcanism(volcanism)
                this.planets[body_short_name].set_gravity(body['gravity'])
                this.planets[body_short_name].set_temp(body['surfaceTemperature'])

                if 'materials' in body:
                    for material in body['materials']:  # type: str
                        this.planets[body_short_name].add_material(material.lower())

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


def value_estimate(body: PlanetData, genus: str) -> tuple[str, int, int, list[tuple[str, str, int]]]:
    """
    Main function to make species determinations from body data.
    Returns the display name and the minimum and maximum values.
    Data is cached, and we check a flag to see if we need to recalculate the species.

    :param body: The planet data we're fetching species for
    :param genus: The genus we're checking for species requirements
    :return: The display string for the calculated genus/species, the minimum and maximum values, and a
             list of individual species if there are multiple matches
    """
    if body.get_name() in this.planet_cache:
        if genus in this.planet_cache[body.get_name()] and not this.planet_cache[body.get_name()][genus][0]:
            return this.planet_cache[body.get_name()][genus][1]
    else:
        this.planet_cache[body.get_name()] = {}

    if genus not in this.planet_cache[body.get_name()]:
        this.planet_cache[body.get_name()][genus] = (True, ('', 0, 0, []))

    possible_species: dict[str, str] = {}
    eliminated_species = set()
    log('Running checks for {}:'.format(bio_genus[genus]['name']))
    for species, reqs in bio_types[genus].items():
        possible_species[species] = ''
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
                    if not body_check(this.planets):
                        log('Eliminated for missing body type(s)')
                        eliminated_species.add(species)
                case 'life':
                    if not body_check(this.planets):
                        log('Eliminated for missing body type(s)')
                        eliminated_species.add(species)
                case 'A+life':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type != 'A':
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                            continue
                    if not body_check(this.planets):
                        log('Eliminated for missing body type(s)')
                        eliminated_species.add(species)
                case 'AV':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type not in ['A', 'N']:
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                            continue
                        elif this.main_star_type == 'A' and this.main_star_luminosity.startswith('VI'):
                            log('Eliminated for star luminosity')
                            eliminated_species.add(species)
                case 'A':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type != 'A':
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                case 'B':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type != 'B':
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                case 'AB':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type not in ['A', 'B']:
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                case 'O':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type != 'O':
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                case 'AFGKMSS':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type not in ['A', 'F', 'G', 'K', 'S', 'MS']:
                            log('Eliminated for star type')
                            eliminated_species.add(species)
                            continue
                        if body.get_distance() < 12000.0:
                            log('Eliminated for distance')
                            eliminated_species.add(species)
                            continue
                        if not body_check(this.planets, True):
                            log('Eliminated for missing body type(s)')
                            eliminated_species.add(species)
                case 'nebula':
                    found = False
                    if this.starsystem in planetary_nebulae:
                        found = True
                    for sector in nebula_sectors:
                        if this.starsystem.startswith(sector):
                            found = True
                            break
                    for system, coords in nebula_coords.items():
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

    for species in eliminated_species:
        possible_species.pop(species, None)

    if 'colors' in bio_genus[genus]:
        if 'species' in bio_genus[genus]['colors']:
            for species in possible_species:
                if 'star' in bio_genus[genus]['colors']['species'][species]:
                    for star_type in bio_genus[genus]['colors']['species'][species]['star']:
                        if body.get_parent_star() == -1:
                            continue
                        if this.stars[body.get_parent_star()].get_type() == star_type:
                            possible_species[species] = bio_genus[genus]['colors']['species'][species]['star'][star_type]
                            break
                elif 'element' in bio_genus[genus]['colors']['species'][species]:
                    for element in bio_genus[genus]['colors']['species'][species]['element']:
                        if element in body.get_materials():
                            possible_species[species] = bio_genus[genus]['colors']['species'][species]['element'][element]
                            break

                if possible_species[species] == '':
                    eliminated_species.add(species)
                    log('Eliminated for lack of color')
        else:
            color = ''
            for star_type in bio_genus[genus]['colors']['star']:
                if body.get_parent_star() == -1:
                    continue
                if this.stars[body.get_parent_star()].get_type() == star_type:
                    color = bio_genus[genus]['colors']['star'][star_type]
                    break
            if color == '':
                possible_species.clear()
                log('Eliminated genus for lack of color')
            else:
                for species in possible_species:
                    possible_species[species] = color

    final_species: dict[str, str] = {}
    for species in possible_species:
        if species not in eliminated_species:
            final_species[species] = possible_species[species]

    sorted_species = sorted(final_species.items(), key=lambda target_species: bio_types[genus][target_species[0]][1])

    if len(sorted_species) == 1:
        this.planet_cache[body.get_name()][genus] = (
            False,
            (
                '{}{}'.format(
                    bio_types[genus][sorted_species[0][0]][0],
                    f' - {sorted_species[0][1]}' if sorted_species[0][1] else ''
                ),
                bio_types[genus][sorted_species[0][0]][1], bio_types[genus][sorted_species[0][0]][1], []
            )
        )
    elif len(sorted_species) > 0:
        color = ''
        localized_species = [
            (bio_types[genus][info[0]][0], info[1], bio_types[genus][info[0]][1]) for info in sorted_species
        ]
        if sorted_species[0][1] == sorted_species[-1][1]:
            color = sorted_species[0][1]
        this.planet_cache[body.get_name()][genus] = (
            False,
            (
                '{}{}'.format(bio_genus[genus]['name'], f' - {color}' if color else ''),
                bio_types[genus][sorted_species[0][0]][1],
                bio_types[genus][sorted_species[-1][0]][1],
                localized_species
            )
        )

    if this.planet_cache[body.get_name()][genus][0]:
        this.planet_cache[body.get_name()][genus] = (False, ('', 0, 0, []))

    return this.planet_cache[body.get_name()][genus][1]


def reset_cache(planet: str = '') -> None:
    """
    Resets the species calculation cache. If genus is passed, resets only that genus.

    :param planet: Optional parameter to reset only a specific genus
    """
    if planet and planet in this.planet_cache:
        for genus in this.planet_cache[planet]:
            this.planet_cache[planet][genus] = (True, this.planet_cache[planet][genus][1])
    else:
        for planet, data in this.planet_cache.items():
            for genus in data:
                data[genus] = (True, data[genus][1])


def get_possible_values(body: PlanetData) -> dict[str, tuple[int, int, list[tuple[str, str, int]]]]:
    """
    For unmapped planets, run through every genus and make species determinations

    :param body: The planet we're fetching
    :return: A dictionary of genera mapped to the minimum and maximum values and a list of species if there
             were multiple matches
    """

    possible_genus = {}
    for genus, species_reqs in bio_types.items():
        name, min_potential_value, max_potential_value, all_species = value_estimate(body, genus)
        if min_potential_value != 0:
            possible_genus[name] = (min_potential_value, max_potential_value, all_species)

    return dict(sorted(possible_genus.items(), key=lambda gen_v: gen_v[0]))


def get_body_name(fullname: str = '') -> str:
    """
    Remove the base system name from the body name if the body has a unique identifier.
    Usually only the main star has the same name as the system in one-star systems.

    :param fullname: The full name of the body including the system name
    :return: The short name of the body unless it matches the system name
    """

    if fullname.startswith(this.starsystem + ' '):
        body_name = fullname[len(this.starsystem + ' '):]
    else:
        body_name = fullname
    return body_name


def reset() -> None:
    """
    Reset system data when location changes
    """

    this.starsystem = ''
    this.main_star_type = ''
    this.main_star_luminosity = ''
    this.location_name = ''
    this.location_id = -1
    this.location_state = ''
    this.fetched_edsm = False
    this.planets = {}
    this.planet_cache = {}
    this.stars = {}
    this.barycenters = {}
    this.scroll_canvas.yview_moveto(0.0)


def journal_entry(
        cmdr: str, is_beta: bool, system: str, station: str, entry: Mapping[str, any], state: MutableMapping[str, any]
) -> str:
    """ EDMC journal entry hook. Primary journal data handler. """

    system_changed = False
    # this.game_version = semantic_version.Version.coerce(state.get('GameVersion', '0.0.0'))
    # this.odyssey = state.get('Odyssey', False)
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
                this.main_star_type = entry['StarType']
                this.main_star_luminosity = entry['Luminosity']

            if entry['BodyID'] not in this.stars:
                star_data = StarData(body_short_name, entry['BodyID'])
            else:
                star_data = this.stars[entry['BodyID']]

            star_data.set_type(entry['StarType'])
            star_data.set_luminosity(entry['Luminosity'])

            this.stars[entry['BodyID']] = star_data

            if 'Parents' in entry:
                if 'Null' in entry['Parents'][0] and entry['Parents'][0]['Null'] in this.barycenters:
                    this.barycenters[entry['Parents'][0]['Null']].append(entry['BodyID'])

            reset_cache()
            update_display()

        if 'PlanetClass' in entry:
            if body_short_name not in this.planets:
                body_data = PlanetData(body_short_name)
            else:
                body_data = this.planets[body_short_name]
            body_data.set_distance(float(entry['DistanceFromArrivalLS'])).set_type(entry['PlanetClass']) \
                .set_id(entry['BodyID']).set_gravity(entry['SurfaceGravity']) \
                .set_temp(entry['SurfaceTemperature']).set_volcanism(entry['Volcanism'])

            for body in entry['Parents']:
                if 'Null' in body:
                    if body['Null'] in this.barycenters:
                        barycenter_stars: list[StarData] = []
                        for star in this.barycenters[body['Null']]:
                            barycenter_stars.append(this.stars[star])
                        sorted_stars = sorted(barycenter_stars, key=lambda item: item.get_id())
                        if len(sorted_stars):
                            body_data.set_parent_star(sorted_stars[0].get_id())
                            break
                elif 'Star' in body:
                    body_data.set_parent_star(body['Star'])
                    break

            if 'Materials' in entry:
                for material in entry['Materials']:
                    body_data.add_material(material['Name'])

            if 'AtmosphereType' in entry:
                body_data.set_atmosphere(entry['AtmosphereType'])

            this.planets[body_short_name] = body_data

            reset_cache()
            update_display()

    elif entry['event'] == 'ScanBaryCentre':
        this.barycenters[entry['BodyID']] = []

    elif entry['event'] == 'FSSBodySignals':
        body_short_name = get_body_name(entry['BodyName'])
        if body_short_name not in this.planets:
            this.planets[body_short_name] = PlanetData(body_short_name)
        for signal in entry['Signals']:
            if signal['Type'] == '$SAA_SignalType_Biological;':
                this.planets[body_short_name].set_bio_signals(signal['Count'])

        reset_cache(body_short_name)
        update_display()

    elif entry['event'] == 'SAASignalsFound':
        body_short_name = get_body_name(entry['BodyName'])

        if body_short_name not in this.planets:
            body_data = PlanetData(body_short_name).set_id(entry['BodyID'])
        else:
            body_data = this.planets[body_short_name].set_id(entry['BodyID'])

        # Add bio signal number just in case
        for signal in entry['Signals']:
            if signal['Type'] == '$SAA_SignalType_Biological;':
                body_data.set_bio_signals(signal['Count'])

        # If signals include genuses, add them to the body data
        if 'Genuses' in entry:
            for genus in entry['Genuses']:
                if body_data.get_flora(genus['Genus']) is None:
                    body_data.add_flora(genus['Genus'])
        this.planets[body_short_name] = body_data

        reset_cache(body_short_name)
        update_display()

    elif entry['event'] == 'ScanOrganic':
        target_body = None
        for name, body in this.planets.items():
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
            this.planets[target_body].set_flora_species_scan(entry['Genus'], entry['Species'], scan_level)
            if this.current_scan != '' and this.current_scan != entry['Genus']:
                species = this.planets[target_body].get_flora(this.current_scan)[0]
                this.planets[target_body].set_flora_species_scan(this.current_scan, species, 0)
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
        for name, body in this.planets.items():
            if body.get_id() == entry['BodyID']:
                target_body = name
                break

        if target_body is not None:
            genus, species, color = get_species_from_codex(entry['Name'])
            if genus is not '' and species is not '':
                this.planets[target_body].add_flora(genus, species, color)

        update_display()

    elif entry['event'] in ['ApproachBody', 'Touchdown', 'Liftoff']:
        if entry['event'] in ['Liftoff', 'Touchdown'] and entry['PlayerControlled'] is False:
            return ''
        body_name = get_body_name(entry['Body'])
        if body_name in this.planets:
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

    if 'BodyName' in entry:
        body_name = get_body_name(entry['BodyName'])
        if this.location_name == '' and body_name != this.starsystem:
            this.location_name = body_name
        if this.location_id == -1 and body_name in this.planets:
            this.location_id = this.planets[body_name].get_id()

    status = StatusFlags(entry['Flags'])
    status2 = StatusFlags2(0)
    if 'Flags2' in entry:
        status2 = StatusFlags2(entry['Flags2'])
    refresh = False
    scroll = False

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
        if (this.focus_setting.get() == 'On Approach' and this.location_state == 'approach') or \
                (this.focus_setting.get() == 'On Surface' and this.location_state == 'surface') or \
                (this.focus_setting.get() != 'Never' and this.location_state == ''):
            scroll = True
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
    if scroll:
        this.scroll_canvas.yview_moveto(0.0)

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


def get_bodies_summary(bodies: dict[str, PlanetData], focused: bool = False) -> tuple[str, int]:
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
                    detail_text += '{}{} ({}): {}{}\n'.format(
                        bio_types[genus][data[0]][0],
                        f' - {data[2]}' if data[2] else '',
                        scan_label(data[1]),
                        this.formatter.format_credits(bio_types[genus][data[0]][1]),
                        u' 🗸' if data[1] == 3 else ''
                    )
                else:
                    bio_name, min_val, max_val, all_species = value_estimate(body, genus)
                    detail_text += '{} (Not located): {}\n'.format(
                        bio_name,
                        this.formatter.format_credit_range(min_val, max_val))
                    if this.focus_breakdown.get():
                        for species in all_species:
                            detail_text += '  {}{}: {}\n'.format(
                                species[0],
                                f' - {species[1]}' if species[1] else '',
                                this.formatter.format_credits(species[2])
                            )
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
                if this.focus_breakdown.get():
                    for species in values[2]:
                        detail_text += '  {}{}: {}\n'.format(
                            species[0],
                            f' - {species[1]}' if species[1] else '',
                            this.formatter.format_credits(species[2])
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
        this.edsm_failed.grid_remove()

    bio_bodies = dict(sorted(dict(filter(lambda fitem: fitem[1].get_bio_signals() > 0 or len(fitem[1].get_flora()) > 0, this.planets.items())).items(),
                             key=lambda item: item[1].get_id()))
    exobio_body_names = [
        '%s%s: %d' % (body_name, get_body_shorthand(body_data.get_type()), body_data.get_bio_signals())
        for body_name, body_data
        in bio_bodies.items()
    ]

    if (this.location_name != '' and this.location_name in bio_bodies) and this.focus_setting.get() != 'Never' and \
            ((this.focus_setting.get() == 'On Approach' and this.location_state in ['approach', 'surface'])
             or (this.focus_setting.get() == 'On Surface' and this.location_state == 'surface')):
        detail_text, total_value = get_bodies_summary({this.location_name: this.planets[this.location_name]}, True)
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
            for genus, data in this.planets[this.location_name].get_flora().items():
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
