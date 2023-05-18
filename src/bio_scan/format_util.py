import locale


class Formatter:

    def __init__(self, shorten=False):
        locale.setlocale(locale.LC_ALL, '')
        self.shorten: bool = shorten

    def set_shorten(self, value: bool) -> None:
        self.shorten = value

    def format_unit(self, num: float, unit: str, space: bool = True) -> str:
        if num > 999999:
            # 1.3 Mu
            s = locale.format_string('%.1f M', num / 1000000.0, grouping=True, monetary=True)
        elif num > 999:
            # 456 ku
            s = locale.format_string('%.1f k', num / 1000.0, grouping=True, monetary=True)
        else:
            # 789 u
            s = locale.format_string('%.0f ', num, grouping=True, monetary=True)

        if not space:
            s = s.replace(' ', '')

        s += unit

        return s

    def format_credits(self, credit_amount: float, space: bool = True) -> str:
        if self.shorten:
            return self.format_unit(credit_amount, 'Cr', space)
        return locale.format_string('%d Cr', credit_amount, grouping=True, monetary=True)

    def format_credit_range(self, min_value: float, max_value: float, space: bool = True) -> str:
        if min_value != max_value:
            if self.shorten:
                return "{} - {}".format(self.format_unit(min_value, '', space),
                                        self.format_unit(max_value, ' Cr', space))
            return locale.format_string('%d - %d Cr', (min_value, max_value), grouping=True, monetary=True)
        else:
            return self.format_credits(min_value, space)

    def format_distance(self, ls: int, unit: str = "ls", space: bool = True) -> str:
        return self.format_unit(ls, unit, space)
