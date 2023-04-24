# -*- coding: utf-8 -*-

# BioScan plugin for EDMC
# Source: https://github.com/Silarn/EDMC-BioScan
# Licensed under the [GNU Public License (GPL)](http://www.gnu.org/licenses/gpl-2.0.html) version 2 or later.

import sys
import tkinter as tk
from tkinter import ttk

from theme import theme
from EDMCLogging import get_main_logger
import semantic_version

from bio_scan.body_data import BodyData
from bio_scan.bio_data import bio_genus, bio_types
from bio_scan.format_util import Formatter

logger = get_main_logger()

VERSION = '0.1'

this = sys.modules[__name__]  # For holding module globals
this.formatter = Formatter()
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
this.body_location = 0
this.starsystem = ''


def plugin_start3(plugin_dir):
    return plugin_start()


def plugin_start():
    # App isn't initialised at this point so can't do anything interesting
    return 'BioScan'


def plugin_app(parent: tk.Frame):
    # parse_config()
    this.frame = tk.Frame(parent)
    this.label = tk.Label(this.frame)
    this.label.grid(row=0, column=0, columnspan=2, sticky=tk.N)
    this.scroll_canvas = tk.Canvas(this.frame, height=60, highlightthickness=0)
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


# def plugin_prefs(parent, cmdr, is_beta):
#
#
# def prefs_changed(cmdr, is_beta):
#     config.set('bioscan_setting', this.setting.get())
#     update_display()
#
#
# def parse_config():
#     this.setting = tk.IntVar(value=config.get_int(key='bioscan_setting', default=400000))


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


def value_estimate(body: BodyData, genus: str):
    possible_species = set()
    eliminated_species = set()
    logger.debug(genus)
    for species, reqs in bio_types[genus].items():
        possible_species.add(species)
        logger.debug(species)
        if reqs[2] is not None:
            if body.get_atmosphere() not in reqs[2]:
                logger.debug("Eliminated for atmos")
                eliminated_species.add(species)
        if reqs[3] is not None:
            if body.get_gravity() / 9.80665 > reqs[3]:
                logger.debug("Eliminated for grav")
                eliminated_species.add(species)
        if reqs[4] is not None:
            if body.get_temp() > reqs[4]:
                logger.debug("Eliminated for high heat")
                eliminated_species.add(species)
        if reqs[5] is not None:
            if body.get_temp() < reqs[5]:
                logger.debug("Eliminated for low heat")
                eliminated_species.add(species)
        if reqs[6] is not None:
            if reqs[6] == "Any" and body.get_volcanism() == "":
                logger.debug("Eliminated for volcanism")
                eliminated_species.add(species)
            else:
                found = False
                for volc_type in reqs[6]:
                    if body.get_volcanism().find(volc_type) != -1:
                        found = True
                if not found:
                    logger.debug("Eliminated for volcanism")
                    eliminated_species.add(species)
        if reqs[7] is not None:
            if body.get_type() not in reqs[7]:
                logger.debug("Eliminated for body type")
                eliminated_species.add(species)
        if reqs[8] is not None:
            match reqs[8]:
                case '2500ls':
                    if body.get_distance() < 2500.0:
                        eliminated_species.add(species)
                case 'AV':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type.startswith('AVI') and not this.main_star_type.startswith('N'):
                            eliminated_species.add(species)
                case 'OBA':
                    if len(this.main_star_type) > 0:
                        if this.main_star_type[0] not in ['O', 'B', 'A']:
                            eliminated_species.add(species)
                case 'special':
                    eliminated_species.add(species)  # ignore old flora with special rules for now

    final_species = possible_species - eliminated_species
    sorted_species = sorted(final_species, key=lambda species: bio_types[genus][species][1])

    if len(sorted_species) > 0:
        return bio_types[genus][sorted_species[0]][1], bio_types[genus][sorted_species[-1]][1]
    return 0, 0


def get_possible_values(body: BodyData):
    possible_genus = {}
    for genus, species_reqs in bio_types.items():
        min_potential_value, max_potential_value = value_estimate(body, genus)
        if min_potential_value != 0:
            possible_genus[bio_genus[genus]] = (min_potential_value, max_potential_value)

    return sorted(possible_genus.items(), key=lambda gen_v: gen_v[0])


def get_bodyname(fullname: str = ""):
    if fullname.startswith(this.starsystem + ' '):
        bodyname = fullname[len(this.starsystem + ' '):]
    else:
        bodyname = fullname
    return bodyname


def journal_entry(cmdr, is_beta, system, station, entry, state):
    if entry['event'] == 'Fileheader' or entry['event'] == 'LoadGame':
        this.odyssey = entry.get('Odyssey', False)
        this.game_version = semantic_version.Version.coerce(entry.get('gameversion'))

    elif entry['event'] == 'Location':
        this.starsystem = entry['StarSystem']

    elif entry['event'] == 'FSDJump':
        if 'StarSystem' in entry:
            this.starsystem = entry['StarSystem']
        this.main_star_id = entry['BodyID'] if 'BodyID' in entry else 0
        this.main_star_type = ""
        this.bodies = {}
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

    elif entry['event'] == 'SAASignalsFound':
        bodyname_insystem = get_bodyname(entry['BodyName'])

        if bodyname_insystem not in this.bodies:
            body_data = BodyData(bodyname_insystem)
        else:
            body_data = this.bodies[bodyname_insystem]

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


def update_display():
    detail_text = ""
    bio_bodies = sorted(dict(filter(lambda fitem: fitem[1].get_bio_signals() > 0 or len(fitem[1].get_flora()) > 0, this.bodies.items())).items(),
                        key=lambda item: item[1].get_id())

    total_value = 0
    for name, body in bio_bodies:
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
            for genus, values in types:
                count += 1
                detail_text += "{}: {}\n".format(genus,
                                               this.formatter.format_credit_range(values[0], values[1]))
                if len(types) == count:
                    detail_text += "\n"

    if len(bio_bodies) > 0:
        text = 'BioScan Estimates:'
    else:
        text = 'BioScan: No Signals Found'

    this.label['text'] = text
    this.values_label['text'] = detail_text
    this.total_label['text'] = "Analysed System Samples:\n{} | FF: {}".format(this.formatter.format_credits(total_value),
                                                                          this.formatter.format_credits((total_value*5)))

    # if this.show_details.get():
    #     this.scroll_canvas.grid()
    #     this.scrollbar.grid()
    # else:
    #     this.scroll_canvas.grid_remove()
    #     this.scrollbar.grid_remove()


def bind_mousewheel(event):
    if sys.platform in ("linux", "cygwin", "msys"):
        this.scroll_canvas.bind_all('<Button-4>', on_mousewheel)
        this.scroll_canvas.bind_all('<Button-5>', on_mousewheel)
    else:
        this.scroll_canvas.bind_all('<MouseWheel>', on_mousewheel)


def unbind_mousewheel(event):
    if sys.platform in ("linux", "cygwin", "msys"):
        this.scroll_canvas.unbind_all('<Button-4>')
        this.scroll_canvas.unbind_all('<Button-5>')
    else:
        this.scroll_canvas.unbind_all('<MouseWheel>')


def on_mousewheel(event):
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
