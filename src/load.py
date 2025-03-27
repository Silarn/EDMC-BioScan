# -*- coding: utf-8 -*-
# BioScan plugin for EDMC
# Source: https://github.com/Silarn/EDMC-BioScan
# Licensed under the [GNU Public License (GPL)](http://www.gnu.org/licenses/gpl-2.0.html) version 2 or later.

# Core imports
from copy import deepcopy
from typing import Mapping, MutableMapping
import os
import sys
import re
import requests
import semantic_version
import math

# TKinter imports
import tkinter as tk
from tkinter import colorchooser as tkColorChooser  # type: ignore # noqa: N812
from tkinter import ttk

# Local imports
import bio_scan.const
from bio_scan.globals import bioscan_globals as this
from bio_scan.nebula_data.reference_stars import get_nearest_nebula
from bio_scan.nebula_data.sectors import data as nebula_sectors
from bio_scan.settings import get_settings, ship_in_whitelist, ship_sold, change_ship_name, add_ship_id, sync_ship_name
from bio_scan.status_flags import StatusFlags2, StatusFlags
from bio_scan.util import system_distance, translate_colors, translate_body, translate_genus, translate_species
from bio_scan.body_data.util import get_body_shorthand, body_check, get_gravity_warning, star_check
from bio_scan.bio_data.codex import check_codex, check_codex_from_name
from bio_scan.bio_data.regions import region_map, guardian_nebulae, tuber_zones
from bio_scan.bio_data.species import rules as bio_types

# Database objects
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from ExploData.explo_data import db
from ExploData.explo_data.db import Commander, PlanetFlora, FloraScans, Waypoint, System, Metadata
from ExploData.explo_data.body_data.struct import PlanetData, StarData, load_planets, load_stars, get_main_star
from ExploData.explo_data.bio_data.codex import parse_variant
from ExploData.explo_data.bio_data.genus import data as bio_genus
import ExploData.explo_data.journal_parse
from ExploData.explo_data.journal_parse import register_journal_callbacks, register_event_callbacks
import ExploData.explo_data.edsm_parse
from ExploData.explo_data.edsm_parse import register_edsm_callbacks

# EDMC imports
from config import config
from edmc_data import ship_name_map
from monitor import monitor
from theme import theme
from EDMCLogging import get_plugin_logger
from ttkHyperlinkLabel import HyperlinkLabel
from l10n import translations as tr

# 3rd Party
from ExploData.explo_data.RegionMap import findRegion
from ExploData.explo_data.RegionMapData import regions as galaxy_regions

this.translation_context = os.path.dirname(__file__)
logger = get_plugin_logger(this.NAME)


def plugin_start3(plugin_dir: str) -> str:
    """
    EDMC start hook.
    Initializes SQLite database.

    :param plugin_dir: The plugin's directory
    :return: The plugin's canonical name
    """

    this.migration_failed = db.init()
    if not this.migration_failed:
        this.sql_session = Session(db.get_engine())
        db_version: Metadata = this.sql_session.scalar(select(Metadata).where(Metadata.key == 'version'))
        if db_version.value.isdigit() and int(db_version.value) != bio_scan.const.db_version:
            this.db_mismatch = True

        if not this.db_mismatch:
            register_event_callbacks({'Scan', 'FSSBodySignals', 'SAASignalsFound', 'ScanOrganic', 'CodexEntry'},
                                     process_data_event)
    return this.NAME


def plugin_app(parent: tk.Frame) -> tk.Frame:
    """
    EDMC initialization hook.
    Build TKinter display pane and initialize display attributes.

    :param parent: EDMC parent TKinter frame
    :return: Plugin's main TKinter frame
    """

    this.parent = parent
    this.frame = tk.Frame(parent)
    this.frame.grid_columnconfigure(0, weight=1)
    if this.migration_failed:
        # LANG: ExploData DB migration threw an error
        this.label = tk.Label(this.frame, text=tr.tl('BioScan: DB Migration Failed', this.translation_context))
        this.label.grid(row=0, sticky=tk.EW)
        # LANG: Hyperlink text for GitHub issue creation
        this.update_button = HyperlinkLabel(this.frame, text=tr.tl('Please Check or Submit an Issue', this.translation_context),
                                            url='https://github.com/Silarn/EDMC-BioScan/issues')
        this.update_button.grid(row=1, columnspan=2, sticky=tk.N)
    elif this.db_mismatch:
        # LANG: Warning text for mismatched ExploData database version
        this.label = tk.Label(this.frame, text=tr.tl('BioScan: Database Mismatch', this.translation_context))
        this.label.grid(row=0, sticky=tk.EW)
        # LANG: Latest release hyperlink text for database mismatch
        this.update_button = HyperlinkLabel(this.frame, text=tr.tl('BioScan/ExploData Version Mismatch', this.translation_context),
                                            url='https://github.com/Silarn/EDMC-BioScan/releases/latest')
        this.update_button.grid(row=1, columnspan=2, sticky=tk.N)
    else:
        parse_config(monitor.cmdr)
        register_journal_callbacks(this.frame, 'biodata', journal_start, journal_update, journal_end)
        register_edsm_callbacks(this.frame, 'biodata', edsm_start, edsm_end)
        this.label = tk.Label(this.frame)
        this.label.grid(row=0, column=0, columnspan=2, sticky=tk.N)
        this.scroll_canvas = tk.Canvas(this.frame, height=this.box_height.get(), highlightthickness=0)
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
        this.scrollbar.grid(row=1, column=1, sticky=tk.NSEW)
        this.total_label = tk.Label(this.frame)
        this.total_label.grid(row=2, column=0, columnspan=2, sticky=tk.N)
        this.edsm_button = tk.Label(this.frame, text='Fetch EDSM Data', fg='white', cursor='hand2')
        this.edsm_button.grid(row=3, columnspan=2, sticky=tk.EW)
        this.edsm_button.bind('<Button-1>', lambda e: edsm_fetch())
        this.journal_label = tk.Label(this.frame, text='Journal Parsing')
        update_version = version_check()
        if update_version != '':
            text = tr.tl('Version {} is now available', this.translation_context).format(update_version)  # LANG: Version update hyperlink message
            url = f'https://github.com/Silarn/EDMC-BioScan/releases/tag/v{update_version}'
            this.update_button = HyperlinkLabel(this.frame, text=text, url=url)
            this.update_button.grid(row=4, columnspan=2, sticky=tk.N)
        update_display()
        theme.register(this.values_label)
    return this.frame


def plugin_prefs(parent: ttk.Notebook, cmdr: str, is_beta: bool) -> tk.Frame:
    """
    EDMC settings pane hook.
    Build settings display and hook in settings properties.

    :param parent: EDMC parent settings pane TKinter frame
    :param cmdr: Active commander name. Unused.
    :param is_beta: Beta status. Unused.
    :return: Plugin settings tab TKinter frame
    """

    parse_config(cmdr)
    return get_settings(parent)


def prefs_changed(cmdr: str, is_beta: bool) -> None:
    """
    EDMC settings changed hook.
    Save persistent settings values and update display.

    :param cmdr: Commander name. Unused.
    :param is_beta: Beta status. Unused.
    """

    config.set('bioscan_shorten_credits', this.credits_setting.get())
    this.formatter.set_shorten(this.credits_setting.get())
    config.set('bioscan_focus', this.focus_setting.get())
    config.set('bioscan_focus_distance', this.focus_distance.get())
    config.set('bioscan_focus_breakdown', this.focus_breakdown.get())
    config.set('bioscan_scan_display', this.scan_display_mode.get())
    config.set('bioscan_signal', this.signal_setting.get())
    config.set('bioscan_exclude_signals', this.exclude_signals.get())
    config.set('bioscan_minimum_signals', this.minimum_signals.get())
    config.set('bioscan_waypoints', this.waypoints_enabled.get())
    config.set('bioscan_box_height', this.box_height.get())
    this.scroll_canvas.config(height=this.box_height.get())
    config.set('bioscan_debugging', this.debug_logging_enabled.get())
    config.set('bioscan_overlay', this.use_overlay.get())
    config.set('bioscan_overlay_color', this.overlay_color.get())
    config.set('bioscan_overlay_anchor_x', this.overlay_anchor_x.get())
    config.set('bioscan_overlay_anchor_y', this.overlay_anchor_y.get())
    config.set('bioscan_overlay_summary_x', this.overlay_summary_x.get())
    config.set('bioscan_overlay_summary_y', this.overlay_summary_y.get())
    config.set('bioscan_overlay_detail_scroll', this.overlay_detail_scroll.get())
    config.set('bioscan_overlay_detail_length', this.overlay_detail_length.get())
    config.set('bioscan_overlay_detail_delay', str(this.overlay_detail_delay.get()))
    config.set(f'bioscan_ship_whitelist_{cmdr.lower()}', this.ship_whitelist)
    update_display()


