import semantic_version

# TKinter imports
import tkinter as tk
from tkinter import ttk

# Database objects
from sqlalchemy.orm import Session

from ExploData.explo_data.db import Commander, System
from ExploData.explo_data.body_data.struct import PlanetData, StarData

# Local imports
import bio_scan.const
import bio_scan.overlay as overlay

# EDMC imports
from ttkHyperlinkLabel import HyperlinkLabel

class Globals:
    """Holds module globals."""

    def __init__(self):
        self.formatter = None
        self.translation_context = ''
        self.started = False

        self.VERSION = semantic_version.Version(bio_scan.const.version)
        self.NAME = bio_scan.const.name

        # Settings vars
        # General
        self.credits_setting: tk.BooleanVar | None = None
        self.focus_setting: tk.StringVar | None = None
        self.signal_setting: tk.StringVar | None = None
        self.focus_breakdown: tk.BooleanVar | None = None
        self.scan_display_mode: tk.StringVar | None = None
        self.hide_body_complete: tk.BooleanVar | None = None
        self.waypoints_enabled: tk.BooleanVar | None = None
        self.hide_waypoint_bearings: tk.BooleanVar | None = None
        self.exclude_signals: tk.BooleanVar | None = None
        self.minimum_signals: tk.IntVar | None = None
        self.debug_logging_enabled: tk.BooleanVar | None = None
        self.focus_distance: tk.IntVar | None = None
        self.box_height: tk.IntVar | None = None
        # Overlay
        self.use_overlay: tk.BooleanVar | None = None
        self.overlay_color: tk.StringVar | None = None
        self.overlay_anchor_x: tk.IntVar | None = None
        self.overlay_anchor_y: tk.IntVar | None = None
        self.overlay_summary_x: tk.IntVar | None = None
        self.overlay_summary_y: tk.IntVar | None = None
        self.overlay_detail_scroll: tk.BooleanVar | None = None
        self.overlay_detail_length: tk.IntVar | None = None
        self.overlay_detail_delay: tk.DoubleVar | None = None
        self.overlay_line_spacing_normal: tk.IntVar | None = None
        self.overlay_line_spacing_large: tk.IntVar | None = None
        ## Radar
        self.radar_enabled: tk.BooleanVar | None = None
        self.radar_ship_loc_enabled: tk.BooleanVar | None = None
        self.radar_anchor_x: tk.IntVar | None = None
        self.radar_anchor_y: tk.IntVar | None = None
        self.radar_radius: tk.IntVar | None = None
        self.radar_max_distance: tk.IntVar | None = None
        self.radar_use_log: tk.BooleanVar | None = None
        ## Whitelist
        self.ship_whitelist: list[str] = []

        # GUI Objects
        self.parent: tk.Frame | None = None
        self.frame: tk.Frame | None = None
        self.scroll_canvas: tk.Canvas | None = None
        self.scrollbar: ttk.Scrollbar | None = None
        self.scrollable_frame: ttk.Frame | None = None
        self.label: tk.Label | None = None
        self.view_button: tk.Button | None = None
        self.values_label: tk.Label | None = None
        self.total_label: tk.Label | None = None
        self.edsm_button: tk.Label | None = None
        self.update_button: HyperlinkLabel | None = None
        self.journal_label: tk.Label | None = None
        self.overlay: overlay.Overlay = overlay.Overlay()
        self.display_hidden: bool = False

        # Plugin state data
        # DB elements
        self.commander: Commander | None = None
        self.planets: dict[str, PlanetData] = {}
        self.stars: dict[str, StarData] = {}
        self.planet_cache: dict[
            str, dict[str, tuple[bool, tuple[str, int, int, list[tuple[str, list[str], int]]]]]] = {}
        self.migration_failed: bool = False
        self.db_mismatch: bool = False
        self.sql_session: Session | None = None
        # System info
        self.system: System | None = None
        self.main_star_type: str = ''
        self.main_star_luminosity: str = ''
        self.location_name: str = ''
        self.location_id: str = ''
        self.location_state: str = ''
        # Body info
        self.ship_location: tuple[float, float] | None = None
        self.planet_radius: float = 0.0
        self.planet_latitude: float | None = None
        self.planet_longitude: float | None = None
        self.planet_altitude: float = 10000.0
        self.planet_heading: int | None = None
        # Ship / player status
        self.docked: bool = False
        self.on_foot: bool = False
        self.suit_name: str = ''
        self.analysis_mode: bool = True
        self.at_nav_beacon: bool = False
        self.in_supercruise: bool = False
        self.mode_changed: bool = False
        self.current_scan: tuple[str, str] = ('', '')
        self.gui_focus: int = 0

        # EDSM vars
        self.fetched_edsm = False

        # EDDMC compat
        self.edd_replay: bool = False

bioscan_globals = Globals()