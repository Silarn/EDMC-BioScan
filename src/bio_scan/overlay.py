from EDMCLogging import get_plugin_logger
from bio_scan import const

try:
    from EDMCOverlay import edmcoverlay
except ImportError:
    edmcoverlay = None


class This:
    """Holds module globals."""

    def __init__(self):
        if edmcoverlay:
            self.overlay = edmcoverlay.Overlay()
        else:
            self.overlay = None


this = This()
logger = get_plugin_logger(const.name)


def disconnect() -> None:
    this.overlay.send_raw({
        "command": "exit"
    })


def display(message_id, text, x=10, y=8, color="#ffffff", size="normal"):
    try:
        this.overlay.send_message(message_id, text, color, x, y, ttl=600, size=size)
    except Exception as err:
        logger.debug(err)


def overlay_enabled() -> bool:
    if this.overlay:
        return True
    else:
        if edmcoverlay:
            this.overlay = edmcoverlay.Overlay()
            return True
    return False