def parse_config(cmdr: str = '') -> None:
    """ Load saved settings vars. Set defaults. """

    this.credits_setting = tk.BooleanVar(value=config.get_bool(key='bioscan_shorten_credits', default=False))
    this.formatter.set_shorten(this.credits_setting.get())
    this.focus_setting = tk.StringVar(value=config.get_str(key='bioscan_focus', default='On Approach'))
    this.focus_distance = tk.IntVar(value=config.get_int(key='bioscan_focus_distance', default=5000))
    this.focus_breakdown = tk.BooleanVar(value=config.get_bool(key='bioscan_focus_breakdown', default=False))
    this.scan_display_mode = tk.StringVar(value=config.get_str(key='bioscan_scan_display', default='Check'))
    this.signal_setting = tk.StringVar(value=config.get_str(key='bioscan_signal', default='Always'))
    this.exclude_signals = tk.BooleanVar(value=config.get_bool(key='bioscan_exclude_signals', default=False))
    this.minimum_signals = tk.IntVar(value=config.get_int(key='bioscan_minimum_signals', default=0))
    this.waypoints_enabled = tk.BooleanVar(value=config.get_bool(key='bioscan_waypoints', default=True))
    this.box_height = tk.IntVar(value=config.get_int(key='bioscan_box_height', default=80))
    this.debug_logging_enabled = tk.BooleanVar(value=config.get_bool(key='bioscan_debugging', default=False))
    this.use_overlay = tk.BooleanVar(value=config.get_bool(key='bioscan_overlay', default=False))
    this.overlay_color = tk.StringVar(value=config.get_str(key='bioscan_overlay_color', default='#ffffff'))
    this.overlay_anchor_x = tk.IntVar(value=config.get_int(key='bioscan_overlay_anchor_x', default=0))
    this.overlay_anchor_y = tk.IntVar(value=config.get_int(key='bioscan_overlay_anchor_y', default=0))
    this.overlay_summary_x = tk.IntVar(value=config.get_int(key='bioscan_overlay_summary_x', default=400))
    this.overlay_summary_y = tk.IntVar(value=config.get_int(key='bioscan_overlay_summary_y', default=0))
    this.overlay_detail_scroll = tk.BooleanVar(value=config.get_int(key='bioscan_overlay_detail_scroll', default=True))
    this.overlay_detail_length = tk.IntVar(value=config.get_int(key='bioscan_overlay_detail_length', default=70))
    this.overlay_detail_delay = tk.DoubleVar(
        value=float(config.get_str(key='bioscan_overlay_detail_delay', default=10.0)))
    if cmdr:
        this.ship_whitelist = config.get_list(key=f'bioscan_ship_whitelist_{cmdr.lower()}', default=[])


def version_check() -> str:
    """
    Parse latest GitHub release version

    :return: The latest version string if it's newer than ours
    """

    try:
        req = requests.get(url='https://api.github.com/repos/Silarn/EDMC-BioScan/releases/latest')
        data = req.json()
        if req.status_code != requests.codes.ok:
            raise requests.RequestException
    except (requests.RequestException, requests.JSONDecodeError) as ex:
        logger.error('Failed to parse GitHub release info', exc_info=ex)
        return ''

    version = semantic_version.Version(data['tag_name'][1:])
    if version > this.VERSION:
        return str(version)
    return ''


def plugin_stop() -> None:
    """
    EDMC plugin stop function. Closes open threads and database sessions for clean shutdown.
    """

    if this.overlay.available():
        this.overlay.disconnect()


def journal_start(event: tk.Event) -> None:
    """
    Event handler for the start of journal processing. Adds the progress line to the display.

    :param event: Required to process the event. Unused.
    """

    this.journal_label.grid(row=5, columnspan=2, sticky=tk.EW)
    # LANG: Label for journal parsing progress indicator
    this.journal_label['text'] = tr.tl('Parsing Journals', this.translation_context) + ': 0%'


def journal_update(event: tk.Event) -> None:
    """
    Event handler for journal processing progress updates. Updates the display with the current progress.

    :param event: Required to process the event. Unused.
    """
    finished, total = ExploData.explo_data.journal_parse.get_progress()
    progress = '0%'
    if total > 0:
        progress = f'{finished / total:.1%}'
    progress = progress.rstrip('0').rstrip('.')
    this.journal_label['text'] = tr.tl('Parsing Journals', this.translation_context) + f': {progress} [{finished}/{total}]'


def journal_end(event: tk.Event) -> None:
    """
    Event handler for journal processing completion. Removes the display or reports an error.

    :param event: Required to process the event. Unused.
    """

    if ExploData.explo_data.journal_parse.has_error():
        # LANG: Journal parsing error message (line 1)
        this.journal_label['text'] = (tr.tl('Error During Journal Parse', this.translation_context) + '\n' +
        # LANG: Journal parsing error message (line 2)
                                      tr.tl('Please Submit a Report', this.translation_context))
    else:
        this.journal_label.grid_remove()
        reload_system_data()
        update_display()


def log(*args) -> None:
    """
    Debug logger helper function. Only writes to log if debug logging is enabled for BioScan.
    :param args: Arguments to be passed to the EDMC logger
    """

    if this.debug_logging_enabled.get():
        logger.debug(args)


def edsm_fetch() -> None:
    """ EDSM system data fetch thread initialization """

    ExploData.explo_data.edsm_parse.edsm_fetch(this.system.name)


def edsm_start(event: tk.Event) -> None:
    this.fetched_edsm = True
    update_display()


def edsm_end(event: tk.Event) -> None:
    reload_system_data()
    update_display()


def scan_label(scans: int) -> str:
    """ Return the label for the scan stage """

    match scans:
        case 0:
            return tr.tl('Located', this.translation_context)  # LANG: Located scan level (0/3)
        case 1:
            return tr.tl('Logged', this.translation_context)  # LANG: Logged scan level (1/3)
        case 2:
            return tr.tl('Sampled', this.translation_context)  # LANG: Sampled scan level (2/3)
        case 3:
            return tr.tl('Analysed', this.translation_context)  # LANG: Analysed scan level (3/3)
    return tr.tl('Unknown', this.translation_context)  # LANG: Unknown scan level


