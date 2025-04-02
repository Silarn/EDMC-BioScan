import locale

from l10n import translations as tr

from EDMCLogging import get_plugin_logger

from bio_scan.globals import bioscan_globals

logger = get_plugin_logger('BioScan')

credits_string = tr.tl('Cr', bioscan_globals.translation_context)  # LANG: Credits unit

def convert_locale(locale_code: str) -> str:
    match locale_code:
        case 'cs':
            return 'cs_CZ'
        case 'de':
            return 'de_DE'
        case 'en':
            return 'en_US'
        case 'es':
            return 'es_ES'
        case 'fi':
            return 'fi_FI'
        case 'fr':
            return 'fr_FR'
        case 'hu':
            return 'hu_HU'
        case 'it':
            return 'it_IT'
        case 'ja':
            return 'ja_JP'
        case 'ko':
            return 'ko_KR'
        case 'lv':
            return 'lv_LV'
        case 'nl':
            return 'nl_NL'
        case 'pl':
            return 'pl_PL'
        case 'pt' | 'pt-PT':
            return 'pt_PT'
        case 'pt-BR':
            return 'pt_BR'
        case 'ru':
            return 'ru_RU'
        case 'sl':
            return 'sl_SI'
        case 'sr' | 'sr-Latn' | 'sr-Latn-BA':
            return 'sr_RS'
        case 'tr':
            return 'tr_TR'
        case 'uk':
            return 'en_UK'
        case 'zh-Hans':
            return 'zh_ZA'
        case _:
            return 'en_US'

class Formatter:

    def __init__(self, shorten=False):
        locale.setlocale(locale.LC_ALL, '')
        self.shorten: bool = shorten

    def set_locale(self, locale_code: str):
        try:
            locale_code = convert_locale(locale_code)
            locale.setlocale(locale.LC_ALL, locale_code)
        except locale.Error as ex:
            logger.error(f'Locale: {locale_code}', exc_info=ex)

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
