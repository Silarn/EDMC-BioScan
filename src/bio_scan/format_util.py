import locale

from l10n import translations as tr

from bio_scan.globals import bioscan_globals

credits_string = tr.tl('Cr', bioscan_globals.translation_context)  # LANG: Credits unit

class Formatter:

    def __init__(self, shorten=False):
        locale.setlocale(locale.LC_ALL, '')
        self.shorten: bool = shorten

    def set_locale(self, local_code: str):
        locale.setlocale(locale.LC_ALL, local_code)

    def set_shorten(self, value: bool) -> None:
        """
        Set the shorten setting which determines how numbers are displayed.

        :param value: Whether or not to shorten number displays
        """

        self.shorten = value

    def format_unit(self, num: float, unit: str, space: bool = True, monetary: bool = True) -> str:
        """
        Number formatting. Automatically convert base unit to kilo- or mega-.

        :param num: Base numeral in standard unit. (e.g. meter, lightsecond, etc.)
        :param unit: Base unit abbreviation
        :param space: Whether or not to include a space before the unit
        :return: Formatted number string with metric unit conversion
        """

        if num > 999999:
            # 1.3 Mu
            # LANG: Millions unit
            s = locale.format_string('%.2f ' + tr.tl('M', bioscan_globals.translation_context), num / 1000000.0, grouping=True, monetary=monetary)
        elif num > 999:
            # 456 ku
            # LANG: Thousands unit
            s = locale.format_string('%.2f ' + tr.tl('k', bioscan_globals.translation_context), num / 1000.0, grouping=True, monetary=monetary)
        else:
            # 789 u
            s = locale.format_string('%.0f ', num, grouping=True, monetary=monetary)

        if not space:
            s = s.replace(' ', '')

        s += unit

        return s

    def format_credits(self, credit_amount: float, space: bool = True) -> str:
        """
        Currency formatting.

        :param credit_amount: Base credit amount.
        :param space: Whether or not to add a space before the credits unit
        :return: Formatted credits string
        """

        if self.shorten:
            return self.format_unit(credit_amount, credits_string, space)
        return locale.format_string('%d %s', bioscan_globals.translation_context, credit_amount, credits_string, grouping=True, monetary=True)

    def format_credit_range(self, min_value: float, max_value: float, space: bool = True) -> str:
        """
        Currency range formatting.

        :param min_value: Minimum credit amount
        :param max_value: Maximum credit amount
        :param space: Whether or not to add a space before the credits unit
        :return: Formatted credit range string
        """

        if min_value != max_value:
            if self.shorten:
                return "{} - {}".format(self.format_unit(min_value, '', space),
                                        self.format_unit(max_value, f' {credits_string}', space))
            return locale.format_string('%d - %d Cr', (min_value, max_value), grouping=True, monetary=True)
        else:
            return self.format_credits(min_value, space)

    def format_distance(self, distance: int, unit: str, space: bool = True) -> str:
        """
        Distance formatter.

        :param distance: Base distance.
        :param unit: The unit for the distance.
        :param space: Whether to add a space before the distance unit
        :return: Formatted distance string with specified unit
        """

        return self.format_unit(distance, unit, space, False)