def value_estimate(body: PlanetData, genus: str) -> tuple[str, int, int, list[tuple[str, list[str], int]]]:
    """
    Main function to make species determinations from body data.
    Returns the display name and the minimum and maximum values.
    Data is cached, and we check a flag to see if we need to recalculate the species.

    :param body: The planet data we're fetching species for
    :param genus: The genus we're checking for species requirements
    :return: List of tuples containing the display string for the calculated genus/species, the minimum and maximum
     values, and a list of individual species data. The species data is a tuple of the species ID, a list of valid
     variants, and the value of that species.
    """

    # Check the cache. If the refresh flag isn't set, skip the genus.
    if body.get_name() in this.planet_cache:
        if genus in this.planet_cache[body.get_name()] and not this.planet_cache[body.get_name()][genus][0]:
            return this.planet_cache[body.get_name()][genus][1]
    else:
        this.planet_cache[body.get_name()] = {}

    # Initialize the cache entry for this genus.
    if genus not in this.planet_cache[body.get_name()]:
        this.planet_cache[body.get_name()][genus] = (True, ('', 0, 0, []))

    # Main processor for the species rulesets
    possible_species: dict[str, set[str]] = {}
    log(f'System: {this.system.name} - Body: {body.get_name()}')
    log(f'Running checks for {bio_genus[genus]["name"]}:')
    for species, data in bio_types[genus].items():
        log(f'Species: {data["name"]}')
        count = 0
        for ruleset in data['rulesets']:
            count += 1
            log(f'Ruleset {count}')
            eliminated = False
            for rule_type, value in ruleset.items():
                log(f'Processing {rule_type}')
                match rule_type:
                    case 'atmosphere':
                        if value == 'Any' and body.get_atmosphere() in ['', 'None']:
                            log('Eliminated for no atmos')
                            eliminated = True
                        elif value != 'Any' and body.get_atmosphere() not in value:
                            log(f'Eliminated for atmos ({body.get_atmosphere()} in {value})')
                            eliminated = True
                    case 'atmosphere_component':
                        for gas, percent in value.items():
                            if body.get_gas(gas) < percent:
                                log('Eliminated for lack of gas in atmosphere')
                                eliminated = True
                    case 'max_gravity':
                        if body.get_gravity() / 9.797759 > value:
                            log('Eliminated for high grav')
                            eliminated = True
                    case 'min_gravity':
                        if body.get_gravity() / 9.797759 < value:
                            log('Eliminated for low grav')
                            eliminated = True
                    case 'max_temperature':
                        if not body.get_temp():
                            continue
                        if body.get_temp() > value:
                            log('Eliminated for high heat')
                            eliminated = True
                    case 'min_temperature':
                        if not body.get_temp():
                            continue
                        if body.get_temp() < value:
                            log('Eliminated for low heat')
                            eliminated = True
                    case 'min_pressure':
                        if not body.get_pressure():
                            continue
                        if body.get_pressure() / 101231.656250 < value:
                            log('Eliminated for low pressure')
                            eliminated = True
                    case 'max_pressure':
                        if not body.get_pressure():
                            continue
                        if body.get_pressure() / 101231.656250 >= value:
                            log('Eliminated for high pressure')
                            eliminated = True
                    case 'max_orbital_period':
                        if body.get_orbital_period() >= value:
                            log('Eliminated for high orbital period')
                            eliminated = True
                    case 'volcanism':
                        log(f'Compare {value} to {body.get_volcanism()}')
                        if isinstance(value, list):
                            found = False
                            for volc_type in value:  # type: str
                                if volc_type.startswith('='):
                                    if body.get_volcanism() == volc_type[1:]:
                                        found = True
                                        break
                                elif body.get_volcanism().find(volc_type) != -1:
                                    found = True
                                    break
                            if not found:
                                log('Eliminated for missing volcanism')
                                eliminated = True
                        elif value == 'Any' and body.get_volcanism() == '':
                            log('Eliminated for no volcanism')
                            eliminated = True
                        elif value == 'None' and body.get_volcanism() != '':
                            log('Eliminated for having volcanism')
                            eliminated = True
                        elif value.startswith('!'):  # 'not' values assume there must be some volcanism
                            if body.get_volcanism().find(value[1:]) != -1 or body.get_volcanism() == '':
                                log(f'Eliminated for having {value[1:]} volcanism')
                                eliminated = True
                    case 'body_type':
                        if body.get_type() not in value:
                            log('Eliminated for body type')
                            eliminated = True
                    case 'regions':
                        if this.system.region is not None:
                            log(f'Current region: {this.system.region} - {galaxy_regions[this.system.region]}')
                            if this.system.region is not None:
                                for region in value:
                                    if region.startswith('!'):
                                        log(f'Not in region ({region[1:]}) map: {region_map[region[1:]]}')
                                        if this.system.region in region_map[region[1:]]:
                                            log('Eliminated by region')
                                            eliminated = True
                                            break

                                if not eliminated:
                                    found = False
                                    count = 0
                                    for region in value:
                                        if not region.startswith('!'):
                                            count += 1
                                            log(f'In region ({region}): {region_map[region]}')
                                            if this.system.region in region_map[region]:
                                                found = True

                                    if not found and count > 0:
                                        log('Eliminated by region')
                                        eliminated = True

                    case 'guardian':
                        found = not value
                        for zone, info in guardian_nebulae.items():
                            log(f'Checking guardian zone: {zone}')
                            max_distance, coordinates = info
                            distance = system_distance((this.system.x, this.system.y, this.system.z), coordinates)
                            log(f'  Distance: {distance}, Max: {max_distance}')
                            if distance < max_distance:
                                found = True
                                break
                        if not found:
                            log('Eliminated for not being in a guardian zone')
                            eliminated = True
                    case 'tuber':
                        found = False
                        for zone, info in tuber_zones.items():
                            if value == 'Any' or zone in value:
                                distances, coordinates = info
                                min_distance, max_distance = distances
                                log(f'Checking tuber zone: {zone}')
                                distance = system_distance((this.system.x, this.system.y, this.system.z), coordinates)
                                log(f'  Distance: {distance}, Max: {max_distance}')
                                if min_distance <= distance <= max_distance:
                                    found = True
                                    break
                        if not found:
                            log('Eliminated for not being in a tuber zone')
                            eliminated = True
                    case 'bodies':
                        if not body_check(value, this.planets):
                            log('Eliminated for missing body type(s)')
                            eliminated = True
                    case 'main_star':
                        if isinstance(value, list):
                            match = False
                            for star_info in value:
                                if isinstance(star_info, tuple):
                                    if star_check(star_info[0], this.main_star_type):
                                        for flag in ['', 'a', 'b', 'ab', 'z']:
                                            if star_info[1] + flag == this.main_star_luminosity:
                                                match = True
                                                break
                                else:
                                    if star_check(star_info, this.main_star_type):
                                        match = True
                                        break
                            if not match:
                                log('Eliminated for star type')
                                eliminated = True
                        else:
                            if not star_check(value, this.main_star_type):
                                log('Eliminated for star type')
                                eliminated = True
                    case 'parent_star':
                        match = False
                        for star_type in value:
                            if star_check(star_type, this.main_star_type):
                                match = True
                                break
                        for star in body.get_parent_stars():
                            if match:
                                break
                            if star in this.stars:
                                for star_type in value:
                                    if star_check(star_type, this.stars[star].get_type()):
                                        match = True
                                        break
                        if not match:
                            log('Eliminated for star type')
                            eliminated = True
                    case 'star':
                        if isinstance(value, list):
                            match = False
                            for _, star in this.stars.items():
                                for star_info in value:
                                    if isinstance(star_info, tuple):
                                        if star_check(star_info[0], star.get_type()):
                                            log(f'Checking {star_info[0]} {star_info[1]} against {star.get_type()}' +
                                                f' {star.get_luminosity()}')
                                            for flag in ['', 'a', 'b', 'ab', 'z']:
                                                if star_info[1] + flag == star.get_luminosity():
                                                    match = True
                                                    break
                                    else:
                                        log(f'Checking {star_info} against {star.get_type()}')
                                        if star_check(star_info, star.get_type()):
                                            match = True
                                            break
                                if match:
                                    break
                            if not match:
                                log('Eliminated for star type')
                                eliminated = True
                        else:
                            match = False
                            for _, star in this.stars.items():
                                if star_check(value, star.get_type()):
                                    match = True
                                    break
                            if not match:
                                log('Eliminated for star type')
                                eliminated = True
                    case 'nebula':
                        if not this.system.x:
                            log('Missing system coordinates')
                            continue
                        if value not in ['all', 'large']:
                            log('Invalid nebula check type')
                        found = False
                        for sector in nebula_sectors:
                            if this.system.name.startswith(sector):
                                found = True
                        if not found:
                            current_location: tuple[float, float, float] = (this.system.x, this.system.y, this.system.z)
                            all_nebulae = True if value == 'all' else False
                            for system, coordinates in get_nearest_nebula(current_location).items():
                                distance = system_distance(current_location, coordinates)
                                log(f'Distance to {system} from {this.system.name}: {distance:n} ly')
                                if distance < 150.0:
                                    found = True
                                    break
                            if not found and all_nebulae:
                                for system, coordinates in get_nearest_nebula(current_location, 'planetary').items():
                                    distance = system_distance(current_location, coordinates)
                                    log(f'Distance to {system} from {this.system.name}: {distance:n} ly')
                                    if distance < 100.0:
                                        found = True
                                        break
                        if not found:
                            log('Eliminated for lack of nebula')
                            eliminated = True
                    case 'distance':
                        if body.get_distance() < value:
                            eliminated = True
                if eliminated:
                    break
            if not eliminated:
                possible_species[species] = set()

    # For remaining species, run color checks if that genus has color variants
    eliminated_species: set[str] = set()
    if 'colors' in bio_genus[genus]:
        if 'species' in bio_genus[genus]['colors']:
            for species in possible_species:
                if 'star' in bio_genus[genus]['colors']['species'][species]:
                    found = False
                    for star in body.get_parent_stars():
                        if found:
                            break
                        if star in this.stars:
                            for star_type in bio_genus[genus]['colors']['species'][species]['star']:
                                log('Checking star type %s against %s' % (star_type, this.stars[star].get_type()))
                                if star_check(star_type, this.stars[star].get_type()):
                                    possible_species[species].add(
                                        bio_genus[genus]['colors']['species'][species]['star'][star_type])
                                    found = True
                                    break
                    for star_name, star_data in this.stars.items():
                        if star_name in body.get_parent_stars():
                            continue
                        if star_data.get_distance() == 0 or parent_is_H(star_data, body):
                            for star_type in bio_genus[genus]['colors']['species'][species]['star']:
                                log('Checking star type %s against %s' % (star_type, star_data.get_type()))
                                if star_check(star_type, star_data.get_type()):
                                    possible_species[species].add(
                                        bio_genus[genus]['colors']['species'][species]['star'][star_type])
                                    break
                elif 'element' in bio_genus[genus]['colors']['species'][species]:
                    for element in bio_genus[genus]['colors']['species'][species]['element']:
                        if element in body.get_materials():
                            possible_species[species].add(
                                bio_genus[genus]['colors']['species'][species]['element'][element])

                if not possible_species[species]:
                    eliminated_species.add(species)
                    log('Eliminated for lack of color')
        else:
            found_colors: set[str] = set()
            found = False
            for star in body.get_parent_stars():
                if found:
                    break
                if star in this.stars:
                    for star_type in bio_genus[genus]['colors']['star']:
                        log('Checking star type %s against %s' % (star_type, this.stars[star].get_type()))
                        if star_check(star_type, this.stars[star].get_type()):
                            found_colors.add(bio_genus[genus]['colors']['star'][star_type])
                            found = True
                            break
            for star_name, star_data in this.stars.items():
                if star_name in body.get_parent_stars():
                    continue
                if star_data.get_distance() == 0 or parent_is_H(star_data, body):
                    for star_type in bio_genus[genus]['colors']['star']:
                        log('Checking star type %s against %s' % (star_type, star_data.get_type()))
                        if star_check(star_type, star_data.get_type()):
                            found_colors.add(bio_genus[genus]['colors']['star'][star_type])
                            break
            if not found_colors:
                possible_species.clear()
                log('Eliminated genus for lack of color')
            else:
                for species in possible_species:
                    possible_species[species].update(found_colors)

    # Species checks are complete. Sort the results.
    final_species: dict[str, list[str]] = {}
    for species in possible_species:
        if species not in eliminated_species:
            final_species[species] = sorted(possible_species[species])

    sorted_species: list[tuple[str, list[str]]] = sorted(
        final_species.items(),
        key=lambda target_species: bio_types[genus][target_species[0]]['value']
    )

    # Save the results to the cache and return. Missing codex entries are evaluated here.
    if len(sorted_species) == 1:
        localized_species: list[tuple[str, list[str], int]] = []
        codex = False
        if sorted_species[0][1]:
            for color in sorted_species[0][1]:
                if not check_codex(this.commander.id, this.system.region, genus, sorted_species[0][0], color):
                    codex = True
                    break
        else:
            codex = not check_codex(this.commander.id, this.system.region, genus, sorted_species[0][0])
        if len(sorted_species[0][1]) > 1:
            localized_species = [
                (translate_species(bio_types[genus][sorted_species[0][0]]['name']),
                 sorted_species[0][1],
                 bio_types[genus][sorted_species[0][0]]['value'])
            ]
        this.planet_cache[body.get_name()][genus] = (
            False,
            (
                '{}{}{}'.format(
                    '\N{memo} ' if codex else '',
                    translate_species(bio_types[genus][sorted_species[0][0]]['name']),
                    f' - {translate_colors(sorted_species[0][1][0])}' if len(sorted_species[0][1]) == 1 else ''
                ),
                bio_types[genus][sorted_species[0][0]]['value'], bio_types[genus][sorted_species[0][0]]['value'],
                localized_species
            )
        )
    elif len(sorted_species) > 0:
        color = ''
        codex = False
        localized_species = [
            (translate_genus(bio_types[genus][info[0]]['name']), info[1], bio_types[genus][info[0]]['value']) for info in sorted_species
        ]
        for species, colors in sorted_species:
            if not codex:
                if colors:
                    for color in colors:
                        if not check_codex(this.commander.id, this.system.region, genus, species, color):
                            codex = True
                            break
                else:
                    codex = not check_codex(this.commander.id, this.system.region, genus, species)
            if len(colors) > 1:
                color = ''
                break
            if len(colors) == 1:
                if color and colors[0] != color:
                    color = ''
                    break
                if not color:
                    color = colors[0]
        this.planet_cache[body.get_name()][genus] = (
            False,
            (
                '{}{}{}'.format(
                    '\N{memo} ' if codex else '',
                    translate_genus(bio_genus[genus]['name']),
                    f' - {translate_colors(color)}' if color else ''
                ),
                bio_types[genus][sorted_species[0][0]]['value'],
                bio_types[genus][sorted_species[-1][0]]['value'],
                localized_species
            )
        )

    if this.planet_cache[body.get_name()][genus][0]:
        this.planet_cache[body.get_name()][genus] = (False, ('', 0, 0, []))

    return this.planet_cache[body.get_name()][genus][1]


