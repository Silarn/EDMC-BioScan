import semantic_version

# TKinter imports
import tkinter as tk
from tkinter import colorchooser as tkColorChooser  # type: ignore # noqa: N812
from tkinter import ttk

# Local imports
import bio_scan.const
from bio_scan.globals import bioscan_globals
from bio_scan.tooltip import Tooltip

# Database objects
from ExploData.explo_data import db
import ExploData.explo_data.journal_parse
from ExploData.explo_data.journal_parse import parse_journals

# EDMC imports
import myNotebook as nb
from edmc_data import ship_name_map
from ttkHyperlinkLabel import HyperlinkLabel
from monitor import monitor
from l10n import translations as tr

x_padding = 10
x_button_padding = 12
y_padding = 2


def get_settings(parent: ttk.Notebook) -> tk.Frame:
    """
    Main settings pane builder.

    :param parent: EDMC parent settings pane TKinter frame
    :return: Plugin settings tab TKinter frame
    """

    frame = nb.Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(10, weight=1)

    # Header
    title_frame = nb.Frame(frame)
    title_frame.grid(row=1, columnspan=2, sticky=tk.NSEW)
    title_frame.columnconfigure(0, weight=1)
    HyperlinkLabel(title_frame, text=bioscan_globals.NAME, background=nb.Label().cget('background'),
                   url='https://github.com/Silarn/EDMC-BioScan', underline=True) \
        .grid(row=0, padx=x_padding, sticky=tk.W)
    # LANG: Version tag at the top of the settings pane
    nb.Label(title_frame, text=tr.tl('Version %s', bioscan_globals.translation_context) % bioscan_globals.VERSION) \
        .grid(row=0, column=1, sticky=tk.E)
    # LANG: Data version tag at the top of the settings pane
    nb.Label(title_frame, text=tr.tl('Data Version: %s', bioscan_globals.translation_context) % bio_scan.const.db_version) \
        .grid(row=0, column=2, padx=x_padding, sticky=tk.E)
    HyperlinkLabel(title_frame, text=ExploData.explo_data.const.plugin_name, background=nb.Label().cget('background'),
                   url='https://github.com/Silarn/EDMC-ExploData', underline=True) \
        .grid(row=1, padx=x_padding, pady=y_padding * 2, sticky=tk.W)
    nb.Label(title_frame, text=tr.tl('Version %s', bioscan_globals.translation_context) % semantic_version.Version(ExploData.explo_data.const.plugin_version)) \
        .grid(row=1, column=1, pady=y_padding * 2, sticky=tk.E)
    nb.Label(title_frame, text=tr.tl('Data Version: %s', bioscan_globals.translation_context) % ExploData.explo_data.const.database_version) \
        .grid(row=1, column=2, padx=x_padding, pady=y_padding * 2, sticky=tk.E)

    # Tabs
    notebook = ttk.Notebook(frame)
    # LANG: General settings tab label
    notebook.add(get_general_tab(notebook), text=tr.tl('General Settings', bioscan_globals.translation_context))
    # LANG: Overlay settings tab label
    notebook.add(get_overlay_tab(notebook), text=tr.tl('Overlay Settings', bioscan_globals.translation_context))
    notebook.grid(row=10, columnspan=2, pady=0, sticky=tk.NSEW)

    # Footer
    # LANG: Journal parsing toggle button text
    nb.Button(frame, text=tr.tl('Start / Stop Journal Parsing', bioscan_globals.translation_context), command=parse_journals) \
        .grid(row=12, column=0, padx=x_padding, sticky=tk.SW)

    nb.Checkbutton(
        frame,
        text=tr.tl('Enable Debug Logging', bioscan_globals.translation_context),  # LANG: Debug logging checkbox label
        variable=bioscan_globals.debug_logging_enabled
    ).grid(row=12, column=1, padx=x_button_padding, sticky=tk.SE)

    return frame


