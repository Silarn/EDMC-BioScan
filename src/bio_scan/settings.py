import semantic_version

# TKinter imports
import tkinter as tk
from tkinter import colorchooser as tkColorChooser  # type: ignore # noqa: N812
from tkinter import ttk

# Local imports
import bio_scan.const
from bio_scan.globals import Globals
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

x_padding = 10
x_button_padding = 12
y_padding = 2


def get_settings(parent: ttk.Notebook, bioscan_globals: Globals) -> tk.Frame:
    """
    Main settings pane builder.

    :param parent: EDMC parent settings pane TKinter frame
    :param bioscan_globals: Plugin globals
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
    nb.Label(title_frame, text='Version %s' % bioscan_globals.VERSION) \
        .grid(row=0, column=1, sticky=tk.E)
    nb.Label(title_frame, text='Data Version: %s' % bio_scan.const.db_version) \
        .grid(row=0, column=2, padx=x_padding, sticky=tk.E)
    HyperlinkLabel(title_frame, text=ExploData.explo_data.const.plugin_name, background=nb.Label().cget('background'),
                   url='https://github.com/Silarn/EDMC-ExploData', underline=True) \
        .grid(row=1, padx=x_padding, pady=y_padding * 2, sticky=tk.W)
    nb.Label(title_frame, text='Version %s' % semantic_version.Version(ExploData.explo_data.const.plugin_version)) \
        .grid(row=1, column=1, pady=y_padding * 2, sticky=tk.E)
    nb.Label(title_frame, text='Data Version: %s' % ExploData.explo_data.const.database_version) \
        .grid(row=1, column=2, padx=x_padding, pady=y_padding * 2, sticky=tk.E)

    # Tabs
    notebook = ttk.Notebook(frame)
    notebook.add(get_general_tab(notebook, bioscan_globals), text='General Settings')
    notebook.add(get_overlay_tab(notebook, bioscan_globals), text='Overlay Settings')
    notebook.grid(row=10, columnspan=2, pady=0, sticky=tk.NSEW)

    # Footer
    nb.Button(frame, text='Start / Stop Journal Parsing', command=parse_journals) \
        .grid(row=12, column=0, padx=x_padding, sticky=tk.SW)

    nb.Checkbutton(
        frame,
        text='Enable Debug Logging',
        variable=bioscan_globals.debug_logging_enabled
    ).grid(row=12, column=1, padx=x_button_padding, sticky=tk.SE)

    return frame


def get_general_tab(parent: ttk.Notebook, bioscan_globals: Globals) -> tk.Frame:
    """
    General tab builder.

    :param parent: Parent tab frame
    :param bioscan_globals: BioScan globals object
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
        text='Focus Body Signals: (?)',
    )
    signal_label.grid(row=0, padx=x_padding, sticky=tk.W)
    Tooltip(
        signal_label,
        text='This setting controls when the prediction details should display.\n\n' +
        'When filtered, you will only see details for the bio signals relevant to your current location.',
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
             text='Never: Never filter signal details\n'
                  'On Approach: Show only local signals on approach\n'
                  'Near Surface: Show signals under given altitude (see below)\n'
                  'On Surface: Show only local signals when on surface',
             justify=tk.LEFT) \
        .grid(row=2, padx=x_padding, column=0, sticky=tk.NW)
    nb.Label(left_column, text='Altitude (in meters) for "Near Surface":') \
        .grid(row=3, column=0, padx=x_padding, sticky=tk.SW)
    nb.EntryMenu(
        left_column, text=bioscan_globals.focus_distance.get(), textvariable=bioscan_globals.focus_distance,
        validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=4, column=0, padx=x_padding, sticky=tk.NW)
    ttk.Separator(left_column).grid(row=5, column=0, pady=y_padding * 2, sticky=tk.EW)
    nb.Checkbutton(
        left_column,
        text='Show complete breakdown of genera with multiple matches',
        variable=bioscan_globals.focus_breakdown
    ).grid(row=6, column=0, padx=0, sticky=tk.W)
    nb.Checkbutton(
        left_column,
        text='Shorten credits displays (eg. 19.8 MCr)',
        variable=bioscan_globals.credits_setting
    ).grid(row=7, column=0, padx=0, sticky=tk.W)
    nb.Checkbutton(
        left_column,
        text='Exclude bodies with fewer than x signals:',
        variable=bioscan_globals.exclude_signals
    ).grid(row=8, column=0, padx=0, sticky=tk.W)
    nb.EntryMenu(
        left_column, text=bioscan_globals.minimum_signals.get(), textvariable=bioscan_globals.minimum_signals,
        validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=9, column=0, padx=x_padding, sticky=tk.NW)
    nb.Label(left_column, text='Scrollbox height (px):') \
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
        text='Display Signal Summary: (?)'
    )
    signal_summary_label.grid(row=0, column=0, sticky=tk.W)
    Tooltip(
        signal_summary_label,
        text='This option determines when to display the signal summary at the top of the pane.\n\n' +
             'eg. B 1 (R): 5  ⬦ B 2 (HMC): 2',
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
             text='Always: Always display the body signal summary\n'
                  'In Flight: Show the signal summary in flight only',
             justify=tk.LEFT) \
        .grid(row=3, column=0, sticky=tk.NW)
    ttk.Separator(right_column).grid(row=4, column=0, pady=y_padding * 2, sticky=tk.EW)
    completed_display_label = nb.Label(
        right_column,
        text='Completed Scan Display: (?)'
    )
    completed_display_label.grid(row=5, column=0, sticky=tk.W)
    Tooltip(
        completed_display_label,
        text='This option determines how to display species that have been fully scanned.',
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
             text='Check: Always show species with a checkmark when complete\n'
                  'Hide: Always hide completed species\n'
                  'Hide in System: Hide completed species in the full system view',
             justify=tk.LEFT) \
        .grid(row=7, column=0, sticky=tk.NW)
    ttk.Separator(right_column).grid(row=8, column=0, pady=y_padding * 2, sticky=tk.EW)
    nb.Checkbutton(
        right_column,
        text='Enable species waypoints with the comp. scanner',
        variable=bioscan_globals.waypoints_enabled
    ).grid(row=9, column=0, padx=0, sticky=tk.W)

    return frame