def parent_is_H(star: StarData, body: PlanetData) -> bool:
    """
    Checks for parent stars which are black holes. Bios nearly always base their color on the parent star, but
    when the parent star is a black hole, the orbiting stars can provide color instead.

    :param star: The star to check for a parent black hole
    :param body: The planet data to ensure the star is a valid parent star
    :return: True if the star has a parent black hole and the body is orbiting it
    """

    log(f'Checking for BH parent, star {star.get_name()}, body {body.get_name()}')
    possible = False
    if star.get_name() != this.system.name:
        if body.get_name().startswith(star.get_name() + " "):
            log('Star is parent star')
            log(f'Main star is {get_main_star(this.system, this.sql_session).name}')
            if get_main_star(this.system, this.sql_session).name == this.system.name:
                log('Main star is system star')
                if this.main_star_type == 'H':
                    log('Primary system star IS a black hole!')
                    possible = True
            else:
                log('Multi-star system')
                star_parts = star.get_name().split(' ')
                if len(star_parts[0]) > 1:
                    log('This is a barycenter')
                    for bary_star in star_parts[0]:
                        log(f'Checking {bary_star}...')
                        if bary_star in this.stars and this.stars[bary_star].get_type() == 'H':
                            log(f'{bary_star} IS a black hole!')
                            possible = True
                else:
                    if len(star_parts) == 1:
                        log(f'{star.get_name()} is a parent star...')
                        if star.get_type() == 'H':
                            log('IS a black hole!')
                            possible = True
                    else:
                        log(f'{star.get_name()} is a sub star...')
                        if star_parts[0] in this.stars and this.stars[star_parts[0]].get_type() == 'H':
                            log(f'{star_parts[0]} IS a black hole!')
                            possible = True


    if possible and body.get_name().startswith(star.get_name()):
        return True
    return False


def reset_cache(planet: str = '') -> None:
    """
    Resets the species calculation cache. If planet is passed, resets only that planet.

    :param planet: Optional parameter to reset only a specific planet
    """

    if planet and planet in this.planet_cache:
        for genus in this.planet_cache[planet]:
            this.planet_cache[planet][genus] = (True, this.planet_cache[planet][genus][1])
    else:
        for planet, data in this.planet_cache.items():
            for genus in data:
                data[genus] = (True, data[genus][1])


def get_possible_values(body: PlanetData) -> list[tuple[str, tuple[int, int, list[tuple[str, list[str], int]]]]]:
    """
    For unmapped planets, run through every genus and make species determinations

    :param body: The planet we're fetching
    :return: A dictionary of genera mapped to the minimum and maximum values and a list of species if there
             were multiple matches
    """

    possible_genus: list[tuple[str, tuple[int, int, list]]] = []
    for genus in sorted(bio_types, key=lambda item: translate_genus(bio_genus[item]['name'])):
        name, min_potential_value, max_potential_value, all_species = value_estimate(body, genus)
        if min_potential_value != 0:
            possible_genus.append((name, (min_potential_value, max_potential_value, all_species)))

    return possible_genus


