import semantic_version

# TKinter imports
import tkinter as tk
from tkinter import colorchooser as tkColorChooser  # type: ignore # noqa: N812
from tkinter import ttk

# Local imports
import bio_scan.const
from bio_scan.globals import Globals

# Database objects
from ExploData.explo_data import db
import ExploData.explo_data.journal_parse
from ExploData.explo_data.journal_parse import parse_journals

# EDMC imports
import myNotebook as nb
from ttkHyperlinkLabel import HyperlinkLabel


def get_settings(parent: ttk.Notebook, bioscan_globals: Globals) -> tk.Frame:

    """
    EDMC settings pane hook.
    Build settings display and hook in settings properties.

    :param parent: EDMC parent settings pane TKinter frame
    :param bioscan_globals: Plugin globals
    :return: Plugin settings tab TKinter frame
    """

    x_padding = 10
    x_button_padding = 12
    y_padding = 2
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
    frame = nb.Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(20, weight=1)

    x_padding = 10
    x_button_padding = 12
    y_padding = 2
    frame = nb.Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(8, weight=1)

    # Left column
    nb.Label(
        frame,
        text='Focus Body Signals:',
    ).grid(row=1, padx=x_padding, sticky=tk.W)
    focus_options = [
        'Never',
        'On Approach',
        'Near Surface',
        'On Surface',
    ]
    nb.OptionMenu(
        frame,
        bioscan_globals.focus_setting,
        bioscan_globals.focus_setting.get(),
        *focus_options
    ).grid(row=2, padx=x_padding, pady=y_padding, column=0, sticky=tk.W)
    nb.Label(frame,
             text='Never: Never filter signal details\n'
                  'On Approach: Show only local signals on approach\n'
                  'Near Surface: Show signals under given altitude (see below)\n'
                  'On Surface: Show only local signals when on surface',
             justify=tk.LEFT) \
        .grid(row=3, padx=x_padding, column=0, sticky=tk.NW)
    nb.Label(frame, text='Altitude (in meters) for "Near Surface":') \
        .grid(row=4, column=0, padx=x_padding, sticky=tk.SW)
    nb.Entry(
        frame, text=bioscan_globals.focus_distance.get(), textvariable=bioscan_globals.focus_distance,
        validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=5, column=0, padx=x_padding, sticky=tk.NW)
    nb.Checkbutton(
        frame,
        text='Show complete breakdown of genera with multiple matches',
        variable=bioscan_globals.focus_breakdown
    ).grid(row=6, column=0, padx=x_button_padding, sticky=tk.W)

    # Right column
    nb.Label(
        frame,
        text='Display Signal Summary:'
    ).grid(row=1, column=1, sticky=tk.W)
    signal_options = [
        'Always',
        'In Flight',
    ]
    nb.OptionMenu(
        frame,
        bioscan_globals.signal_setting,
        bioscan_globals.signal_setting.get(),
        *signal_options
    ).grid(row=2, column=1, pady=y_padding, sticky=tk.W)
    nb.Label(frame,
             text='Always: Always display the body signal summary\n'
                  'In Flight: Show the signal summary in flight only',
             justify=tk.LEFT) \
        .grid(row=3, column=1, sticky=tk.NW)
    nb.Checkbutton(
        frame,
        text='Enable species waypoints with the comp. scanner',
        variable=bioscan_globals.waypoints_enabled
    ).grid(row=4, column=1, padx=x_button_padding, sticky=tk.W)
    nb.Label(
        frame,
        text='Completed Scan Display:'
    ).grid(row=6, column=1, sticky=tk.W)
    scan_options = [
        'Check',
        'Hide',
        'Hide in System'
    ]
    nb.OptionMenu(
        frame,
        bioscan_globals.scan_display_mode,
        bioscan_globals.scan_display_mode.get(),
        *scan_options
    ).grid(row=7, column=1, sticky=tk.W)
    nb.Label(frame,
             text='Check: Always show species with a checkmark when complete\n'
                  'Hide: Always hide completed species\n'
                  'Hide in System: Hide completed species in the full system view',
             justify=tk.LEFT) \
        .grid(row=8, column=1, sticky=tk.NW)

    return frame


