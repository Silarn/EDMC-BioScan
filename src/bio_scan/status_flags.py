from enum import Flag, auto


class StatusFlags(Flag):
    """
    Enum definition for Elite Dangerous Status.json flags (group 1)
    """

    DOCKED = auto()
    LANDED = auto()
    LANDING_GEAR = auto()
    SHIELDS_UP = auto()
    SUPERCRUISE = auto()
    FA_OFF = auto()
    HARDPOINTS = auto()
    IN_WING = auto()
    LIGHTS = auto()
    CARGO_SCOOP = auto()
    SILENT = auto()
    FUEL_SCOOP = auto()
    HANDBREAK = auto()
    SRV_USING_TURRET = auto()
    SRV_TURRET_BLOCKED = auto()
    SRV_DRIVE_ASSIST_ON = auto()
    MASS_LOCKED = auto()
    FSD_CHARGING = auto()
    FSD_COOLDOWN = auto()
    LOW_FUEL = auto()
    OVERHEAT = auto()
    HAVE_LATLONG = auto()
    DANGER = auto()
    INTERDICTED = auto()
    IN_SHIP = auto()
    IN_FIGHTER = auto()
    IN_SRV = auto()
    IS_ANALYSIS_MODE = auto()
    NIGHT_VISION = auto()
    HAVE_ALTITUDE = auto()
    FSD_JUMP_IN_PROGRESS = auto()
    SRV_HIGHBEAM = auto()


class StatusFlags2(Flag):
    """
    Enum definition for Elite Dangerous Status.json flags (group 2)
    """

    ON_FOOT = auto()
    IN_TAXI = auto()
    MULTICREW = auto()
    STATION_ON_FOOT = auto()
    PLANET_ON_FOOT = auto()
    AIM_DOWN_SIGHT = auto()
    LOW_OXYGEN = auto()
    LOW_HEALTH = auto()
    COLD = auto()
    HOT = auto()
    VERY_COLD = auto()
    VERY_HOT = auto()
    GLIDING = auto()
    HANGAR_ON_FOOT = auto()
    SOCIAL_ON_FOOT = auto()
    EXTERIOR_ON_FOOT = auto()
    BREATHABLE = auto()
    MULTICREW_TELEPRESENCE = auto()
    MULTICREW_PHYSICAL = auto()
    SUPERCHARGING_FSD = auto()