def get_overlay_tab(parent: ttk.Notebook, bioscan_globals: Globals) -> tk.Frame:
    """
    Overlay tab builder.

    :param parent: Parent tab frame
    :param bioscan_globals: BioScan globals object
    :return: Frame for overlay tab
    """

    ship_name = monitor.state['ShipName'] if monitor.state['ShipName'] else ship_name_map.get(
                monitor.state['ShipType'], monitor.state['ShipType'])

    frame = nb.Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(5, weight=1)
    color_button = None
    ship_list = nb.Label(
        frame,
        text=', '.join(get_ship_names(bioscan_globals)) if len(bioscan_globals.ship_whitelist) else 'None',
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
            bioscan_globals.overlay_color.get(), title='Overlay Color', parent=bioscan_globals.parent
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
            ship_list['text'] = ', '.join(get_ship_names(bioscan_globals))

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
            ship_list['text'] = ', '.join(get_ship_names(bioscan_globals))
        else:
            clear_ships_button['state'] = tk.DISABLED
            ship_list['text'] = 'None'

    def clear_ships() -> None:
        """
        Clears ship whitelist
        """

        bioscan_globals.ship_whitelist.clear()
        clear_ships_button['state'] = tk.DISABLED
        ship_list['text'] = 'None'
        if ship_name:
            remove_ship_button.grid_remove()
            add_ship_button.grid(row=0, column=0, padx=x_padding, sticky=tk.W)

    nb.Checkbutton(
        frame,
        text='Enable overlay',
        variable=bioscan_globals.use_overlay
    ).grid(row=0, column=0, padx=x_button_padding, pady=0, sticky=tk.W)
    color_button = tk.Button(
        frame,
        text='Text Color',
        foreground=bioscan_globals.overlay_color.get(),
        background='grey4',
        command=lambda: color_chooser()
    )
    color_button.grid(row=1, column=0, padx=x_button_padding, pady=y_padding, sticky=tk.NW)

    whitelist_label = nb.Label(
        frame,
        text='Ship Whitelist (?)',
        justify=tk.LEFT
    )
    whitelist_label.grid(row=2, column=0, padx=x_padding, sticky=tk.W)
    Tooltip(
        whitelist_label,
        text='Ships added to this list will display BioScan on the overlay.\n' +
             'When empty, BioScan will display for all ships.',
        waittime=1000
    )
    ship_list.grid(row=3, column=0, padx=x_padding, sticky=tk.W)

    ship_whitelist_frame = tk.Frame(frame)
    ship_whitelist_frame.grid(row=4, column=0, sticky=tk.NSEW)
    ship_whitelist_frame.columnconfigure(1, weight=1)

    add_ship_button = nb.Button(ship_whitelist_frame, text=f'Add "{ship_name}"',
                                command=add_ship)
    remove_ship_button = nb.Button(ship_whitelist_frame, text=f'Remove "{ship_name}"',
                                   command=remove_ship)
    clear_ships_button = nb.Button(ship_whitelist_frame, text='Clear Ships', command=clear_ships)
    if ship_name:
        if ship_in_whitelist(monitor.state['ShipID'], ship_name, bioscan_globals):
            remove_ship_button.grid(row=0, column=0, padx=x_padding, sticky=tk.W)
        else:
            add_ship_button.grid(row=0, column=0, padx=x_padding, sticky=tk.W)
    if not len(bioscan_globals.ship_whitelist):
        clear_ships_button['state'] = tk.DISABLED
    clear_ships_button.grid(row=0, column=1, padx=x_padding, sticky=tk.W)

    anchor_frame = tk.Frame(frame)
    anchor_frame.grid(row=0, column=1, sticky=tk.NSEW)
    anchor_frame.columnconfigure(4, weight=1)
    summary_frame = tk.Frame(frame)
    summary_frame.grid(row=1, column=1, sticky=tk.NSEW)
    summary_frame.columnconfigure(4, weight=1)
    details_frame = tk.Frame(frame)
    details_frame.grid(row=2, column=1, sticky=tk.NSEW)
    details_frame.columnconfigure(4, weight=1)

    nb.Label(anchor_frame, text='Prediction Details Anchor:') \
        .grid(row=0, column=0, sticky=tk.W)
    nb.Label(anchor_frame, text='X') \
        .grid(row=0, column=1, sticky=tk.W)
    nb.EntryMenu(
        anchor_frame, text=bioscan_globals.overlay_anchor_x.get(), textvariable=bioscan_globals.overlay_anchor_x,
        width=8, validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=2, sticky=tk.W)
    nb.Label(anchor_frame, text='Y') \
        .grid(row=0, column=3, sticky=tk.W)
    nb.EntryMenu(
        anchor_frame, text=bioscan_globals.overlay_anchor_y.get(), textvariable=bioscan_globals.overlay_anchor_y,
        width=8, validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=4, sticky=tk.W)

    nb.Label(summary_frame, text='Summary / Progress Anchor:') \
        .grid(row=0, column=0, sticky=tk.W)
    nb.Label(summary_frame, text='X') \
        .grid(row=0, column=1, sticky=tk.W)
    nb.EntryMenu(
        summary_frame, text=bioscan_globals.overlay_summary_x.get(), textvariable=bioscan_globals.overlay_summary_x,
        width=8, validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=2, sticky=tk.W)
    nb.Label(summary_frame, text='Y') \
        .grid(row=0, column=3, sticky=tk.W)
    nb.EntryMenu(
        summary_frame, text=bioscan_globals.overlay_summary_y.get(), textvariable=bioscan_globals.overlay_summary_y,
        width=8, validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=4, sticky=tk.W)

    nb.Checkbutton(
        details_frame,
        text='Scroll details',
        variable=bioscan_globals.overlay_detail_scroll
    ).grid(row=0, column=0, padx=x_padding, sticky=tk.NW)
    nb.Label(details_frame, text='Maximum details length:') \
        .grid(row=0, column=1, sticky=tk.W)
    nb.EntryMenu(
        details_frame, text=bioscan_globals.overlay_detail_length.get(), textvariable=bioscan_globals.overlay_detail_length,
        width=8, validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=2, sticky=tk.W)
    nb.Label(details_frame, text='Scroll delay (sec):') \
        .grid(row=0, column=3, sticky=tk.W)
    nb.EntryMenu(
        details_frame, text=bioscan_globals.overlay_detail_delay.get(), textvariable=bioscan_globals.overlay_detail_delay,
        width=8, validate='all', validatecommand=(frame.register(is_double), '%P', '%d')
    ).grid(row=0, column=4, sticky=tk.W)
    return frame


def get_ship_names(bioscan_globals: Globals) -> list[str]:
    """
    Process and return sorted array of overlay whitelist ship names

    :param bioscan_globals: BioScan globals storage class
    :return: Sorted array of ship names
    """

    ships: list[str] = []
    for ship in bioscan_globals.ship_whitelist:
        ship_data = ship.split(':')
        ships.append(ship_data[-1])
    return sorted(ships)


def ship_in_whitelist(ship_id: int, name: str, bioscan_globals: Globals) -> bool:
    """
    Check if the specified ship ID and / or name is in the overlay whitelist

    :param ship_id: The ship ID
    :param name: The ship name (custom or default)
    :param bioscan_globals: BioScan globals storage class
    :return: Whether or not ship is in the overlay whitelist
    """

    if f'{ship_id}:{name}' in bioscan_globals.ship_whitelist:
        return True
    if name and name in bioscan_globals.ship_whitelist:
        return True
    return False


def change_ship_name(ship_id: int, name: str, bioscan_globals: Globals) -> None:
    """
    Change the stored ship name in EDMC storage assigned to the given ship ID

    :param ship_id: The ship ID
    :param name: The ship name (custom or default)
    :param bioscan_globals: BioScan globals storage class
    """

    for ship in bioscan_globals.ship_whitelist:
        if ship.startswith(f'{ship_id}:'):
            bioscan_globals.ship_whitelist.append(f'{ship_id}:{name}')
            bioscan_globals.ship_whitelist.remove(ship)
            break


def ship_sold(ship_id: int, bioscan_globals) -> None:
    """
    Remove sold ship from overlay whitelist

    :param ship_id: The ship ID
    :param bioscan_globals: BioScan globals storage class
    """

    for ship in bioscan_globals.ship_whitelist:
        if ship.startswith(ship_id):
            bioscan_globals.ship_whitelist.remove(ship)
            return


def add_ship_id(ship_id: int, name: str, bioscan_globals: Globals) -> None:
    """
    Convert old name-based storage to ID:name if ship name is in the overlay whitelist

    :param ship_id: The ship ID
    :param name: The ship name (custom or default)
    :param bioscan_globals: BioScan globals storage class
    """

    if name in bioscan_globals.ship_whitelist:
        bioscan_globals.ship_whitelist.remove(name)
        bioscan_globals.ship_whitelist.append(f'{ship_id}:{name}')


def sync_ship_name(ship_id: int, name: str, bioscan_globals: Globals) -> None:
    """
    Update the ship name in the overlay whitelist on change

    :param ship_id: The ship ID
    :param name: The ship name (custom or default)
    :param bioscan_globals: BioScan globals storage class
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