def get_body_name(fullname: str = '') -> str:
    """
    Remove the base system name from the body name if the body has a unique identifier.
    Usually only the main star has the same name as the system in one-star systems.

    :param fullname: The full name of the body including the system name
    :return: The short name of the body unless it matches the system name
    """

    if fullname.startswith(this.system.name + ' '):
        body_name = fullname[len(this.system.name + ' '):]
    else:
        body_name = fullname
    return body_name


def reset() -> None:
    """
    Reset system data, typically when the location changes
    """

    this.main_star_type = ''
    this.main_star_luminosity = ''
    this.location_name = ''
    this.location_id = -1
    this.location_state = ''
    this.fetched_edsm = False
    this.planets = {}
    this.planet_cache = {}
    this.stars = {}
    this.scroll_canvas.yview_moveto(0.0)
    this.sql_session.commit()


def reload_system_data() -> None:
    this.planets = load_planets(this.system, this.sql_session)
    this.stars = load_stars(this.system, this.sql_session)
    main_star = get_main_star(this.system, this.sql_session)
    if main_star:
        this.main_star_type = main_star.type
        this.main_star_luminosity = main_star.luminosity


def add_star(entry: Mapping[str, any]) -> None:
    """
    Add main star data from journal event

    :param entry: The journal event dict (must be a Scan event with star data)
    """

    body_short_name = get_body_name(entry['BodyName'])

    if body_short_name not in this.stars:
        star_data = StarData.from_journal(this.system, body_short_name, entry['BodyID'], this.sql_session)
    else:
        star_data = this.stars[body_short_name]

    star_data.set_type(entry['StarType'])
    star_data.set_luminosity(entry['Luminosity'])
    star_data.set_distance(entry['DistanceFromArrivalLS'])

    this.stars[body_short_name] = star_data


def journal_entry(
        cmdr: str, is_beta: bool, system: str, station: str, entry: Mapping[str, any], state: MutableMapping[str, any]
) -> str:
    """
    EDMC journal entry hook. Primary journal data handler.
    Update location information. System data is handled by ExploData.

    :param cmdr: The commander name
    :param is_beta: Beta status (unused)
    :param system: The system name
    :param station: The current station name (unused)
    :param entry: The journal entry dictionary object
    :param state: The EDMC state dictionary object
    :return: Result string. Empty means success.
    """

    if this.migration_failed or this.db_mismatch:
        return ''

    system_changed = False
    if not state['StarPos']:
        return ''
    if system and (not this.system or system != this.system.name):
        reset()
        system_changed = True
        this.system = this.sql_session.scalar(select(System).where(System.name == system))
        if not this.system:
            this.system = System(name=system)
            this.sql_session.add(this.system)
            this.system.x = state['StarPos'][0]
            this.system.y = state['StarPos'][1]
            this.system.z = state['StarPos'][2]
            sector = findRegion(this.system.x, this.system.y, this.system.z)
            this.system.region = sector[0] if sector is not None else None
        reload_system_data()

    if state['SuitCurrent'] and state['SuitCurrent']['name'] != this.suit_name:
        this.suit_name = state['SuitCurrent']['name']
        this.mode_changed = True
        update_display()

    if cmdr and (not this.commander or this.commander.name != cmdr):
        stmt = select(Commander).where(Commander.name == cmdr)
        result = this.sql_session.scalars(stmt)
        this.commander = result.first()
        if not this.commander:
            this.commander = Commander(name=cmdr)
            this.sql_session.add(this.commander)
            this.sql_session.commit()
        parse_config(cmdr)

    log(f'Event {entry["event"]}')

    ship_name = monitor.state['ShipName'] if monitor.state['ShipName'] else ship_name_map.get(
                monitor.state['ShipType'], monitor.state['ShipType'])

    match entry['event']:
        case 'Loadout':
            if ship_name in this.ship_whitelist:
                add_ship_id(entry['ShipID'], ship_name)
            else:
                sync_ship_name(entry['ShipID'], ship_name)
            prefs_changed(cmdr, is_beta)

        case 'ApproachBody' | 'Touchdown' | 'Liftoff':
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

        case 'LeaveBody':
            this.location_name = ''
            this.location_id = -1
            this.location_state = ''

            update_display()
            this.scroll_canvas.yview_moveto(0.0)

        case 'SetUserShipName':
            change_ship_name(entry['ShipID'], ship_name)
            prefs_changed(cmdr, is_beta)

        case 'SellShipOnRebuy' | 'ShipyardSell':
            ship_id = entry.get('SellShipID', entry.get('SellShipId', -1))
            if ship_id != -1:
                ship_sold(ship_id)
                prefs_changed(cmdr, is_beta)

        case 'Resurrect':
            if entry['Bankrupt']:
                this.ship_whitelist.clear()
                prefs_changed(cmdr, is_beta)

    if system_changed:
        update_display()

    return ''  # No error


def process_data_event(entry: Mapping[str, any]) -> None:
    this.sql_session.commit()
    match entry['event']:
        case 'Scan':
            body_short_name = get_body_name(entry['BodyName'])
            if 'StarType' in entry:
                if body_short_name in this.stars:
                    this.stars[body_short_name].refresh()
                elif re.match(r'^[A-Z]$', body_short_name) or body_short_name == this.system.name:
                    this.stars[body_short_name] = StarData.from_journal(this.system, body_short_name,
                                                                        entry['BodyID'], this.sql_session)
                if entry['DistanceFromArrivalLS'] == 0.0:
                    this.main_star_type = entry['StarType']
                    this.main_star_luminosity = entry['Luminosity']
                reset_cache()
                update_display()
            if 'PlanetClass' in entry and entry['PlanetClass']:
                if body_short_name in this.planets:
                    this.planets[body_short_name].refresh()
                else:
                    this.planets[body_short_name] = PlanetData.from_journal(this.system, body_short_name,
                                                                            entry['BodyID'], this.sql_session)
                reset_cache()
                update_display()

        case 'FSSBodySignals' | 'SAASignalsFound':
            body_short_name = get_body_name(entry['BodyName'])
            if body_short_name.endswith('Ring') or body_short_name.find('Belt Cluster') != -1:
                return
            if body_short_name in this.planets:
                this.planets[body_short_name].refresh()
            else:
                this.planets[body_short_name] = PlanetData.from_journal(this.system, body_short_name,
                                                                        entry['BodyID'], this.sql_session)
            reset_cache()
            update_display()

        case 'ScanOrganic':
            target_body = None
            if this.edd_replay:
                return
            for name, body in this.planets.items():
                if body.get_id() == entry['Body']:
                    target_body = name
                    break

            this.current_scan = (entry['Genus'], entry['Species'])
            scan_level = 0
            match entry['ScanType']:
                case 'Log':
                    scan_level = 1
                case 'Sample':
                    scan_level = 2
                case 'Analyse':
                    scan_level = 3

            if target_body is not None:
                this.planets[target_body].set_flora_species_scan(
                    entry['Genus'], entry['Species'], scan_level, this.commander.id
                )
                if scan_level == 1 and this.current_scan[0]:
                    data: PlanetFlora = this.planets[target_body].get_flora(this.current_scan[0],
                                                                            this.current_scan[1])[0]
                    stmt = delete(Waypoint).where(Waypoint.commander_id == this.commander.id) \
                        .where(Waypoint.type == 'scan').where(Waypoint.flora_id != data.id)
                    this.sql_session.execute(stmt)
                    stmt = update(FloraScans).values({'count': 0}).where(FloraScans.commander_id == this.commander.id) \
                        .where(FloraScans.count < 3).where(FloraScans.flora_id != data.id)
                    this.sql_session.execute(stmt)
                    this.sql_session.commit()

                match scan_level:
                    case 1 | 2:
                        if this.planet_latitude and this.planet_longitude and this.waypoints_enabled.get():
                            this.planets[target_body].add_flora_waypoint(
                                entry['Genus'],
                                entry['Species'],
                                (this.planet_latitude, this.planet_longitude),
                                this.commander.id,
                                scan=True
                            )
                    case _:
                        this.current_scan = ('', '')

            update_display()

        case 'CodexEntry':
            if this.edd_replay:
                return
            if entry['Category'] == '$Codex_Category_Biology;' and 'BodyID' in entry:
                target_body = None
                for name, body in this.planets.items():
                    if body.get_id() == entry['BodyID']:
                        target_body = name
                        break

                if target_body is not None:
                    genus, species, _ = parse_variant(entry['Name'])
                    if genus:
                        if this.location_id == entry['BodyID'] and this.planet_latitude \
                                and this.planet_longitude and this.waypoints_enabled.get():
                            latitude = this.planet_latitude
                            longitude = this.planet_longitude
                            if 'Latitude' in entry:
                                latitude = entry['Latitude']
                                longitude = entry['Longitude']
                            this.planets[target_body].add_flora_waypoint(
                                genus, species, (latitude, longitude), this.commander.id
                            )
                    reset_cache()  # Required to clear found codex marks

                update_display()


