import math
import sys
import threading
from os import environ
from typing import Callable, Self

from EDMCLogging import get_plugin_logger
from bio_scan import const

try:
    from EDMCOverlay import edmcoverlay
except ImportError:
    try:
        from edmcoverlay import edmcoverlay
    except ImportError:
        edmcoverlay = None

logger = get_plugin_logger(const.name)

VIRTUAL_WIDTH = 1280.0
VIRTUAL_HEIGHT = 1024.0
VIRTUAL_ORIGIN_X = 20.0
VIRTUAL_ORIGIN_Y = 40.0

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


def round_away(val):
    val += -0.5 if val < 0 else 0.5
    return int(val)


class TextBlock:
    """
    Cache class for a multi-line text block on the overlay.

    These can be configured to auto-scroll beyond a certain length, with a given delay before scrolling
    the opposite direction.
    """
    def __init__(self, text: list[str], x: int, y: int, size: str, color: str,
                 scrolled: bool = False, limit: int = 0, delay: float = 10):
        """
        Constructor.

        :param text: List of strings to display
        :param x: X coordinate for upper left corner
        :param y: Y coordinate for upper left corner
        :param size: Text size (normal or large)
        :param color: Text color (#aarrggbb, #rrggbb, red, green, blue, yellow, white, black)
        :param scrolled: Whether to scroll the text display (default: False)
        :param limit: Maximum line length of display, for use with 'scrolled' (default: 0)
        :param delay: Time to wait before scrolling the opposite direction when reaching the
         end of the text (default 10)
        """

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


class RadarSet:
    """
    Cache class for a radar display.

    Contains circles and marker positions with a given position and radius. Can be set to display
    linearly or logarithmically.
    """
    def __init__(self, markers: list[dict], circles: list[dict], x: int, y: int, r: int, d: int, north: float, log: bool):
        """
        Constructor.

        :param markers: List of marker data. Should contain a dict of 'distance', 'bearing', 'color', and 'genus'.
        :param circles: List of circle data. Should contain a dict of 'radius', 'color' and optionally 'text'.
        :param x: X coordinate for upper left corner
        :param y: Y coordinate for upper left corner
        :param r: Radius of circle
        :param d: Maximum distance tracked by radar (at r)
        :param log: Whether to display a logarithmic distance scale
        """

        self.markers: list[dict] = markers
        self.circles: list[dict] = circles
        self.x = x
        self.y = y
        self.r = r
        self.d = d
        self.north = north
        self.log = log


