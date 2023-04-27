import locale


class Formatter:

    def __init__(self, shorten=False):
        locale.setlocale(locale.LC_ALL, '')
        self.shorten: bool = shorten

    def set_shorten(self, value: bool):
        self.shorten = value

    def format_unit(self, num, unit, space=True):
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

    def format_credits(self, credits, space=True):
        if self.shorten:
            return self.format_unit(credits, 'Cr', space)
        return locale.format_string('%d Cr', credits, grouping=True, monetary=True)

    def format_credit_range(self, min, max, space=True):
        if min != max:
            if self.shorten:
                return "{} - {}".format(self.format_unit(min, '', space),
                                        self.format_unit(max, ' Cr', space))
            return locale.format_string('%d - %d Cr', (min, max), grouping=True, monetary=True)
        else:
            return self.format_credits(min, space)

    def format_distance(self, ls, unit="ls", space=True):
        return self.format_unit(ls, unit, space)
