# -*- coding: utf-8 -*-
import locale
import math
# BioScan plugin for EDMC
# Source: https://github.com/Silarn/EDMC-BioScan
# Licensed under the [GNU Public License (GPL)](http://www.gnu.org/licenses/gpl-2.0.html) version 2 or later.

import sys
import tkinter as tk
from tkinter import ttk
import semantic_version

import myNotebook as nb
from bio_scan.nebula_coordinates import nebula_coords
from bio_scan.nebulae_data import planetary_nebulae, nebula_sectors
from ttkHyperlinkLabel import HyperlinkLabel
from config import config
from theme import theme

from RegionMap import findRegion
from EDMCLogging import get_main_logger

from bio_scan.body_data import BodyData, get_body_shorthand, body_check
from bio_scan.bio_data import bio_genus, bio_types, get_species_from_codex, region_map
from bio_scan.format_util import Formatter

logger = get_main_logger()

VERSION = '0.7-beta'

this = sys.modules[__name__]  # For holding module globals
this.formatter = Formatter()
this.focus_setting = None
this.signal_setting = None
this.debug_logging_enabled = None

this.frame = None
this.scroll_canvas = None
this.scrollbar = None
this.scrollable_frame = None
this.label = None
this.values_label = None
this.total_label = None
this.bodies = {}  # type: dict[str, BodyData]
this.odyssey = False
this.game_version = semantic_version.Version.coerce('0.0.0.0')
this.shorten_values = None
this.main_star_id = None
this.main_star_type = ''
this.coordinates = [0.0, 0.0, 0.0]
this.location_name = ''
this.location_id = ''
this.location_state = ''
this.body_location = 0
this.starsystem = ''


def plugin_start3(plugin_dir):
    return plugin_start()


def plugin_start():
    # App isn't initialised at this point so can't do anything interesting
    return 'BioScan'


def plugin_app(parent: tk.Frame) -> tk.Frame:
    parse_config()
    this.frame = tk.Frame(parent)
    this.label = tk.Label(this.frame)
    this.label.grid(row=0, column=0, columnspan=2, sticky=tk.N)
    this.scroll_canvas = tk.Canvas(this.frame, height=80, highlightthickness=0)
    this.scrollbar = ttk.Scrollbar(this.frame, orient="vertical", command=this.scroll_canvas.yview)
    this.scrollable_frame = ttk.Frame(this.scroll_canvas)
    this.scrollable_frame.bind(
        "<Configure>",
        lambda e: this.scroll_canvas.configure(
            scrollregion=this.scroll_canvas.bbox("all")
        )
    )
    this.scroll_canvas.bind("<Enter>", bind_mousewheel)
    this.scroll_canvas.bind("<Leave>", unbind_mousewheel)
    this.scroll_canvas.create_window((0, 0), window=this.scrollable_frame, anchor="nw")
    this.scroll_canvas.configure(yscrollcommand=this.scrollbar.set)
    this.values_label = ttk.Label(this.scrollable_frame)
    this.values_label.pack(fill="both", side="left")
    this.scroll_canvas.grid(row=1, column=0, sticky=tk.EW)
    this.scroll_canvas.grid_rowconfigure(1, weight=0)
    this.frame.grid_columnconfigure(0, weight=1)
    this.scrollbar.grid(row=1, column=1, sticky=tk.NSEW)
    this.total_label = tk.Label(this.frame)
    this.total_label.grid(row=2, column=0, columnspan=2, sticky=tk.N)
    update_display()
    theme.register(this.values_label)
    return this.frame