class Overlay:
    """
    An interface for displaying multiple text blocks with EDMCOverlay. Breaks multi-line text into
    multiple individual lines to work around EDMCOverlay limitations. Redraws the text every 5 minutes in order to
    display text indefinitely.
    """

    def __init__(self):
        if edmcoverlay:
            self._overlay: edmcoverlay.Overlay | None = edmcoverlay.Overlay()
            if hasattr(self._overlay, 'connection'):
                self._overlay_type = 'EDMCOverlay'
            elif hasattr(self._overlay, '_emit_payload'):
                self._overlay_type = 'modern_overlay'
            elif hasattr(self._overlay, 'connect') and not hasattr(self._overlay, 'server'):
                self._overlay_type = 'edmcoverlay_for_linux'
            else:
                if environ.get('XDG_SESSION_TYPE', 'X11') == 'wayland' and hasattr(self._overlay, 'server'):
                    self._overlay_type = 'edmcoverlay2_wayland'
                else:
                    self._overlay_type = 'edmcoverlay2'
        else:
            self._overlay_type = "none"
            self._overlay: edmcoverlay.Overlay | None = None
        self._normal_spacer: int = 16
        self._large_spacer: int = 26
        self._text_blocks: dict[str, TextBlock] = {}
        self._markers: dict[str, RadarSet] = {}
        self._redraw_timer = self.redraw()
        self._redraw_radar_timer = self.redraw_radar()
        self._scroll_timer = self.scroll()
        self._screen_width = 1920
        self._screen_height = 1080
        self._over_aspect_x = self._calc_aspect_x()

    def set_screen_dimensions(self, w: int, h: int) -> Self:
        """
        Sets screen dimensions for use in pixel ratio scaling.

        :param w: Width.
        :param h: Height.
        :return: Returns self.
        """

        self._screen_width = w
        self._screen_height = h
        self._over_aspect_x = self._calc_aspect_x()
        return self

    def set_line_spacing(self, normal: int, large: int) -> Self:
        """
        Sets line spacing for text displays.

        :param normal: Normal text size spacing
        :param large: Large text size spacing
        :return: Returns self.
        """

        self._normal_spacer = normal
        self._large_spacer = large
        return self

    def disconnect(self) -> None:
        """
        Shut down overlay draw timers
        """

        self._redraw_timer.set()
        self._redraw_radar_timer.set()
        self._scroll_timer.set()

    def _calc_aspect_x(self) -> float:
        if self._overlay_type == 'EDMCOverlay':
            return (VIRTUAL_WIDTH+32) / (VIRTUAL_HEIGHT+18) * (self._screen_height-2*VIRTUAL_ORIGIN_Y) / (self._screen_width-2*VIRTUAL_ORIGIN_X)
        elif self._overlay_type == 'modern_overlay':
            return 1
        else:
            return (VIRTUAL_WIDTH / VIRTUAL_HEIGHT) * (self._screen_height / self._screen_width)

    def _aspect_x(self, x: float) -> int:
        if self._overlay_type in ['EDMCOverlay', 'edmcoverlay2']:
            return round_away(self._over_aspect_x * x)
        return int(x)

    def _aspect_y(self, y: float) -> int:
        if self._overlay_type == 'edmcoverlay2_wayland':
            return int(y + 20)
        return int(y)

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

        if sys.platform == 'linux' and self._overlay_type in ['edmcoverlay2', 'edmcoverlay_for_linux']:
            formatted_text = (text.replace('\N{HEAVY CHECK MARK}\N{VARIATION SELECTOR-16}', '*').replace('\N{memo}', '»')
                              .replace(' ', ' ').split('\n'))
        elif self._overlay_type == 'EDMCOverlay':
            formatted_text = text.replace('\N{HEAVY CHECK MARK}\N{VARIATION SELECTOR-16}', '√').replace('\N{memo}', '♦').split('\n')
        else:
            formatted_text = text.split('\n')
        if message_id in self._text_blocks and len(formatted_text) < len(self._text_blocks[message_id].text):
            self.clear(message_id, len(formatted_text)-1, False)
        self._text_blocks[message_id] = TextBlock(
            text=formatted_text, x=x, y=y, size=size, color=color, scrolled=scrolled, limit=limit, delay=delay
        )
        self.draw(message_id)

    def clear(self, message_id: str, new_length: int = 0, remove: bool = True) -> None:
        """
        Clears a given text block identified by a unique message ID.

        :param message_id: Unique ID of text to clear.
        :param new_length: Start point of clear
        :param remove: Remove the message from the cache.
        """

        try:
            if message_id in self._text_blocks:
                last_len = self._text_blocks[message_id].limit if self._text_blocks[message_id].limit else len(self._text_blocks[message_id].text)
                last_len = min(len(self._text_blocks[message_id].text), last_len)
                if new_length:
                    if new_length < last_len:
                        for item in range(new_length, last_len):
                            self._overlay.send_raw({'id': f'{message_id}_{item}', 'text': '', 'ttl': 0})
                else:
                    for item in range(last_len):
                        self._overlay.send_raw({'id': f'{message_id}_{item}', 'text': '', 'ttl': 0})
                if remove:
                    self._text_blocks.pop(message_id, None)
        except Exception as ex:
            logger.debug("Exception during overlay clear", exc_info=ex)

    def render_radar(self, message_id: str, x: int, y: int, r: int, d: int, north: float,
                     markers: list | None = None, circles: list | None = None, logarithmic: bool = False) -> None:
        """
        Render radar display, cached to refresh on a timer.

        :param message_id: ID of radar group, used to update or clear existing radar display
        :param x: Center x coordinate of radar
        :param y: Center y coordinate of radar
        :param r: Radius of radar
        :param d: Max distance of radar display
        :param north: Bearing toward 'north'
        :param markers: List of markers as a dict of 'distance', 'bearing', and 'genus'
        :param circles: List of circles to draw as a dict of 'radius' and 'color'
        :param logarithmic: Make radar scale logarithmic (default: False)
        """

        if self._overlay_type == 'EDMCOverlay':
            self.clear_radar(message_id)
        else:
            self.trim_radar(message_id, circles, markers)
        self._markers[message_id] = RadarSet(markers, circles, x, y, r, d, north, logarithmic)
        self.draw_circles(message_id)
        self.draw_markers(message_id)

    def clear_radar(self, message_id: str, remove: bool = True) -> None:
        """
        Clears radar display
        """

        if message_id in self._markers:
            for item in range(len(self._markers[message_id].circles)):
                self._overlay.send_raw({'id': f'{message_id}_circle_{item}', 'ttl': 0})
                if 'text' in self._markers[message_id].circles[item]:
                    self._overlay.send_raw({'id': f'{message_id}_circle_{item}_text', 'ttl': 0})
            for item in range(len(self._markers[message_id].markers) + 1):
                self._overlay.send_raw({'id': f'{message_id}_{item}'})
            self._overlay.send_raw({'id': f'{message_id}_north'})
        if message_id in self._markers and remove:
            self._markers.pop(message_id)

    def trim_radar(self, message_id: str, circles: list | None = None, markers: list | None = None) -> None:
        """
        Removes expired radar components
        """
        if message_id in self._markers:
            if len(self._markers[message_id].circles) > len(circles):
                for item in range(len(circles) - 1, len(self._markers[message_id].circles)):
                    self._overlay.send_raw({'id': f'{message_id}_circle_{item}'})
                    if 'text' in self._markers[message_id].circles[item]:
                        self._overlay.send_raw({'id': f'{message_id}_circle_{item}_text'})
            if len(self._markers[message_id].markers) > len(markers):
                for item in range(len(markers), len(self._markers[message_id].markers) + 1):
                    self._overlay.send_raw({'id':  f'{message_id}_{item}'})

    @setInterval(10)
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

    @setInterval(10)
    def redraw_radar(self):
        """
        Redraws all cached radars on a 5-second interval.
        :rtype: threading.Event
        """

        if self.available():
            for message_id, markers in self._markers.copy().items():
                if self._overlay_type == 'EDMCOverlay':
                    self.clear_radar(message_id, False)
                self.draw_circles(message_id)
                self.draw_markers(message_id)

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
                    elif message_info.limit != 0 and message_info.limit >= len(message_info.text):
                        self.draw(message_id)
            except Exception as ex:
                logger.debug("Exception during scroll repaint", exc_info=ex)

    def draw(self, message_id: str):
        """
        Render one overlay display
        """

        if message_id in self._text_blocks:
            block = self._text_blocks[message_id]
            count = block.offset
            line_count = 0
            spacer = self._normal_spacer if block.size == "normal" else self._large_spacer
            while (block.limit == 0 or count - block.offset <= block.limit) and count < len(block.text):
                try:
                    self._overlay.send_message("{}_{}".format(message_id, line_count), block.text[count], block.color,
                                               block.x, self._aspect_y(block.y) + (spacer * (count - block.offset)),
                                               ttl=20, size=block.size)
                except AttributeError:
                    count -= 1
                    self._overlay.connect()
                except Exception as ex:
                    logger.debug("Exception during draw", exc_info=ex)
                count += 1
                line_count += 1

    def draw_circles(self, message_id: str):
        if message_id in self._markers:
            for index in range(len(self._markers[message_id].circles)):
                try:
                    points = []
                    x = self._markers[message_id].x
                    y = self._markers[message_id].y
                    r = self._markers[message_id].circles[index]['radius']
                    for pie_slice in range(49):
                        x_point = x + (r * math.cos(math.radians(7.5 * pie_slice)))
                        y_point = y + (r * math.sin(math.radians(7.5 * pie_slice)))
                        point = {
                            'x': self._aspect_x(x_point),
                            'y': self._aspect_y(y_point)
                        }
                        points.append(point)

                    message = {'id': f'{message_id}_circle_{index}',
                               'shape': 'vect',
                               'vector': points,
                               'color': self._markers[message_id].circles[index]['color'],
                               'ttl': 20}
                    self._overlay.send_raw(message)
                    if 'text' in self._markers[message_id].circles[index]:
                        point = {
                            'x': self._aspect_x(x + (r * math.cos(math.radians(0)))),
                            'y': self._aspect_y(y + (r * math.sin(math.radians(0)))),
                            'color': self._markers[message_id].circles[index]['color'],
                            'text': self._markers[message_id].circles[index]['text'],
                            'marker': 'circle'
                        }
                        message = {'id': f'{message_id}_circle_{index}_text', 'shape': 'vect', 'vector': [point], 'ttl': 20}
                        self._overlay.send_raw(message)
                except AttributeError:
                    self._overlay.connect()
                except Exception as ex:
                    logger.debug('Exception during radar circle draw', exc_info=ex)

    def draw_markers(self, message_id: str) -> None:
        if message_id in self._markers:
            try:
                if self._markers[message_id].markers is None:
                    return
                x = self._markers[message_id].x
                y = self._markers[message_id].y
                r = self._markers[message_id].r
                message = {
                    'id': f'{message_id}_north',
                    'shape': 'vect',
                    'vector': [
                        {
                            'x': self._aspect_x(x + ((r-5) * math.cos(math.radians(self._markers[message_id].north)))),
                            'y': self._aspect_y(y + ((r-5) * math.sin(math.radians(self._markers[message_id].north)))),
                        },
                        {
                            'x': self._aspect_x(x + ((r+5) * math.cos(math.radians(self._markers[message_id].north)))),
                            'y': self._aspect_y(y + ((r+5) * math.sin(math.radians(self._markers[message_id].north)))),
                        }
                    ],
                    'color': self._markers[message_id].circles[0]['color'],
                    'ttl': 20
                }
                self._overlay.send_raw(message)
                d = self._markers[message_id].d
                markers = self._markers[message_id].markers
                message = {
                    'id': f'{message_id}_0',
                    'shape': 'vect',
                    'vector': [{
                        'x': self._aspect_x(x), 'y': self._aspect_y(y),
                        'color': self._markers[message_id].circles[0]['color'],
                        'marker': 'circle'
                    }],
                    'ttl': 20
                }
                self._overlay.send_raw(message)
                for item in range(len(markers)):
                    if self._markers[message_id].log:
                        log_d = math.log(markers[item]['distance']+1, d)
                        log_d = log_d if markers[item]['distance'] > 0 else 0
                        marker_radius = r if log_d > 1.0 else log_d * r
                    else:
                        marker_radius = r if markers[item]['distance'] > self._markers[message_id].d \
                            else r * markers[item]['distance'] / self._markers[message_id].d
                    marker_bearing = markers[item]['bearing']
                    x_point = x + (marker_radius * math.cos(math.radians(marker_bearing)))
                    y_point = y + (marker_radius * math.sin(math.radians(marker_bearing)))
                    message = {
                        'id': f'{message_id}_{item+1}',
                        'shape': 'vect',
                        'vector': [{
                            'x': self._aspect_x(x_point), 'y': self._aspect_y(y_point),
                            'color': markers[item]['color'], 'marker': 'cross',
                            'text': markers[item]['text']
                        }],
                        'ttl': 20
                    }
                    self._overlay.send_raw(message)
            except AttributeError:
                self._overlay.connect()
            except Exception as ex:
                logger.debug('Exception during radar marker draw', exc_info=ex)

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