def get_general_tab(parent: ttk.Notebook) -> tk.Frame:
    """
    General tab builder.

    :param parent: Parent tab frame
    :return: Frame for overlay tab
    """

    frame = nb.Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.grid(sticky=tk.NSEW)

    # Left column
    left_column = tk.Frame(frame, background='')
    left_column.grid(row=0, column=0, sticky=tk.NSEW)
    left_column.rowconfigure(6, weight=1)
    signal_label = nb.Label(
        left_column,
        text=tr.tl('Focus Bio Details List: (?)', bioscan_globals.translation_context),  # LANG: Body focus filter settings title
    )
    signal_label.grid(row=0, padx=x_padding, sticky=tk.W)
    Tooltip(
        signal_label,
        # LANG: Tooltip text for body focus filter settings #1
        text=tr.tl('This setting controls when the prediction details should display.', bioscan_globals.translation_context) + '\n\n' +
        # LANG: Tooltip text for body focus filter settings #2
        tr.tl('When filtered, you will only see details for the bio signals relevant to your current location.', bioscan_globals.translation_context),
        waittime=1000
    )
    focus_options = [
        'Never',
        'On Approach',
        'Near Surface',
        'On Surface',
    ]
    nb.OptionMenu(
        left_column,
        bioscan_globals.focus_setting,
        bioscan_globals.focus_setting.get(),
        *focus_options
    ).grid(row=1, padx=x_padding, pady=y_padding, column=0, sticky=tk.W)
    nb.Label(left_column,
             # LANG: Settings explanation for body focus filter options (dropdown options (e.g. On Approach) should not be translated)
             text=tr.tl('Never: Never filter signal details', bioscan_globals.translation_context) + '\n' +
                        tr.tl('On Approach: Show only local signals on approach', bioscan_globals.translation_context) + '\n' +
                        tr.tl('Near Surface: Show signals under given altitude (see below)', bioscan_globals.translation_context) + '\n' +
                        tr.tl('On Surface: Show only local signals when on surface', bioscan_globals.translation_context),
             justify=tk.LEFT) \
        .grid(row=2, padx=x_padding, column=0, sticky=tk.NW)
    nb.Label(left_column, text=tr.tl('Altitude (in meters) for "Near Surface":', bioscan_globals.translation_context)) \
        .grid(row=3, column=0, padx=x_padding, sticky=tk.SW)
    nb.EntryMenu(
        left_column, text=bioscan_globals.focus_distance.get(), textvariable=bioscan_globals.focus_distance,
        validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=4, column=0, padx=x_padding, sticky=tk.NW)
    ttk.Separator(left_column).grid(row=5, column=0, pady=y_padding * 2, sticky=tk.EW)
    nb.Checkbutton(
        left_column,
        text=tr.tl('Show complete breakdown of genera with multiple matches', bioscan_globals.translation_context),
        variable=bioscan_globals.focus_breakdown
    ).grid(row=6, column=0, padx=0, sticky=tk.W)
    nb.Checkbutton(
        left_column,
        text=tr.tl('Shorten credits displays (eg. 19.8 MCr)', bioscan_globals.translation_context),
        variable=bioscan_globals.credits_setting
    ).grid(row=7, column=0, padx=0, sticky=tk.W)
    nb.Checkbutton(
        left_column,
        text=tr.tl('Exclude bodies with fewer than x signals:', bioscan_globals.translation_context),
        variable=bioscan_globals.exclude_signals
    ).grid(row=8, column=0, padx=0, sticky=tk.W)
    nb.EntryMenu(
        left_column, text=bioscan_globals.minimum_signals.get(), textvariable=bioscan_globals.minimum_signals,
        validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=9, column=0, padx=x_padding, sticky=tk.NW)
    nb.Label(left_column, text=tr.tl('Scrollbox height (px):', bioscan_globals.translation_context)) \
        .grid(row=10, column=0, padx=x_padding, sticky=tk.SW)
    nb.EntryMenu(
        left_column, text=bioscan_globals.box_height.get(), textvariable=bioscan_globals.box_height,
        validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=11, column=0, padx=x_padding, sticky=tk.NW)

    # Right column
    right_column = tk.Frame(frame, background='')
    right_column.grid(row=0, column=1, sticky=tk.NSEW)
    left_column.rowconfigure(9, weight=1)
    signal_summary_label = nb.Label(
        right_column,
        text=tr.tl('Display Signal Summary: (?)', bioscan_globals.translation_context)
    )
    signal_summary_label.grid(row=0, column=0, sticky=tk.W)
    Tooltip(
        signal_summary_label,
        # LANG: Signal summary tooltip line 1
        text=tr.tl('This option determines when to display the signal summary at the top of the pane.', bioscan_globals.translation_context) +
             # LANG: Signal summary tooltip line 2
             '\r\n' + tr.tl('eg. B 1 (R): 5  ⬦ B 2 (HMC): 2', bioscan_globals.translation_context),
        waittime=1000
    )
    signal_options = [
        'Always',
        'In Flight',
    ]
    nb.OptionMenu(
        right_column,
        bioscan_globals.signal_setting,
        bioscan_globals.signal_setting.get(),
        *signal_options
    ).grid(row=2, column=0, pady=y_padding, sticky=tk.W)
    nb.Label(right_column,
             text=tr.tl('Always: Always display the body signal summary', bioscan_globals.translation_context) + '\n' +
                        tr.tl('In Flight: Show the signal summary in flight only', bioscan_globals.translation_context),
             justify=tk.LEFT) \
        .grid(row=3, column=0, sticky=tk.NW)
    ttk.Separator(right_column).grid(row=4, column=0, pady=y_padding * 2, sticky=tk.EW)
    completed_display_label = nb.Label(
        right_column,
        # LANG: Label for options pertaining to completed scans
        text=tr.tl('Completed Scan Display: (?)', bioscan_globals.translation_context)
    )
    completed_display_label.grid(row=5, column=0, sticky=tk.W)
    Tooltip(
        completed_display_label,
        # LANG: Tooltip for 'Completed Scan Display' label
        text=tr.tl('This option determines how to display species that have been fully scanned.', bioscan_globals.translation_context),
        waittime=1000
    )
    scan_options = [
        'Check',
        'Hide',
        'Hide in System'
    ]
    nb.OptionMenu(
        right_column,
        bioscan_globals.scan_display_mode,
        bioscan_globals.scan_display_mode.get(),
        *scan_options
    ).grid(row=6, column=0, sticky=tk.W)
    nb.Label(right_column,
             text=tr.tl('Check: Always show species with a checkmark when complete', bioscan_globals.translation_context) + '\n' +
                  tr.tl('Hide: Always hide completed species', bioscan_globals.translation_context) + '\n' +
                  tr.tl('Hide in System: Hide completed species in the full system view', bioscan_globals.translation_context),
             justify=tk.LEFT) \
        .grid(row=7, column=0, sticky=tk.NW)
    nb.Checkbutton(
        right_column,
        text=tr.tl('Completely hide body when all samples are complete', bioscan_globals.translation_context),
        variable=bioscan_globals.hide_body_complete
    ).grid(row=8, column=0, padx=0, sticky=tk.W)
    ttk.Separator(right_column).grid(row=9, column=0, pady=y_padding * 2, sticky=tk.EW)
    nb.Checkbutton(
        right_column,
        text=tr.tl('Enable species waypoints with the comp. scanner', bioscan_globals.translation_context),
        variable=bioscan_globals.waypoints_enabled
    ).grid(row=10, column=0, padx=0, sticky=tk.W)
    nb.Checkbutton(
        right_column,
        text=tr.tl('Hide waypoint bearings with radar enabled (see overlay)', bioscan_globals.translation_context),
        variable=bioscan_globals.hide_waypoint_bearings,
        state=tk.ACTIVE if bioscan_globals.overlay.available() else tk.DISABLED
    ).grid(row=11, column=0, padx=0, sticky=tk.W)

    return frame


