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
        self.text_blocks: dict[str, list[str]] = {}


this = This()
logger = get_plugin_logger(const.name)


def disconnect() -> None:
    this.overlay.send_raw({
        "command": "exit"
    })


def display(message_id: str, text: str, x: int = 0, y: int = 0, color: str = "#ffffff", size: str = "normal"):
    if message_id in this.text_blocks:
        clear(message_id)
    this.text_blocks[message_id] = text.replace('🗸', '√').replace('\N{memo}', '♦').split("\n")
    try:
        count = 0
        spacer = 14 if size == "normal" else 24
        for message in this.text_blocks[message_id]:
            this.overlay.send_message("{}_{}".format(message_id, count), message, color, x, y + (spacer * count), ttl=600, size=size)
            count += 1
    except Exception as err:
        logger.debug(err)


def clear(message_id):
    try:
        if message_id in this.text_blocks:
            count = 0
            for _ in this.text_blocks[message_id]:
                this.overlay.send_message("{}_{}".format(message_id, count), "", "#ffffff", 0, 0, ttl=1)
                count += 1
            this.text_blocks.pop(message_id, None)
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