def dashboard_entry(cmdr: str, is_beta: bool, entry: dict[str, any]) -> str:
    """
    EDMC dashboard entry hook. Parses updates to the Status.json.
    Used to determine planetary location data. Used by waypoints, organic scans, and display focus.

    :param cmdr: Commander name (unused)
    :param is_beta: Beta status (unused)
    :param entry: Dictionary of status file data
    :return: Result string. Empty means success.
    """

    if this.migration_failed or this.db_mismatch or not this.system:
        return ''

    if 'BodyName' in entry:
        body_name = get_body_name(entry['BodyName'])
        if this.location_name == '' and body_name != this.system.name:
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
        if 'Altitude' in entry:
            if this.focus_setting.get() == 'Near Surface' and \
                    (this.planet_altitude > this.focus_distance.get() > entry['Altitude'] or
                     this.planet_altitude < this.focus_distance.get() < entry['Altitude']):
                scroll = True
                refresh = True
            this.planet_altitude = entry['Altitude']
        else:
            this.planet_altitude = 0
        this.planet_latitude = entry['Latitude']
        this.planet_longitude = entry['Longitude']
        this.planet_radius = entry['PlanetRadius']
        this.planet_heading = entry['Heading'] if 'Heading' in entry else None
        try:
            if this.location_name != '' and (this.current_scan[0]
                                             or this.planets[this.location_name].has_waypoint(this.commander.id)):
                refresh = True
        except KeyError:
            log(f"Current location ({this.location_name}) has no planet data")
    else:
        this.planet_latitude = None
        this.planet_longitude = None
        this.planet_heading = None
        this.planet_altitude = 0 if this.location_state == 'surface' else 10000
        this.planet_radius = 0

    if this.analysis_mode != (StatusFlags.IS_ANALYSIS_MODE in status):
        this.analysis_mode = (StatusFlags.IS_ANALYSIS_MODE in status)
        this.mode_changed = True
        refresh = True

    if StatusFlags2.PLANET_ON_FOOT in status2:
        if (StatusFlags2.SOCIAL_ON_FOOT in status2) or (StatusFlags2.HANGAR_ON_FOOT in status2):
            on_foot = False
        else:
            on_foot = True
    else:
        on_foot = False

    if this.in_supercruise != (StatusFlags.SUPERCRUISE in status):
        this.in_supercruise = (StatusFlags.SUPERCRUISE in status)
        this.mode_changed = True
        refresh = True

    if this.on_foot != on_foot:
        this.on_foot = on_foot
        this.mode_changed = True
        refresh = True

    docked = True if (StatusFlags.DOCKED in status) else False

    if this.docked != docked:
        this.docked = docked
        this.mode_changed = True
        refresh = True

    if refresh:
        update_display()
    if scroll:
        this.scroll_canvas.yview_moveto(0.0)

    return ''


def calc_bearing(lat_long: tuple[float, float]) -> float:
    """
    Get the bearing angle from your current position to the target position using lat/long coordinates.

    :param lat_long: The target lat/long coordinates.
    :return: The bearing angle (from 0-359)
    """

    lat_long2 = (this.planet_latitude, this.planet_longitude)
    phi_1 = math.radians(lat_long2[0])
    phi_2 = math.radians(lat_long[0])
    delta_lambda = math.radians(lat_long[1] - lat_long2[1])
    y = math.sin(delta_lambda) * math.cos(phi_2)
    x = math.cos(phi_1) * math.sin(phi_2) \
        - math.sin(phi_1) * math.cos(phi_2) * math.cos(delta_lambda)
    theta = math.atan2(y, x)
    return (math.degrees(theta) + 360) % 360