def get_overlay_tab(parent: ttk.Notebook, bioscan_globals: Globals) -> tk.Frame:
    color_button = None

    def color_chooser() -> None:
        (_, color) = tkColorChooser.askcolor(
            bioscan_globals.overlay_color.get(), title='Overlay Color', parent=bioscan_globals.parent
        )

        if color:
            bioscan_globals.overlay_color.set(color)
            if color_button is not None:
                color_button['foreground'] = color

    frame = nb.Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)

    x_padding = 10
    x_button_padding = 12
    y_padding = 2
    frame = nb.Frame(parent)

    nb.Label(frame,
             text='EDMC Overlay Integration',
             justify=tk.LEFT) \
        .grid(row=0, column=0, padx=x_padding, sticky=tk.NW)
    nb.Checkbutton(
        frame,
        text='Enable overlay',
        variable=bioscan_globals.use_overlay
    ).grid(row=1, column=0, padx=x_button_padding, pady=0, sticky=tk.W)
    color_button = nb.ColoredButton(
        frame,
        text='Text Color',
        foreground=bioscan_globals.overlay_color.get(),
        background='grey4',
        command=lambda: color_chooser()
    ).grid(row=2, column=0, padx=x_button_padding, pady=y_padding, sticky=tk.W)

    anchor_frame = nb.Frame(frame)
    anchor_frame.grid(row=0, column=1, sticky=tk.NSEW)
    anchor_frame.columnconfigure(4, weight=1)
    summary_frame = nb.Frame(frame)
    summary_frame.grid(row=1, column=1, sticky=tk.NSEW)
    summary_frame.columnconfigure(4, weight=1)
    details_frame = nb.Frame(frame)
    details_frame.grid(row=2, column=1, sticky=tk.NSEW)
    details_frame.columnconfigure(4, weight=1)

    nb.Label(anchor_frame, text='Prediction Details Anchor:') \
        .grid(row=0, column=0, sticky=tk.W)
    nb.Label(anchor_frame, text='X') \
        .grid(row=0, column=1, sticky=tk.W)
    nb.Entry(
        anchor_frame, text=bioscan_globals.overlay_anchor_x.get(), textvariable=bioscan_globals.overlay_anchor_x,
        width=8, validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=2, sticky=tk.W)
    nb.Label(anchor_frame, text='Y') \
        .grid(row=0, column=3, sticky=tk.W)
    nb.Entry(
        anchor_frame, text=bioscan_globals.overlay_anchor_y.get(), textvariable=bioscan_globals.overlay_anchor_y,
        width=8, validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=4, sticky=tk.W)

    nb.Label(summary_frame, text='Summary / Progress Anchor:') \
        .grid(row=0, column=0, sticky=tk.W)
    nb.Label(summary_frame, text='X') \
        .grid(row=0, column=1, sticky=tk.W)
    nb.Entry(
        summary_frame, text=bioscan_globals.overlay_summary_x.get(), textvariable=bioscan_globals.overlay_summary_x,
        width=8, validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=2, sticky=tk.W)
    nb.Label(summary_frame, text='Y') \
        .grid(row=0, column=3, sticky=tk.W)
    nb.Entry(
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
    nb.Entry(
        details_frame, text=bioscan_globals.overlay_detail_length.get(), textvariable=bioscan_globals.overlay_detail_length,
        width=8, validate='all', validatecommand=(frame.register(is_digit), '%P', '%d')
    ).grid(row=0, column=2, sticky=tk.W)
    nb.Label(details_frame, text='Scroll delay (sec):') \
        .grid(row=0, column=3, sticky=tk.W)
    nb.Entry(
        details_frame, text=bioscan_globals.overlay_detail_delay.get(), textvariable=bioscan_globals.overlay_detail_delay,
        width=8, validate='all', validatecommand=(frame.register(is_double), '%P', '%d')
    ).grid(row=0, column=4, sticky=tk.W)
    return frame


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