def get_overlay_tab(parent: ttk.Notebook) -> tk.Frame:
    """
    Overlay tab builder.

    :param parent: Parent tab frame
    :return: Frame for overlay tab
    """

    ship_name = monitor.state['ShipName'] if monitor.state['ShipName'] else ship_name_map.get(
                monitor.state['ShipType'], monitor.state['ShipType'])

    frame = nb.Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    left_frame = tk.Frame(frame)
    left_frame.columnconfigure(0, weight=1)
    right_frame = tk.Frame(frame)
    right_frame.columnconfigure(0, weight=1)

    left_frame.grid(row=0, column=0, sticky=tk.NSEW)
    color_button = None
    ship_list = nb.Label(
        left_frame,
        text=', '.join(get_ship_names()) if len(bioscan_globals.ship_whitelist) else tr.tl('None', bioscan_globals.translation_context),
        justify=tk.LEFT
    )
    add_ship_button = None
    remove_ship_button = None
    clear_ships_button = None

    def color_chooser() -> None:
        """
        Color selector for overlay text
        """

        (_, color) = tkColorChooser.askcolor(
            bioscan_globals.overlay_color.get(), title=tr.tl('Overlay Color', bioscan_globals.translation_context), parent=bioscan_globals.parent
        )

        if color:
            bioscan_globals.overlay_color.set(color)
            if color_button is not None:
                color_button['foreground'] = color

    def add_ship() -> None:
        """
        Adds active ship to whitelist
        """

        if ship_name not in bioscan_globals.ship_whitelist:
            bioscan_globals.ship_whitelist.append(f'{monitor.state["ShipID"]}:{ship_name}')
            add_ship_button.grid_remove()
            remove_ship_button.grid(row=0, column=0, padx=x_padding, sticky=tk.W)
            clear_ships_button['state'] = tk.NORMAL
            ship_list['text'] = ', '.join(get_ship_names())

    def remove_ship() -> None:
        """
        Removes active ship to whitelist
        """

        for ship in bioscan_globals.ship_whitelist:
            ship_data = ship.split(':')
            if len(ship_data) == 1:
                if ship_name == ship_data[0]:
                    bioscan_globals.ship_whitelist.remove(ship)
                    remove_ship_button.grid_remove()
                    add_ship_button.grid(row=0, column=0, padx=x_padding, sticky=tk.W)
                    break
            else:
                if monitor.state['ShipID'] == int(ship_data[0]):
                    bioscan_globals.ship_whitelist.remove(ship)
                    remove_ship_button.grid_remove()
                    add_ship_button.grid(row=0, column=0, padx=x_padding, sticky=tk.W)
                    break

        if len(bioscan_globals.ship_whitelist):
            ship_list['text'] = ', '.join(get_ship_names())
        else:
            clear_ships_button['state'] = tk.DISABLED
            ship_list['text'] = 'None'

    def clear_ships() -> None:
        """
        Clears ship whitelist
        """

        bioscan_globals.ship_whitelist.clear()
        clear_ships_button['state'] = tk.DISABLED
        ship_list['text'] = tr.tl('None', bioscan_globals.translation_context)
        if ship_name:
            remove_ship_button.grid_remove()
            add_ship_button.grid(row=0, column=0, padx=x_padding, sticky=tk.W)

    nb.Checkbutton(
        left_frame,
        text=tr.tl('Enable overlay', bioscan_globals.translation_context),
        variable=bioscan_globals.use_overlay,
        state=tk.NORMAL if bioscan_globals.overlay.available() else tk.DISABLED
    ).grid(row=0, column=0, padx=x_button_padding, pady=0, sticky=tk.W)
    color_button = tk.Button(
        left_frame,
        text=tr.tl('Text Color', bioscan_globals.translation_context),
        foreground=bioscan_globals.overlay_color.get(),
        background='grey4',
        command=lambda: color_chooser()
    )
    color_button.grid(row=1, column=0, padx=x_button_padding, pady=y_padding, sticky=tk.NW)

    nb.Label(
        left_frame,
        text=tr.tl('Line spacing:', bioscan_globals.translation_context),
        justify=tk.LEFT
    ).grid(row=2, column=0, padx=x_padding, pady=y_padding, sticky=tk.W)

    linespace_frame = tk.Frame(left_frame)
    linespace_frame.grid(row=3, column=0, sticky=tk.NW)
    linespace_frame.columnconfigure(3, weight=1)
    nb.Label(
        linespace_frame,
        text=tr.tl('Normal:', bioscan_globals.translation_context),
        justify=tk.LEFT
    ).grid(row=0, column=0, padx=x_padding, pady=y_padding, sticky=tk.W)
    nb.EntryMenu(
        linespace_frame, text=bioscan_globals.overlay_line_spacing_normal.get(),
        textvariable=bioscan_globals.overlay_line_spacing_normal,
        width=8, validate='all', validatecommand=(linespace_frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=1, pady=y_padding, sticky=tk.W)
    nb.Label(
        linespace_frame,
        text=tr.tl('Large:', bioscan_globals.translation_context),
        justify=tk.LEFT
    ).grid(row=0, column=2, padx=x_padding, pady=y_padding, sticky=tk.W)
    nb.EntryMenu(
        linespace_frame, text=bioscan_globals.overlay_line_spacing_large.get(),
        textvariable=bioscan_globals.overlay_line_spacing_large,
        width=8, validate='all', validatecommand=(linespace_frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=3, pady=y_padding, sticky=tk.W)

    ttk.Separator(left_frame).grid(row=4, column=0, pady=y_padding * 2, sticky=tk.EW)

    whitelist_label = nb.Label(
        left_frame,
        text=tr.tl('Ship Whitelist (?)', bioscan_globals.translation_context),
        justify=tk.LEFT
    )
    whitelist_label.grid(row=5, column=0, padx=x_padding, pady=y_padding, sticky=tk.W)
    Tooltip(
        whitelist_label,
        text=tr.tl('Ships added to this list will display BioScan on the overlay.', bioscan_globals.translation_context) +
             '\n\n' + tr.tl('When empty, BioScan will display for all ships.', bioscan_globals.translation_context),
        waittime=1000
    )
    ship_list.grid(row=6, column=0, padx=x_padding, pady=y_padding, sticky=tk.W)

    ship_whitelist_frame = tk.Frame(left_frame)
    ship_whitelist_frame.grid(row=7, column=0, sticky=tk.NW)
    ship_whitelist_frame.columnconfigure(2, weight=1)

    add_ship_button = nb.Button(ship_whitelist_frame, text=tr.tl('Add', bioscan_globals.translation_context) + f' "{ship_name}"',
                                command=add_ship)
    remove_ship_button = nb.Button(ship_whitelist_frame, text=tr.tl('Remove', bioscan_globals.translation_context) + f' "{ship_name}"',
                                   command=remove_ship)
    clear_ships_button = nb.Button(ship_whitelist_frame, text=tr.tl('Clear Ships', bioscan_globals.translation_context), command=clear_ships)
    if ship_name:
        if ship_in_whitelist(monitor.state['ShipID'], ship_name):
            remove_ship_button.grid(row=0, column=0, padx=x_button_padding, pady=y_padding, sticky=tk.W)
        else:
            add_ship_button.grid(row=0, column=0, padx=x_button_padding, pady=y_padding, sticky=tk.W)
    if not len(bioscan_globals.ship_whitelist):
        clear_ships_button['state'] = tk.DISABLED
    clear_ships_button.grid(row=0, column=1, padx=x_button_padding, pady=y_padding, sticky=tk.W)

    # Second column
    right_frame.grid(row=0, column=1, sticky=tk.NSEW)
    anchor_frame = tk.Frame(right_frame)
    anchor_frame.grid(row=0, column=1, sticky=tk.NSEW)
    anchor_frame.columnconfigure(4, weight=1)
    summary_frame = tk.Frame(right_frame)
    summary_frame.grid(row=1, column=1, sticky=tk.NSEW)
    summary_frame.columnconfigure(4, weight=1)
    details_frame = tk.Frame(right_frame)
    details_frame.grid(row=2, column=1, sticky=tk.NSEW)
    details_frame.columnconfigure(4, weight=1)

    nb.Label(anchor_frame, text=tr.tl('Prediction Details Anchor:', bioscan_globals.translation_context)) \
        .grid(row=0, column=0, padx=x_padding, pady=y_padding, sticky=tk.W)
    nb.Label(anchor_frame, text='X') \
        .grid(row=0, column=1, padx=(x_padding, 0), pady=y_padding, sticky=tk.W)
    nb.EntryMenu(
        anchor_frame, text=bioscan_globals.overlay_anchor_x.get(), textvariable=bioscan_globals.overlay_anchor_x,
        width=8, validate='all', validatecommand=(anchor_frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=2, padx=(0, x_padding), pady=y_padding, sticky=tk.W)
    nb.Label(anchor_frame, text='Y') \
        .grid(row=0, column=3, padx=(x_padding, 0), pady=y_padding, sticky=tk.W)
    nb.EntryMenu(
        anchor_frame, text=bioscan_globals.overlay_anchor_y.get(), textvariable=bioscan_globals.overlay_anchor_y,
        width=8, validate='all', validatecommand=(anchor_frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=4, padx=(0, x_padding), pady=y_padding, sticky=tk.W)

    nb.Label(summary_frame, text=tr.tl('Summary / Progress Anchor:', bioscan_globals.translation_context)) \
        .grid(row=0, column=0, padx=x_padding, pady=y_padding, sticky=tk.W)
    nb.Label(summary_frame, text='X') \
        .grid(row=0, column=1, padx=(x_padding, 0), pady=y_padding, sticky=tk.W)
    nb.EntryMenu(
        summary_frame, text=bioscan_globals.overlay_summary_x.get(), textvariable=bioscan_globals.overlay_summary_x,
        width=8, validate='all', validatecommand=(summary_frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=2, padx=(0, x_padding), pady=y_padding, sticky=tk.W)
    nb.Label(summary_frame, text='Y') \
        .grid(row=0, column=3, padx=(x_padding, 0), pady=y_padding, sticky=tk.W)
    nb.EntryMenu(
        summary_frame, text=bioscan_globals.overlay_summary_y.get(), textvariable=bioscan_globals.overlay_summary_y,
        width=8, validate='all', validatecommand=(summary_frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=4, padx=(0, x_padding), pady=y_padding, sticky=tk.W)

    nb.Checkbutton(
        details_frame,
        text=tr.tl('Scroll details', bioscan_globals.translation_context),
        variable=bioscan_globals.overlay_detail_scroll
    ).grid(row=0, column=0, padx=x_padding, pady=y_padding, sticky=tk.NW)
    nb.Label(details_frame, text=tr.tl('Maximum details length:', bioscan_globals.translation_context)) \
        .grid(row=1, column=0, padx=x_padding, pady=y_padding, sticky=tk.W)
    nb.EntryMenu(
        details_frame, text=bioscan_globals.overlay_detail_length.get(), textvariable=bioscan_globals.overlay_detail_length,
        width=8, validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=1, column=1, padx=(0, x_padding), pady=y_padding, sticky=tk.W)
    nb.Label(details_frame, text=tr.tl('Scroll delay (sec):', bioscan_globals.translation_context)) \
        .grid(row=1, column=2, padx=x_padding, pady=y_padding, sticky=tk.W)
    nb.EntryMenu(
        details_frame, text=bioscan_globals.overlay_detail_delay.get(), textvariable=bioscan_globals.overlay_detail_delay,
        width=8, validate='all', validatecommand=(frame.register(is_double), '%P', '%d')
    ).grid(row=1, column=3, padx=(0, x_padding), pady=y_padding, sticky=tk.W)

    ttk.Separator(right_frame).grid(row=3, column=1, pady=y_padding * 2, sticky=tk.EW)

    radar_frame = tk.Frame(right_frame)
    radar_frame.grid(row=4, column=1, sticky=tk.NSEW)
    radar_frame.columnconfigure(2, weight=1)

    # LANG: Waypoint / scan radar overlay settings title
    radar_label = nb.Label(radar_frame, text=tr.tl('Active Scan / Waypoint Radar (?):', bioscan_globals.translation_context))
    radar_label.grid(row=0, column=0, padx=x_padding, pady=y_padding, columnspan=3, sticky=tk.W)
    Tooltip(
        radar_label,
        # LANG: Ship overlay tooltip; Line 1
        text=tr.tl('Draw a radar on the overlay when active scans and waypoints are present.', bioscan_globals.translation_context) +
        # LANG: Ship overlay tooltip; Line 2
             '\n\n' + tr.tl('This displays bio markers up to a defined distance and shows a display of the minimum scan distance.', bioscan_globals.translation_context) +
             # LANG: Ship overlay tooltip; Line 3
             '\n\n' + tr.tl('This is oriented where up is the direction you\'re facing. The ship location can be tracked as well.', bioscan_globals.translation_context),
        waittime=1000
    )
    nb.Checkbutton(radar_frame,
        # LANG: Radar enable / disable setting
        text=tr.tl('Enable Radar', bioscan_globals.translation_context),
        variable=bioscan_globals.radar_enabled
    ).grid(row=1, column=0, padx=x_padding, pady=y_padding, sticky=tk.NW)
    nb.Checkbutton(radar_frame,
        # LANG: Radar ship location tracking enable / disable setting
        text=tr.tl('Enable Ship Location Tracker', bioscan_globals.translation_context),
        variable=bioscan_globals.radar_ship_loc_enabled
    ).grid(row=1, column=1, columnspan=2, padx=x_padding, pady=y_padding, sticky=tk.NW)

    radar_anchor_frame = tk.Frame(radar_frame)
    radar_anchor_frame.grid(row=2, column=0, columnspan=3, sticky=tk.NSEW)
    radar_anchor_frame.columnconfigure(4, weight=1)
    # LANG: Main label for radar x/y/radius configuration
    nb.Label(radar_anchor_frame, text=tr.tl('Radar Anchor (Center Point):', bioscan_globals.translation_context)) \
        .grid(row=2, column=0, padx=x_padding, pady=y_padding, sticky=tk.W)
    nb.Label(radar_anchor_frame, text='X') \
        .grid(row=2, column=1, padx=(x_padding, 0), pady=y_padding, sticky=tk.W)
    nb.EntryMenu(
        radar_anchor_frame, text=bioscan_globals.radar_anchor_x.get(), textvariable=bioscan_globals.radar_anchor_x,
        width=8, validate='all', validatecommand=(radar_anchor_frame.register(is_digit), '%P', '%d')
    ).grid(row=2, column=2, padx=(0, x_padding), pady=y_padding, sticky=tk.W)
    nb.Label(radar_anchor_frame, text='Y') \
        .grid(row=2, column=3, padx=(x_padding, 0), pady=y_padding, sticky=tk.W)
    nb.EntryMenu(
        radar_anchor_frame, text=bioscan_globals.radar_anchor_y.get(), textvariable=bioscan_globals.radar_anchor_y,
        width=8, validate='all', validatecommand=(radar_anchor_frame.register(is_digit), '%P', '%d')
    ).grid(row=2, column=4, padx=(0, x_padding), pady=y_padding, sticky=tk.W)

    # LANG: Radius label for radar display settings
    nb.Label(radar_frame, text=tr.tl('Radius:', bioscan_globals.translation_context)) \
        .grid(row=3, column=0, padx=x_padding, pady=y_padding, sticky=tk.W)
    nb.EntryMenu(
        radar_frame, text=bioscan_globals.radar_radius.get(), textvariable=bioscan_globals.radar_radius,
        width=8, validate='all', validatecommand=(radar_frame.register(is_digit), '%P', '%d')
    ).grid(row=3, column=1, padx=x_padding, pady=y_padding, columnspan=2, sticky=tk.W)
    # LANG: Distance label for radar display settings
    nb.Label(radar_frame, text=tr.tl('Maximum radar distance:', bioscan_globals.translation_context)) \
        .grid(row=4, column=0, padx=x_padding, pady=y_padding, sticky=tk.W)
    nb.EntryMenu(
        radar_frame, text=bioscan_globals.radar_max_distance.get(), textvariable=bioscan_globals.radar_max_distance,
        width=8, validate='all', validatecommand=(radar_frame.register(is_digit), '%P', '%d')
    ).grid(row=4, column=1, padx=(x_padding, 0), pady=y_padding, sticky=tk.W)
    nb.Label(radar_frame, text=tr.tl('m', bioscan_globals.translation_context)) \
        .grid(row=4, column=2, padx=(0, x_padding), pady=y_padding, sticky=tk.W)
    nb.Checkbutton(radar_frame,
        # LANG: Radar ship location tracking enable / disable setting
        text=tr.tl('Use logarithmic scaling', bioscan_globals.translation_context),
        variable=bioscan_globals.radar_use_log
    ).grid(row=5, column=0, columnspan=3, padx=x_padding, pady=y_padding, sticky=tk.NW)

    return frame


def get_ship_names() -> list[str]:
    """
    Process and return sorted array of overlay whitelist ship names

    :return: Sorted array of ship names
    """

    ships: list[str] = []
    for ship in bioscan_globals.ship_whitelist:
        ship_data = ship.split(':')
        ships.append(ship_data[-1])
    return sorted(ships)


def ship_in_whitelist(ship_id: int, name: str) -> bool:
    """
    Check if the specified ship ID and / or name is in the overlay whitelist

    :param ship_id: The ship ID
    :param name: The ship name (custom or default)
    :return: Whether or not ship is in the overlay whitelist
    """

    if f'{ship_id}:{name}' in bioscan_globals.ship_whitelist:
        return True
    if name and name in bioscan_globals.ship_whitelist:
        return True
    return False


def change_ship_name(ship_id: int, name: str) -> None:
    """
    Change the stored ship name in EDMC storage assigned to the given ship ID

    :param ship_id: The ship ID
    :param name: The ship name (custom or default)
    """

    for ship in bioscan_globals.ship_whitelist:
        if ship.startswith(f'{ship_id}:'):
            bioscan_globals.ship_whitelist.append(f'{ship_id}:{name}')
            bioscan_globals.ship_whitelist.remove(ship)
            break


def ship_sold(ship_id: int) -> None:
    """
    Remove sold ship from overlay whitelist

    :param ship_id: The ship ID
    """

    for ship in bioscan_globals.ship_whitelist:
        if ship.startswith(ship_id):
            bioscan_globals.ship_whitelist.remove(ship)
            return


def add_ship_id(ship_id: int, name: str) -> None:
    """
    Convert old name-based storage to ID:name if ship name is in the overlay whitelist

    :param ship_id: The ship ID
    :param name: The ship name (custom or default)
    """

    if name in bioscan_globals.ship_whitelist:
        bioscan_globals.ship_whitelist.remove(name)
        bioscan_globals.ship_whitelist.append(f'{ship_id}:{name}')


def sync_ship_name(ship_id: int, name: str) -> None:
    """
    Update the ship name in the overlay whitelist on change

    :param ship_id: The ship ID
    :param name: The ship name (custom or default)
    """

    for ship in bioscan_globals.ship_whitelist:
        if ship.startswith(f'{ship_id}:'):
            if ship != f'{ship_id}:{name}':
                bioscan_globals.ship_whitelist.remove(ship)
                bioscan_globals.ship_whitelist.append(f'{ship_id}:{name}')
            return


def is_digit(value: str, action: str) -> bool:
    """
    Numeral validator for Entry input

    :param value: Value for input event
    :param action: Input event action type
    :return: True or false if input is a numeral
    """

    if action == '1':
        if not value.isdigit():
            return False
    return True


def is_double(value: str, action: str) -> bool:
    """
    Double validator for Entry input

    :param value: Value for input event
    :param action: Input event action type
    :return: True or false if input is a numeral
    """

    if action == '1':
        try:
            float(value)
        except ValueError:
            return False
    return True
