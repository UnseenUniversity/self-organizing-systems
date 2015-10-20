__author__ = 'alexei'


def increase_population(count, percentage):
    return count + max(1, (count * percentage / 100))


class Creature(object):

    settings = {}

    def __init__(self, current_year, life_cycle):
        self.life_cycle = life_cycle
        self.next_cycle = current_year + life_cycle

    def __cmp__(self, other):
        return self.next_cycle > other.next_cycle

    @classmethod
    def reproduce(cls, current_year, life_cycle, base_count, mutations=True):

        if base_count == 0:
            return

        num        = increase_population(base_count, cls.settings["pop_increase"])
        result     = []

        if mutations:

            for (perc, change) in cls.settings["repro_distro"]:

                count = max(1, int((perc * num) / 100))
                new_life_cycle = max(1, life_cycle + change)
                result += [cls(current_year, new_life_cycle) for _ in xrange(count)]
        else:

            result = [cls(current_year, life_cycle) for _ in xrange(num)]

        return result


class Parasite(Creature):

    def __init__(self, current_year, life_cycle):
        super(Parasite, self).__init__(current_year, life_cycle)
        self.attempts_left = Parasite.settings["karma_cycles"]
        self.type = "parasite"

class Cricket(Creature):

    def __init__(self, current_year, life_cycle):
        super(Cricket, self).__init__(current_year, life_cycle)
        self.type = "cricket"