def calc_distance(lat_long: tuple[float, float], lat_long2: tuple[float, float] | None = None) -> float:
    """
    Use the haversine formula to get the distance between two points of latitude/longitude.

    :param lat_long: The lat/long coordinates of the first (target) position.
    :param lat_long2: Optional. The lat/long coordinates of the second position. Defaults to the player's position.
    :return: The calculated distance (in meters).
    """

    lat_long2 = lat_long2 if lat_long2 else (this.planet_latitude, this.planet_longitude)
    phi_1 = math.radians(lat_long2[0])
    phi_2 = math.radians(lat_long[0])
    delta_phi = math.radians(lat_long[0] - lat_long2[0])
    delta_lambda = math.radians(lat_long[1] - lat_long2[1])
    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi_1) * math.cos(phi_2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return this.planet_radius * c


def get_distance(lat_long: tuple[float, float] | None = None) -> float | None:
    """
    Get the shortest distance to a scan location for the currently-in-progress species.

    :param lat_long: The lat/long coordinates to consider for the distance. Defaults to the player's location.
    :return: The minimum distance or None if we don't have active scan info.
    """

    distance_list = []
    if this.planet_latitude is not None and this.planet_longitude is not None:
        if this.location_name and this.current_scan[0]:
            waypoints: list[Waypoint] = (this.planets[this.location_name]
                                         .get_flora(this.current_scan[0], this.current_scan[1])[0].waypoints)
            waypoints = list(
                filter(lambda item: item.type == 'scan' and item.commander_id == this.commander.id, waypoints))
            for waypoint in waypoints:
                distance_list.append(calc_distance((waypoint.latitude, waypoint.longitude), lat_long))
            return min(distance_list, default=None)
    return None


def get_nearest(genus: str, waypoints: list[Waypoint]) -> str:
    """
    Check logged waypoints and return the nearest one that's not within a previous sample radius.

    :param genus: The genus ID
    :param waypoints: A list of logged waypoints
    :return: Display string with the distance and bearing to the nearest qualifying waypoint. If none is found, return
             an empty string.
    """

    if this.planet_heading and this.planet_latitude and this.planet_longitude:
        distances: list[tuple[float, float]] = []
        for waypoint in waypoints:
            min_distance = get_distance((waypoint.latitude, waypoint.longitude))
            if min_distance is None or min_distance > bio_genus[genus]['distance']:
                distance = calc_distance((waypoint.latitude, waypoint.longitude))
                bearing = calc_bearing((waypoint.latitude, waypoint.longitude))
                distances.append((distance, bearing))

        if len(distances):
            distance, bearing = sorted(distances, key=lambda item: item[0])[0]
            distance_formatted = this.formatter.format_distance(int(distance), 'm', False)
            bearing_diff = abs(bearing - this.planet_heading) % 360
            bearing_diff = 360 - bearing_diff if bearing_diff > 180 else bearing_diff
            bearing_diff = bearing_diff if (this.planet_heading + bearing_diff) % 360 == bearing else bearing_diff * -1
            return '{}° ({}{}°), {}'.format(int(bearing),
                                            '-> ' if bearing_diff >= 0 else '<- ',
                                            int(abs(bearing_diff)),
                                            distance_formatted)

    return ''


def get_bodies_summary(bodies: dict[str, PlanetData], focused: bool = False) -> tuple[str, int]:
    """
    Get body genus estimate display text for the scroll pane

    :param bodies: Dictionary of planets to display
    :param focused: Whether to return a focused display
    :return: A tuple containing the display text and the final completed scan value of the display
    """

    detail_text = ''
    complete_text = tr.tl('Complete', this.translation_context)  # LANG: Scan complete status text
    value_sum = 0
    for name, body in bodies.items():
        complete = True
        num_complete = 0
        if len(body.get_flora()):
            for flora in body.get_flora():
                scan: list[FloraScans] = list(filter(lambda item: item.commander_id == this.commander.id, flora.scans))
                if not scan or scan[0].count < 3:
                    complete = False
                else:
                    num_complete += 1
        else:
            complete = False
        if not focused:
            if not complete or this.scan_display_mode.get() not in ['Hide', 'Hide in System']:
                if (this.exclude_signals.get() and body.get_bio_signals()
                        and body.get_bio_signals() < this.minimum_signals.get()):
                    detail_text += f'{name} - {body.get_bio_signals()} Signal{"s"[:body.get_bio_signals()^1]}'
                    if len(body.get_flora()) and len(body.get_flora()) == num_complete:
                        detail_text += f' ({complete_text})'
                    detail_text += '\n'
                elif len(body.get_flora()) and num_complete:
                    detail_text += '{} -{}{} ({}/{} {}):\n'.format(
                        name,
                        get_body_shorthand(body.get_type()),
                        get_gravity_warning(body.get_gravity(), True),
                        num_complete,
                        len(body.get_flora()),
                        complete_text
                    )
                elif body.get_scan_state(this.commander.id) in [2, 4] or body.get_bio_signals():
                    detail_text += '{} -{}{}:\n'.format(
                        name,
                        get_body_shorthand(body.get_type()),
                        get_gravity_warning(body.get_gravity(), True)
                    )
            else:
                # LANG: All scans complete status text
                detail_text += f'{name} - ' + tr.tl('All Samples Complete', this.translation_context) + '\n'
        elif complete and this.scan_display_mode.get() == 'Hide':
            detail_text += tr.tl('All Samples Complete', this.translation_context)
        if (this.exclude_signals.get() and body.get_bio_signals()
                and body.get_bio_signals() < this.minimum_signals.get()):
            detail_text += '\n'
        elif len(body.get_flora()) > 0:
            count = 0
            genus_count: dict[str, int] = {}
            for flora in sorted(body.get_flora(), key=lambda item: translate_genus(bio_genus[item.genus]['name'])):
                count += 1
                show = True
                genus: str = flora.genus
                species: str = flora.species
                scan: list[FloraScans] = list(filter(lambda item: item.commander_id == this.commander.id, flora.scans))
                color: str = flora.color
                waypoints: list[Waypoint] = list(
                    filter(
                        lambda item: item.commander_id == this.commander.id and item.type == 'tag',
                        flora.waypoints
                    )
                )
                if scan and scan[0].count == 3:
                    value_sum += bio_types[genus][species]['value']
                    if this.scan_display_mode.get() == 'Hide':
                        show = False
                    elif this.scan_display_mode.get() == 'Hide in System' and not focused:
                        show = False

                if species != '':
                    if bio_genus[genus]['multiple']:
                        genus_count[genus] = genus_count.get(genus, 0) + 1
                        if show and genus_count[genus] == 1:
                            detail_text += (f'{translate_genus(bio_genus[genus]["name"])} - ' +
                                            tr.tl('Multiple Possible', this.translation_context) + ':\n')  # LANG: Indicator for multiple possible bio variants
                    if show:
                        waypoint = get_nearest(genus, waypoints) if (this.waypoints_enabled.get() and focused
                                                                     and not this.current_scan[0] and waypoints) else ''
                        detail_text += '{}{}{}{} ({}): {}{}{}\n'.format(
                            '  ' if bio_genus[genus]['multiple'] else '',
                            '\N{memo} ' if not check_codex(this.commander.id, this.system.region,
                                                           genus, species, color) else '',
                            translate_species(bio_types[genus][species]['name']),
                            f' - {translate_colors(color)}' if color else '',
                            scan_label(scan[0].count if scan else 0),
                            this.formatter.format_credits(bio_types[genus][species]['value']),
                            u' 🗸' if scan and scan[0].count == 3 else '',
                            # LANG: Nearest waypoint text
                            f'\n  ' + tr.tl('Nearest Saved Waypoint', this.translation_context) + f': {waypoint}' if waypoint else ''
                        )
                else:
                    bio_name, min_val, max_val, all_species = value_estimate(body, genus)
                    # LANG: Predicted bio not located label
                    detail_text += (f'{bio_name} (' + tr.tl('Not located', this.translation_context) +
                                    f'): {this.formatter.format_credit_range(min_val, max_val)}\n')

                    if this.focus_breakdown.get():
                        for species_details in all_species:
                            species_details_final = deepcopy(species_details)
                            if species_details_final[1] and len(species_details_final[1]) > 1:
                                for variant in species_details_final[1]:
                                    if not check_codex_from_name(this.commander.id, this.system.region,
                                                                 species_details_final[0], variant):
                                        species_details_final[1][species_details_final[1].index(variant)] = \
                                            f'\N{memo}{translate_colors(variant)}'
                                    else:
                                        species_details_final[1][species_details_final[1].index(variant)] = \
                                            f'{translate_colors(variant)}'
                            else:
                                variant = ''
                                if species_details_final[1]:
                                    variant = species_details_final[1][0]
                                    species_details_final[1][0] = translate_colors(variant)
                                if not check_codex_from_name(this.commander.id, this.system.region,
                                                             species_details_final[0], variant):
                                    species_details_final = (
                                        f'\N{memo}{species_details_final[0]}',
                                        species_details_final[1],
                                        species_details_final[2]
                                    )
                            detail_text += '  {}{}: {}\n'.format(
                                species_details_final[0],
                                ' - {}'.format(', '.join(species_details_final[1])) if species_details_final[1] else '',
                                this.formatter.format_credits(species_details_final[2])
                            )
                if len(body.get_flora()) == count:
                    detail_text += '\n'

        else:
            types = get_possible_values(body)
            if body.get_bio_signals():
                if body.get_scan_state(this.commander.id) == 3:
                    # LANG: Basic scan data messages
                    detail_text += (tr.tl('! Basic Scan Detected !', this.translation_context) + '\n'
                    # LANG: Basic scan data FSS / DSS reminder
                                    + tr.tl('FSS / DSS / AutoScan Needed', this.translation_context) + '\n')

                detail_text += '{} {} - {}:\n'.format(
                    body.get_bio_signals(),
                    tr.tl('Signals', this.translation_context) if body.get_bio_signals() > 1 else tr.tl('Signal', this.translation_context),  # LANG: Body signal display
                    tr.tl('Possible Types', this.translation_context)  # LANG: Possible types label for body signal diplay
                )
                count = 0
                for bio_name, values in types:
                    count += 1
                    detail_text += '{}: {}\n'.format(
                        bio_name,
                        this.formatter.format_credit_range(values[0], values[1])
                    )
                    if this.focus_breakdown.get():
                        for species_details in values[2]:
                            species_details_final = deepcopy(species_details)
                            if species_details_final[1] and len(species_details_final[1]) > 1:
                                for variant in species_details_final[1]:
                                    if not check_codex_from_name(this.commander.id, this.system.region,
                                                                 species_details_final[0], variant):
                                        species_details_final[1][species_details_final[1].index(variant)] = \
                                            f'\N{memo}{translate_colors(variant)}'
                                    else:
                                        species_details_final[1][species_details_final[1].index(variant)] = \
                                            f'{translate_colors(variant)}'
                            else:
                                variant = ''
                                if species_details_final[1]:
                                    variant = species_details_final[1][0]
                                    species_details_final[1][0] = translate_colors(variant)
                                if not check_codex_from_name(this.commander.id, this.system.region,
                                                             species_details_final[0], variant):
                                    species_details_final = (
                                        f'\N{memo}{species_details_final[0]}',
                                        species_details_final[1],
                                        species_details_final[2]
                                    )
                            detail_text += '  {}{}: {}\n'.format(
                                species_details_final[0],
                                ' - {}'.format(', '.join(species_details_final[1])) if species_details_final[1] else '',
                                this.formatter.format_credits(species_details_final[2])
                            )
                    if len(types) == count:
                        detail_text += '\n'
            elif body.get_scan_state(this.commander.id) < 4 and len(types):
                detail_text += (f'{name}:\n' +
                                # LANG: Text for bodies with unknown signals; typically after autoscans
                                tr.tl('AutoScan/NavBeacon Data, Bios Possible', this.translation_context) +
                                '\n' +
                                # LANG: Reminder to trigger FSS / DSS for unknown signals
                                tr.tl('Check FSS for Signals (or DSS)', this.translation_context) + '\n\n')

    return detail_text, value_sum


def update_display() -> None:
    """ Primary display update function. This is run whenever something could change the display state. """

    if this.fetched_edsm or not this.system:
        this.edsm_button.grid_remove()
    else:
        this.edsm_button.grid()

    if not this.commander:
        this.scroll_canvas.grid_remove()
        this.scrollbar.grid_remove()
        this.total_label.grid_remove()
        # LANG: Startup message before data has been processed
        this.label['text'] = tr.tl('BioScan: Awaiting Data', this.translation_context)
        return

    bio_bodies = dict(
        sorted(
            dict(
                filter(
                    lambda item: item[1].get_bio_signals() > 0
                                 or len(item[1].get_flora()) > 0
                                 or (item[1].is_landable() and item[1].get_scan_state(this.commander.id) != 4
                                     and item[1].get_geo_signals() == 0),
                    this.planets.items()
                )
            ).items(),
            key=lambda item: item[1].get_id()
        )
    )
    exobio_body_names = [
        '{}{}{}: {}'.format(
            body_name,
            get_body_shorthand(body_data.get_type()),
            get_gravity_warning(body_data.get_gravity()),
            body_data.get_bio_signals() if body_data.get_bio_signals() > 0 else '?'
        )
        for body_name, body_data
        in filter(lambda item: item[1].get_bio_signals() > 0 or len(item[1].get_flora()) > 0, bio_bodies.items())
    ]

    if display_planetary_data(bio_bodies, True):
        detail_text, total_value = get_bodies_summary({this.location_name: this.planets[this.location_name]}, True)
    else:
        detail_text, total_value = get_bodies_summary(bio_bodies)

    if detail_text != '':
        this.scroll_canvas.grid()
        this.scrollbar.grid()
        this.total_label.grid()
        title = tr.tl('BioScan Predictions', this.translation_context) + ':\n'  # LANG: General BioScan prediction title label
        text = ''
        signal_summary = ''

        if this.signal_setting.get() == 'Always' or this.location_state != 'surface':
            while True:
                exo_list = exobio_body_names[:5]
                exobio_body_names = exobio_body_names[5:]
                signal_summary += ' ⬦ '.join([b for b in exo_list])
                if len(exobio_body_names) == 0:
                    break
                else:
                    signal_summary += '\n'

        if display_planetary_data(bio_bodies):
            if text and text[-1] != '\n':
                text += '\n'
            complete = 0
            floras = bio_bodies[this.location_name].get_flora()
            for flora in floras:
                for scan in filter(lambda item: item.commander_id == this.commander.id,
                                   flora.scans):  # type: FloraScans
                    if scan.count == 3:
                        complete += 1
            text += '{} - {} [{}G] - {}/{} {}'.format(
                bio_bodies[this.location_name].get_name(),
                translate_body(bio_bodies[this.location_name].get_type()),
                '{:.2f}'.format(bio_bodies[this.location_name].get_gravity() / 9.797759).rstrip('0').rstrip('.'),
                # LANG: Bio scans completed indicator label
                complete, len(bio_bodies[this.location_name].get_flora()), tr.tl('Analysed', this.translation_context)
            )
            for flora in this.planets[this.location_name].get_flora():
                genus: str = flora.genus
                species: str = flora.species
                scan_list: list[FloraScans] = list(
                    filter(lambda item: item.commander_id == this.commander.id, flora.scans))
                scan: int = scan_list[0].count if scan_list else 0
                waypoints: list[Waypoint] = list(
                    filter(
                        lambda item: item.commander_id == this.commander.id and item.type == 'tag',
                        flora.waypoints
                    )
                )
                if 0 < scan < 3:
                    if not this.current_scan[0]:
                        this.current_scan = (genus, '')
                    distance = get_distance()
                    distance_format = f'{distance:.2f}' if distance is not None else 'unk'
                    distance = distance if distance is not None else 0
                    waypoint = get_nearest(genus, waypoints) if (waypoints and this.waypoints_enabled.get()) else ''
                    text += '\n{}: {} - {} ({}/3) [{}]{}'.format(
                        tr.tl('In Progress', this.translation_context),  # LANG: Scan in progress indicator
                        translate_genus(bio_types[genus][species]['name']),
                        scan_label(scan),
                        scan,
                        '{}/{}m'.format(
                            distance_format
                            if distance < bio_genus[genus]['distance']
                            else f'> {bio_genus[genus]["distance"]}',
                            bio_genus[genus]['distance']
                        ),
                        '\n' + tr.tl('Nearest Saved Waypoint', this.translation_context) + f': {waypoint}' if waypoint else ''
                    )
                    break

        this.total_label['text'] = '{}:\n{} | FF: {}'.format(
            tr.tl('Analysed System Samples', this.translation_context),  # LANG: Analysed samples list label
            this.formatter.format_credits(total_value),
            this.formatter.format_credits((total_value * 5)))
    else:
        this.scroll_canvas.grid_remove()
        this.scrollbar.grid_remove()
        this.total_label.grid_remove()
        title = tr.tl('BioScan: No Signals Found', this.translation_context)  # LANG: No signals found in current system
        text = ''
        signal_summary = ''
        this.total_label['text'] = ''

    this.label['text'] = title + signal_summary + ('\n' if signal_summary else '') + text
    redraw_overlay = True if this.values_label['text'] != detail_text.strip() else False
    if this.mode_changed:
        redraw_overlay = True
        this.mode_changed = False
    this.values_label['text'] = detail_text.strip()

    if this.use_overlay.get() and this.overlay.available():
        if overlay_should_display():
            if detail_text:
                this.overlay.display("bioscan_title", tr.tl("BioScan Details", this.translation_context),  # LANG: Overlay details label
                                     x=this.overlay_anchor_x.get(), y=this.overlay_anchor_y.get(),
                                     color=this.overlay_color.get())
                if redraw_overlay:
                    this.overlay.display("bioscan_details", detail_text.strip(),
                                         x=this.overlay_anchor_x.get(), y=this.overlay_anchor_y.get() + 20,
                                         color=this.overlay_color.get(), scrolled=this.overlay_detail_scroll.get(),
                                         limit=this.overlay_detail_length.get(), delay=this.overlay_detail_delay.get())
                this.overlay.display("bioscan_summary", text,
                                     x=this.overlay_summary_x.get(), y=this.overlay_summary_y.get(),
                                     size="large", color=this.overlay_color.get())
            else:
                # LANG: Overlay no signals label
                this.overlay.display("bioscan_title", tr.tl("BioScan: No Signals", this.translation_context),
                                     x=this.overlay_anchor_x.get(), y=this.overlay_anchor_y.get(),
                                     color=this.overlay_color.get())
                this.overlay.clear("bioscan_details")
                this.overlay.clear("bioscan_summary")
        else:
            this.overlay.clear("bioscan_title")
            this.overlay.clear("bioscan_details")
            this.overlay.clear("bioscan_summary")


def display_planetary_data(bodies: dict, for_focus: bool = False) -> bool:
    if this.location_name != '' and this.location_name in bodies:
        if this.focus_setting.get() == 'Never':
            if this.location_state in ['approach', 'surface'] and not for_focus:
                return True
        else:
            if this.focus_setting.get() == 'On Approach' and this.location_state in ['approach', 'surface']:
                return True
            if this.focus_setting.get() == 'On Surface':
                if not for_focus and this.location_state == 'approach':
                    return True
                if this.location_state == 'surface':
                    return True
            if this.focus_setting.get() == 'Near Surface' and this.location_state in ['approach', 'surface']:
                if this.planet_altitude <= this.focus_distance.get():
                    return True
    return False


def overlay_should_display() -> bool:
    result = True
    if not this.docked and not this.on_foot:
        ship_name = monitor.state['ShipName'] if monitor.state['ShipName'] else ship_name_map.get(
                monitor.state['ShipType'], monitor.state['ShipType'])
        if this.ship_whitelist and not ship_in_whitelist(monitor.state['ShipID'], ship_name):
            result = False
        if not this.in_supercruise and this.planet_radius == 0:
            result = False
    if this.on_foot:
        if not this.suit_name.startswith('explorationsuit'):
            result = False
    elif this.docked or not this.analysis_mode:
        result = False
    return result


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