def plugin_prefs(parent: ttk.Notebook, cmdr: str, is_beta: bool) -> tk.Frame:
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
    nb.Label(frame, text = 'Version %s' % VERSION).grid(row=1, column=1, padx=x_padding, sticky=tk.E)

    ttk.Separator(frame).grid(row=5, columnspan=2, pady=y_padding*2, sticky=tk.EW)

    nb.Label(
        frame,
        text="Focus Body Signals:",
    ).grid(row=10, padx=x_padding, sticky=tk.W)
    focus_options = [
        "Never",
        "On Approach",
        "On Surface",
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
        text="Display Signal Summary:"
    ).grid(row=10, column=1, sticky=tk.W)
    signal_options = [
        "Always",
        "In Flight",
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
    config.set('bioscan_focus', this.focus_setting.get())
    config.set('bioscan_signal', this.signal_setting.get())
    config.set('bioscan_debugging', this.debug_logging_enabled.get())
    update_display()


def parse_config() -> None:
    this.focus_setting = tk.StringVar(value=config.get_str(key='bioscan_focus', default="On Approach"))
    this.signal_setting = tk.StringVar(value=config.get_str(key='bioscan_signal', default="Always"))
    this.debug_logging_enabled = tk.BooleanVar(value=config.get_bool(key='bioscan_debugging', default=False))


def log(*args):
    if this.debug_logging_enabled.get():
        logger.debug(args)


def scan_label(scans: int):
    match scans:
        case 0:
            return "Located"
        case 1:
            return "Logged"
        case 2:
            return "Sampled"
        case 3:
            return "Analysed"


def value_estimate(body: BodyData, genus: str) -> tuple[int, int]:
    possible_species = set()
    eliminated_species = set()
    log(genus)
    for species, reqs in bio_types[genus].items():
        possible_species.add(species)
        log(species)
        if reqs[2] is not None:
            if reqs[2] == "Any" and body.get_atmosphere() in ["", "None"]:
                log("Eliminated for no atmos")
                eliminated_species.add(species)
            elif body.get_atmosphere() not in reqs[2]:
                log("Eliminated for atmos")
                eliminated_species.add(species)
        if reqs[3] is not None:
            if body.get_gravity() / 9.80665 > reqs[3]:
                log("Eliminated for grav")
                eliminated_species.add(species)
        if reqs[4] is not None:
            if body.get_temp() > reqs[4]:
                log("Eliminated for high heat")
                eliminated_species.add(species)
        if reqs[5] is not None:
            if body.get_temp() < reqs[5]:
                log("Eliminated for low heat")
                eliminated_species.add(species)
        if reqs[6] is not None:
            if reqs[6] == "Any" and body.get_volcanism() == "":
                log("Eliminated for no volcanism")
                eliminated_species.add(species)
            else:
                found = False
                for volc_type in reqs[6]:
                    if body.get_volcanism().find(volc_type) != -1:
                        found = True
                if not found:
                    log("Eliminated for volcanism")
                    eliminated_species.add(species)
        if reqs[7] is not None:
            if body.get_type() not in reqs[7]:
                log("Eliminated for body type")
                eliminated_species.add(species)
        if reqs[8] is not None:
            if this.coordinates is not None:
                found = None
                for region in reqs[8]:
                    region_id = findRegion(*this.coordinates)
                    if region_id is not None:
                        log("Current region: {} - {}".format(region_id[0], region_id[1]))
                        if region.startswith("!"):
                            if region_id[0] in region_map[region[1:]]:
                                log("Eliminated by region")
                                eliminated_species.add(species)
                        else:
                            found = False if found is None else found
                            if region_id[0] in region_map[region]:
                                found = True
                if not found and found is not None:
                    log("Eliminated by region")
                    eliminated_species.add(species)
        if reqs[9] is not None:
            match reqs[9]:
                case '2500ls':
                    if body.get_distance() < 2500.0:
                        eliminated_species.add(species)
                case 'A':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type[0] != 'A':
                            log("Eliminated for star type")
                            eliminated_species.add(species)
                    if not body_check(this.bodies):
                        log("Eliminated for missing body type(s)")
                        eliminated_species.add(species)
                case 'AV':
                    if len(this.main_star_type) > 0:
                        if not this.main_star_type.startswith('A') and not this.main_star_type.startswith('N'):
                            log("Eliminated for star type")
                            eliminated_species.add(species)
                        elif this.main_star_type.startswith('AVI'):
                            log("Eliminated for star type")
                            eliminated_species.add(species)
                case 'OBA':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type[0] not in ['O', 'B', 'A']:
                            log("Eliminated for star type")
                            eliminated_species.add(species)
                case 'AFGKMS':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type[0] not in ['A', 'F', 'G', 'K', 'M', 'S']:
                            log("Eliminated for star type")
                            eliminated_species.add(species)
                        if body.get_distance() < 12000.0:
                            log("Eliminated for distance")
                            eliminated_species.add(species)
                        if not body_check(this.bodies):
                            log("Eliminated for missing body type(s)")
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
                        log("Distance to {0} from {1}: {2:n} ly".format(system, this.starsystem, distance))
                        if distance < 100.0:
                            found = True
                            break
                    if not found:
                        log("Eliminated for lack of nebula")
                        eliminated_species.add(species)
                case 'special':
                    log("Eliminated due to unhandled special rules")
                    eliminated_species.add(species)  # ignore old flora with special rules for now

    final_species = possible_species - eliminated_species
    sorted_species = sorted(final_species, key=lambda species: bio_types[genus][species][1])

    if len(sorted_species) > 0:
        return bio_types[genus][sorted_species[0]][1], bio_types[genus][sorted_species[-1]][1]
    return 0, 0


def get_possible_values(body: BodyData) -> dict[str, tuple]:
    possible_genus = {}
    for genus, species_reqs in bio_types.items():
        min_potential_value, max_potential_value = value_estimate(body, genus)
        if min_potential_value != 0:
            possible_genus[bio_genus[genus]] = (min_potential_value, max_potential_value)

    return dict(sorted(possible_genus.items(), key=lambda gen_v: gen_v[0]))


def get_bodyname(fullname: str = "") -> str:
    if fullname.startswith(this.starsystem + ' '):
        bodyname = fullname[len(this.starsystem + ' '):]
    else:
        bodyname = fullname
    return bodyname


def journal_entry(
        cmdr: str, is_beta: bool, system: str, station: str, entry: dict[str, any], state: dict[str, any]
) -> str:
    if entry['event'] == 'Fileheader' or entry['event'] == 'LoadGame':
        this.odyssey = entry.get('Odyssey', False)
        this.game_version = semantic_version.Version.coerce(entry.get('gameversion'))

    elif entry['event'] == 'Location':
        this.starsystem = entry['StarSystem']
        this.coordinates = entry['StarPos']

    elif entry['event'] == 'FSDJump':
        if 'StarSystem' in entry:
            this.starsystem = entry['StarSystem']
        this.main_star_id = entry['BodyID'] if 'BodyID' in entry else 0
        this.main_star_type = ""
        this.location_name = ""
        this.location_id = -1
        this.location_state = ""
        this.bodies = {}
        this.coordinates = entry['StarPos']
        update_display()
        this.scroll_canvas.yview_moveto(0.0)

    elif entry['event'] == 'Scan':
        bodyname_insystem = get_bodyname(entry['BodyName'])
        if 'StarType' in entry:
            if entry['BodyID'] == this.main_star_id or entry['BodyID'] == 0:
                this.main_star_type = "{}{}".format(entry['StarType'], entry['Luminosity'])
        if 'PlanetClass' in entry:
            odyssey_bonus = this.odyssey or this.game_version.major >= 4
            if 'StarSystem' in entry:
                this.starsystem = entry['StarSystem']

            if bodyname_insystem not in this.bodies:
                body_data = BodyData(bodyname_insystem)
            else:
                body_data = this.bodies[bodyname_insystem]
            body_data.set_distance(float(entry['DistanceFromArrivalLS'])).set_type(entry['PlanetClass']) \
                .set_id(entry['BodyID']).set_gravity(entry['SurfaceGravity']) \
                .set_temp(entry['SurfaceTemperature']).set_volcanism(entry['Volcanism'])

            if 'AtmosphereType' in entry:
                body_data.set_atmosphere(entry['AtmosphereType'])

            this.bodies[bodyname_insystem] = body_data

            update_display()

    elif entry['event'] == 'FSSBodySignals':
        bodyname_insystem = get_bodyname(entry['BodyName'])
        if bodyname_insystem not in this.bodies:
            this.bodies[bodyname_insystem] = BodyData(bodyname_insystem)
        for signal in entry['Signals']:
            if signal['Type'] == '$SAA_SignalType_Biological;':
                this.bodies[bodyname_insystem].set_bio_signals(signal['Count'])

        update_display()

    elif entry['event'] == 'SAASignalsFound':
        bodyname_insystem = get_bodyname(entry['BodyName'])

        if bodyname_insystem not in this.bodies:
            body_data = BodyData(bodyname_insystem).set_id(entry['BodyID'])
        else:
            body_data = this.bodies[bodyname_insystem].set_id(entry['BodyID'])

        # Add bio signal number just in case
        for signal in entry['Signals']:
            if signal['Type'] == '$SAA_SignalType_Biological;':
                body_data.set_bio_signals(signal['Count'])

        # If signals include genuses, add them to the body data
        if 'Genuses' in entry:
            for genus in entry['Genuses']:
                if body_data.get_flora(genus['Genus']) is None:
                    body_data.add_flora(genus['Genus'])
        this.bodies[bodyname_insystem] = body_data

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

        update_display()

    elif entry['event'] == 'CodexEntry' and \
            entry['BodyID'] == this.location_id and \
            entry['Category'] == "$Codex_Category_Biology;":
        target_body = None
        for name, body in this.bodies.items():
            if body.get_id() == entry['BodyID']:
                target_body = name
                break

        if target_body is not None:
            genus, species = get_species_from_codex(entry["Name"])
            this.bodies[target_body].add_flora(genus, species)

        update_display()

    elif entry['event'] in ['ApproachBody', 'Touchdown', 'Liftoff', 'Embark', 'Disembark']:
        body_name = get_bodyname(entry["Body"])
        if body_name in this.bodies:
            this.location_name = body_name
            this.location_id = entry["BodyID"]

        if entry['event'] in ['ApproachBody', 'Liftoff']:
            this.location_state = 'approach'
        else:
            this.location_state = 'surface'

        update_display()
        this.scroll_canvas.yview_moveto(0.0)

    elif entry['event'] == 'LeaveBody':
        this.location_name = ''
        this.location_id = -1
        this.location_state = ''

        update_display()
        this.scroll_canvas.yview_moveto(0.0)

    return ''  # No error


def update_display() -> None:
    detail_text = ""
    bio_bodies = dict(sorted(dict(filter(lambda fitem: fitem[1].get_bio_signals() > 0 or len(fitem[1].get_flora()) > 0, this.bodies.items())).items(),
                        key=lambda item: item[1].get_id()))
    exobio_body_names = [
        '%s%s: %d' % (body_name, get_body_shorthand(body_data.get_type()), body_data.get_bio_signals())
        for body_name, body_data
        in bio_bodies.items()
    ]

    total_value = 0
    if (this.location_name != "" and this.location_name in bio_bodies) and this.focus_setting.get() != "Never" and \
            ((this.focus_setting.get() == 'On Approach' and this.location_state in ['approach', 'surface'])
             or (this.focus_setting.get() == 'On Surface' and this.location_state == 'surface')):
        count = 0
        for genus, data in bio_bodies[this.location_name].get_flora().items():
            count += 1
            if data[1] == 3:
                total_value += bio_types[genus][data[0]][1]
            if data[0] != "":
                detail_text += "{} ({}): {}{}\n".format(bio_types[genus][data[0]][0],
                                                        scan_label(data[1]),
                                                        this.formatter.format_credits(bio_types[genus][data[0]][1]),
                                                        u' 🗸' if data[1] == 3 else '')
            else:
                min_val, max_val = value_estimate(bio_bodies[this.location_name], genus)
                detail_text += "{} (Not located): {}\n".format(bio_genus[genus],
                                                             this.formatter.format_credit_range(min_val, max_val))
            if len(bio_bodies[this.location_name].get_flora()) == count:
                detail_text += "\n"

    else:
        for name, body in bio_bodies.items():
            detail_text += "{}:\n".format(name)
            if len(body.get_flora()) > 0:
                count = 0
                for genus, data in body.get_flora().items():
                    count += 1
                    if data[1] == 3:
                        total_value += bio_types[genus][data[0]][1]
                    if data[0] != "":
                        detail_text += "{} ({}): {}{}\n".format(bio_types[genus][data[0]][0],
                                                                scan_label(data[1]),
                                                                this.formatter.format_credits(bio_types[genus][data[0]][1]),
                                                                u' 🗸' if data[1] == 3 else '')
                    else:
                        min_val, max_val = value_estimate(body, genus)
                        detail_text += "{} (Not located): {}\n".format(bio_genus[genus],
                                                                     this.formatter.format_credit_range(min_val, max_val))
                    if len(body.get_flora()) == count:
                        detail_text += "\n"

            else:
                types = get_possible_values(body)
                detail_text += "{} Signals - Possible Types:\n".format(body.get_bio_signals())
                count = 0
                for genus, values in types.items():
                    count += 1
                    detail_text += "{}: {}\n".format(genus,
                                                   this.formatter.format_credit_range(values[0], values[1]))
                    if len(types) == count:
                        detail_text += "\n"

    if len(bio_bodies) > 0:
        this.scroll_canvas.grid()
        this.scrollbar.grid()
        this.total_label.grid()
        text = 'BioScan Estimates:\n'

        if this.signal_setting.get() == "Always" or this.location_state != "surface":
            while True:
                exo_list = exobio_body_names[:5]
                exobio_body_names = exobio_body_names[5:]
                text += ' ⬦ '.join([b for b in exo_list])
                if len(exobio_body_names) == 0:
                    break
                else:
                    text += '\n'

        if (this.location_name != "" and this.location_name in bio_bodies) and this.focus_setting.get() != "Never" and \
                ((this.focus_setting.get() == 'On Approach' and this.location_state in ['approach', 'surface'])
                 or (this.focus_setting.get() == 'On Surface' and this.location_state == 'surface')):
            if text[-1] != '\n':
                text += '\n'
            complete = len(dict(filter(lambda x: x[1][1] == 3 , bio_bodies[this.location_name].get_flora().items())))
            text += '{} - {} - {}/{} Analysed'.format(bio_bodies[this.location_name].get_name(),
                                                      bio_bodies[this.location_name].get_type(),
                                                      complete, len(bio_bodies[this.location_name].get_flora()))

        this.total_label['text'] = "Analysed System Samples:\n{} | FF: {}".format(
            this.formatter.format_credits(total_value),
            this.formatter.format_credits((total_value * 5)))
    else:
        this.scroll_canvas.grid_remove()
        this.scrollbar.grid_remove()
        this.total_label.grid_remove()
        text = 'BioScan: No Signals Found'
        this.total_label['text'] = ""

    this.label['text'] = text
    this.values_label['text'] = detail_text

    # if this.show_details.get():
    #     this.scroll_canvas.grid()
    #     this.scrollbar.grid()
    # else:
    #     this.scroll_canvas.grid_remove()
    #     this.scrollbar.grid_remove()


def bind_mousewheel(event: tk.Event) -> None:
    if sys.platform in ("linux", "cygwin", "msys"):
        this.scroll_canvas.bind_all('<Button-4>', on_mousewheel)
        this.scroll_canvas.bind_all('<Button-5>', on_mousewheel)
    else:
        this.scroll_canvas.bind_all('<MouseWheel>', on_mousewheel)


def unbind_mousewheel(event: tk.Event) -> None:
    if sys.platform in ("linux", "cygwin", "msys"):
        this.scroll_canvas.unbind_all('<Button-4>')
        this.scroll_canvas.unbind_all('<Button-5>')
    else:
        this.scroll_canvas.unbind_all('<MouseWheel>')


def on_mousewheel(event: tk.Event) -> None:
    shift = (event.state & 0x1) != 0
    scroll = 0
    if event.num == 4 or event.delta == 120:
        scroll = -1
    if event.num == 5 or event.delta == -120:
        scroll = 1
    if shift:
        this.scroll_canvas.xview_scroll(scroll, "units")
    else:
        this.scroll_canvas.yview_scroll(scroll, "units")
