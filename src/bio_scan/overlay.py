import sys
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


class TextBlock:
    def __init__(self, text: list[str], x: int, y: int, size: str, color: str,
                 scrolled: bool = False, limit: int = 0, delay: float = 10):
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.scrolled = scrolled
        self.limit = limit
        self.delay = delay
        self.direction = 'down'
        self.offset = 0
        self.timer = threading.Timer(self.delay, lambda *args: None)
        if scrolled:
            self.timer.start()


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
        self._text_blocks: dict[str, TextBlock] = {}
        self._redraw_timer = self.redraw()
        self._scroll_timer = self.scroll()

    def disconnect(self) -> None:
        self._redraw_timer.set()
        self._scroll_timer.set()
        self._overlay.send_raw({
            "command": "exit"
        })

    def display(self, message_id: str, text: str, x: int = 0, y: int = 0, color: str = "#ffffff", size: str = "normal",
                scrolled: bool = False, limit: int = 0, delay: float = 10) -> None:
        """
        Displays text with given attributes. Saves text in cache to allow for redraw and clearing.
        Expires after 60 seconds.

        :param message_id: Unique identifier for a given text block.
        :param text: Message to display.
        :param x: X coordinate
        :param y: Y coordinate
        :param color: Accepts "red", "green", "blue", and hex "#ffffff"
        :param size: Accepts "normal" and "large"
        :param scrolled: Toggle for scrolled text panel
        :param limit: Line limit for display; 0 is no limit
        :param delay: Time between up/down scroll of scrolled text
        """

        if sys.platform == 'linux':
            formatted_text = text.replace('🗸', '*').replace('\N{memo}', '»').split("\n")
        else:
            formatted_text = text.replace('🗸', '√').replace('\N{memo}', '♦').split("\n")
        if not scrolled:
            self.clear(message_id, False)
        elif message_id in self._text_blocks and len(formatted_text) < len(self._text_blocks[message_id].text):
            self.clear(message_id, len(formatted_text), False)
        self._text_blocks[message_id] = TextBlock(
            text=formatted_text, x=x, y=y, size=size, color=color, scrolled=scrolled, limit=limit, delay=delay
        )
        if not scrolled:
            self.draw(message_id)

    def clear(self, message_id: str, from_line: int = 0, remove: bool = True) -> None:
        """
        Clears a given text block identified by a unique message ID.

        :param message_id: Unique ID of text to clear.
        :param from_line: Start point of clear
        :param remove: Remove the message from the cache.
        """
        try:
            if message_id in self._text_blocks:
                count = from_line
                while (count < len(self._text_blocks[message_id].text) or
                       (self._text_blocks[message_id].limit > 0 and count < self._text_blocks[message_id].limit)):
                    self._overlay.send_message("{}_{}".format(message_id, count),
                                               "", "#ffffff", 0, 0, ttl=1)
                    count += 1
                if remove:
                    self._text_blocks.pop(message_id, None)
        except Exception as ex:
            logger.debug("Exception during overlay clear", exc_info=ex)

    @setInterval(30)
    def redraw(self):
        """
        Redraws all cached text blocks on a 30-second interval.
        :rtype: threading.Event
        """

        if self.available():
            for message_id, message_info in self._text_blocks.copy().items():
                if message_info.scrolled:
                    continue
                self.draw(message_id)

    @setInterval(.75)
    def scroll(self):
        """
        Redraw scrolled displays based on given lines.
        :rtype: threading.Event
        """

        if self.available():
            try:
                for message_id, message_info in self._text_blocks.copy().items():
                    if not message_info.scrolled:
                        continue

                    if not message_info.timer.is_alive():
                        self.draw(message_id)
                        if message_info.limit != 0 and message_info.limit < len(message_info.text):
                            offset = message_info.offset + 1 if message_info.direction == "down" else \
                                len(message_info.text) - message_info.offset
                            display = offset + message_info.limit if message_info.direction == "down" else offset
                            if display >= len(message_info.text):
                                self._text_blocks[message_id].direction = "up" if message_info.direction == "down" \
                                    else "down"
                                self._text_blocks[message_id].timer = threading.Timer(message_info.delay,
                                                                                      lambda *args: None)
                                self._text_blocks[message_id].timer.start()
                            if self._text_blocks[message_id].direction == "down":
                                self._text_blocks[message_id].offset += 1
                            else:
                                self._text_blocks[message_id].offset -= 1
                    elif message_info.limit != 0 and message_info.limit > len(message_info.text):
                        self.draw(message_id)
            except Exception as ex:
                logger.debug("Exception during scroll repaint", exc_info=ex)

    def draw(self, message_id: str):
        if message_id in self._text_blocks:
            block = self._text_blocks[message_id]
            count = block.offset
            line_count = 0
            spacer = 14 if block.size == "normal" else 24
            while (block.limit == 0 or count - block.offset < block.limit) and count < len(block.text):
                try:
                    self._overlay.send_message("{}_{}".format(message_id, line_count), block.text[count], block.color,
                                               block.x, block.y + (spacer * (count - block.offset)),
                                               ttl=60, size=block.size)
                except AttributeError:
                    count -= 1
                    self._overlay.connect()
                except Exception as ex:
                    logger.debug("Exception during draw", exc_info=ex)
                count += 1
                line_count += 1

    def available(self) -> bool:
        """
        Get availability of EDMCOverlay interface

        :return: Availability of EDMCOverlay
        """
        if self._overlay is not None:
            if hasattr(self._overlay, 'connection'):
                if self._overlay.connection is None:
                    self._overlay = edmcoverlay.Overlay()
            return True
        else:
            if edmcoverlay:
                self._overlay = edmcoverlay.Overlay()
                return True
        return False
