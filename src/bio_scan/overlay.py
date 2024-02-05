import threading
from typing import Callable

from EDMCLogging import get_plugin_logger
from bio_scan import const

try:
    from EDMCOverlay import edmcoverlay
except ImportError:
    edmcoverlay = None

logger = get_plugin_logger(const.name)


def setInterval(interval: float) -> Callable:
    """
    Decorator which automatically repeats the function at a given interval.

    :param interval: Interval in seconds
    """
    def decorator(function: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> threading.Event:
            stopped = threading.Event()

            def loop() -> None:  # executed in another thread
                while not stopped.wait(interval):  # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True  # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator


class Overlay:
    """
    An interface for displaying multiple text blocks with EDMCOverlay. Breaks multi-line text into
    multiple individual lines to work around EDMCOverlay limitations. Redraws the text every 5 minutes in order to
    display text indefinitely.
    """

    def __init__(self):
        if edmcoverlay:
            self._overlay: edmcoverlay.Overlay | None = edmcoverlay.Overlay()
        else:
            self._overlay: edmcoverlay.Overlay | None = None
        self._text_blocks: dict[str, tuple[int, int, str, str, list[str]]] = {}
        self._redraw_timer = self.redraw()

    def disconnect(self) -> None:
        self._redraw_timer.set()
        self._overlay.send_raw({
            "command": "exit"
        })

    def display(self, message_id: str, text: str, x: int = 0, y: int = 0,
                color: str = "#ffffff", size: str = "normal") -> None:
        """
        Displays text with given attributes. Saves text in cache to allow for redraw and clearing.
        Expires after 60 seconds.

        :param message_id: Unique identifier for a given text block.
        :param text: Message to display.
        :param x: X coordinate
        :param y: Y coordinate
        :param color: Accepts "red", "green", "blue", and hex "#ffffff"
        :param size: Accepts "normal" and "large"
        """
        if message_id in self._text_blocks:
            self.clear(message_id)
        self._text_blocks[message_id] = (
            x, y, color, size,
            text.replace('🗸', '√').replace('\N{memo}', '♦').split("\n")
        )
        try:
            count = 0
            spacer = 14 if size == "normal" else 24
            for message in self._text_blocks[message_id][4]:
                self._overlay.send_message("{}_{}".format(message_id, count), message, color,
                                           x, y + (spacer * count), ttl=60, size=size)
                count += 1
        except Exception as err:
            logger.debug(err)

    def clear(self, message_id) -> None:
        """
        Clears a given text block identified by a unique message ID.

        :param message_id: Unique ID of text to clear.
        """
        try:
            if message_id in self._text_blocks:
                count = 0
                for _ in self._text_blocks[message_id][4]:
                    self._overlay.send_message("{}_{}".format(message_id, count),
                                               "", "#ffffff", 0, 0, ttl=1)
                    count += 1
                self._text_blocks.pop(message_id, None)
        except Exception as err:
            logger.debug(err)

    @setInterval(30)
    def redraw(self):
        """
        Redraws all cached text blocks on a 30-second interval.
        :rtype: threading.Event
        """

        if self.available():
            for message_id, message_info in self._text_blocks.items():
                x, y, color, size, messages = message_info
                count = 0
                spacer = 14 if size == "normal" else 24
                for message in messages:
                    try:
                        self._overlay.send_message("{}_{}".format(message_id, count), message, color,
                                                   x, y + (spacer * count), 60, size)
                    except Exception as err:
                        logger.debug(err)
                    count += 1

    def available(self) -> bool:
        """
        Get availability of EDMCOverlay interface

        :return: Availability of EDMCOverlay
        """
        if self._overlay:
            return True
        else:
            if edmcoverlay:
                self._overlay = edmcoverlay.Overlay()
                return True
        return False
