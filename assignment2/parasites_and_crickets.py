__author__ = 'alexei'

# z% cricket eggs are destroyed
# nc parasite life cycles
from heapq import *


class Creature(object):

    def __init__(self, current_year, life_cycle):
        self.life_cycle = life_cycle
        self.next_cycle = current_year + life_cycle

    def __cmp__(self, other):
        return self.next_cycle > other.next_cycle


class Parasite(Creature):

    def __init__(self, current_year, settings):
        super(Parasite, self).__init__(current_year, settings)


class Cricket(Creature):

    def __init__(self, current_year, settings):
        super(Cricket, self).__init__(current_year, settings)


parasite_settings = {"life_cycle"                : 2,
                     "increase_in_pop"           : 5,
                     "chance_increase_life_cycle": 5,
                     "chance_keep_life_cycle"    : 5,
                     "karma_cycles"              : 10}
parasite_population = 10
p = Parasite(0, parasite_settings)
parasite_type = p.__class__

cricket_settings = {"life_cycle"                 : 5,
                     "increase_in_pop"           : 5,
                     "chance_increase_life_cycle": 5,
                     "chance_keep_life_cycle"    : 5,
                     "eggs_destroyed"            : 10}
cricket_population = 10
p = Cricket(0, cricket_settings)
cricket_type = p.__class__

current_year = 0

population = [Parasite(current_year, parasite_settings)
              for _ in xrange(parasite_population)] + \
             [Cricket(current_year, cricket_settings)
              for _ in xrange(cricket_population)]

population = []

for _ in xrange(parasite_population):
    heappush(population, Parasite(current_year, parasite_settings["life_cycle"]))

for _ in xrange(cricket_population):
    heappush(population, Cricket(current_year, cricket_settings["life_cycle"]))

while len(population) > 0:

    creatures    = [heappop(population)]
    current_year = creatures[0].next_cycle

    print "Year ", current_year, "!"

    while len(population) > 0:

        creature = heappop(population)
        if creature.next_cycle != current_year:
            heappush(population, creature)
            break
        creatures.append(creature)

    crickets  = [creature for creature in creatures if creature.__class__ == cricket_type]
    parasites = [creature for creature in creatures if creature.__class__ == parasite_type]

    def percent_increase(pop, perc):
        return pop + percent(perc, pop)

    def percent(pop, perc):
        return int(perc * pop / 100)

    def reproduction(population):

        pops = {}
        for creature in population:

            life_cycle = creature.settings["life_cycle"]

            if life_cycle in pops:
                pops[life_cycle].append(creature)
            else:
                pops[life_cycle] = [creature]
        return pops

    if len(parasites) == 0:

        pops = reproduction(crickets)
        for pop in pops:

            new_count = percent_increase(pop, cricket_settings["increase_in_pop"])
            for _ in xrange(len(pops[pop])):
                heappush(population, Cricket(current_year, cricket_settings))

    elif len(crickets) == 0:

        pops = reproduction(parasites)

        for pop in pops:
            new_count = len(parasites)

            count_1 = percent_increase(new_count, parasite_settings["chance_increase_life_cycle"])
            life_cycle = pop + 1

            for _ in xrange(count_1):
                heappush(population, Parasite(current_year, life_cycle))

            count_2 = percent(new_count, parasite_settings["chance_keep_life_cycle"])
            life_cycle = pop

            for _ in xrange(count_2):
                heappush(population, Parasite(current_year, life_cycle))

            count_3 = 100 - count_1 - count_2
            life_cycle = pop - 1
            if life_cycle == 0 or count_3 <= 0:
                continue

            for _ in xrange(count_3):
                heappush(population, Parasite(current_year, life_cycle))

    else:

        pops = reproduction(crickets)

        for pop in pops:
            new_count = percent_increase(pop, cricket_settings["increase_in_pop"])

            count_1 = percent_increase(new_count, cricket_settings["chance_increase_life_cycle"])
            life_cycle = pop + 1

            for _ in xrange(count_1):
                heappush(population, Cricket(current_year, life_cycle))

            count_2 = percent(new_count, cricket_settings["chance_keep_life_cycle"])
            life_cycle = pop

            for _ in xrange(count_2):
                heappush(population, Cricket(current_year, life_cycle))

            count_3 = 100 - count_1 - count_2
            life_cycle = pop - 1
            if life_cycle == 0 or count_3 <= 0:
                continue

            for _ in xrange(count_3):
                heappush(population, Cricket(current_year, life_cycle))

            pops = reproduction(parasites)
            for pop in pops:
                new_count = percent_increase(pop, parasite_settings["increase_in_pop"])
                for _ in xrange(len(pops[pop])):
                    heappush(population, Parasite(current_year, parasite_settings))



























