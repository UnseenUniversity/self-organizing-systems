__author__ = 'alexei'

# z% cricket eggs are destroyed
# nc parasite life cycles
from heapq import *

from creature import Creature, Parasite, Cricket


def spawn(cls, settings, year=0):

    cls.settings = settings
    count        = settings["initial_count"]
    life_cycle   = settings["life_cycle"]
    return [cls(year, life_cycle) for _ in xrange(count)]


def test(cricket_settings,
         parasite_settings,
         max_year=42):

    # parasite_count        = parasite_settings["initial_count"]
    # parasite_life_cycle   = parasite_settings["life_cycle"]
    # Parasite.repro_distro = parasite_settings["repro_distro"]
    # Parasite.karma_cycles = parasite_settings["karma_cycles"]
    # Parasite.pop_increase = parasite_settings["pop_increase"]
    #
    # cricket_count        = cricket_settings["initial_count"]
    # cricket_life_cycle   = cricket_settings["life_cycle"]
    # Cricket.repro_distro = cricket_settings["repro_distro"]
    # Cricket.karma_cycles = cricket_settings["karma_cycles"]
    # Cricket.pop_increase = cricket_settings["pop_increase"]

    tmp = spawn(Cricket, cricket_settings) + \
          spawn(Parasite, parasite_settings)

    env = []

    for elem in tmp:
        heappush(env, elem)

    count = {"parasite": parasite_settings["initial_count"],
             "cricket": cricket_settings["initial_count"]}
    year = 0

    def attach_creature(kind, life_cycle, creature):
            if life_cycle in kind:
                kind[life_cycle].append(creature)
            else:
                kind[life_cycle] = [creature]

    while count["parasite"] > 0 and abs(count["parasite"] - count["cricket"]) < 100000 and \
          count["cricket"] > 0 and \
          year < max_year:

        creatures = []
        year = env[0].next_cycle

        print "Year: ", year, " | Parasites: ", count["parasite"], " | Crickets: ", count["cricket"]

        while len(env) > 0 and env[0].next_cycle == year:
            creature = heappop(env)
            creatures.append(creature)

        parasites = {}
        crickets  = {}

        crickets_exist  = False
        parasites_exist = False

        for creature in creatures:
            life_cycle = creature.life_cycle
            if creature.type == "parasite":
                attach_creature(parasites, life_cycle, creature)
                parasites_exist = True
            else:
                attach_creature(crickets, life_cycle, creature)
                crickets_exist = True

        if not parasites_exist:

            print "No parasites this cycle!"

            population = []
            for life_cycle, pop in crickets.items():
                print "Cricket population", (life_cycle, len(pop))

                count["cricket"] -= len(pop)

                new_crickets = Cricket.reproduce(year, life_cycle, len(pop), mutations=False)
                population += new_crickets

                count["cricket"] += len(new_crickets)

            for creature in population:
                heappush(env, creature)

        elif not crickets_exist:

            print "No crickets this cycle!"

            for life_cycle, pop in parasites.items():
                print "Parasite population", (life_cycle, len(pop))

                for parasite in pop:
                    if parasite.attempts_left == 0:
                        count["parasite"] -= 1
                    else:
                        parasite.attempts_left -= 1
                        parasite.next_cycle     = year + parasite.life_cycle
                        heappush(env, parasite)

        else:

            print "Crickets and parasites meet!"

            population = []
            for life_cycle, pop in crickets.items():
                print "Cricket population", (life_cycle, len(pop))

                count["cricket"] -= len(pop)

                new_crickets = Cricket.reproduce(year, life_cycle, len(pop), mutations=True)
                population += new_crickets

                count["cricket"] += len(new_crickets)


            # kill the babies!
            perc = cricket_settings["baby_massacre"]
            new_count = min(max(1, int(len(population) * perc / 100)), len(population))
            print count["cricket"], new_count, len(population)
            count["cricket"] -= new_count
            population = population[new_count:]

            for life_cycle, pop in parasites.items():
                print "Parasite population", (life_cycle, len(pop))

                count["parasite"] -= len(pop)

                new_parasites = Parasite.reproduce(year, life_cycle, len(pop), mutations=False)
                population += new_parasites

                count["parasite"] += len(new_parasites)

            for creature in population:
                heappush(env, creature)

        print "Year: ", year, " | Parasites: ", count["parasite"], " | Crickets: ", count["cricket"]
        year += 1
        print "==============================================="
        print

    print
    print "Survivors", count, "!"

    result_parasites = {}
    result_crickets  = {}

    for creature in env:
        life_cycle = creature.life_cycle
        if creature.type == "parasite":
            attach_creature(result_parasites, life_cycle, creature)
        else:
            attach_creature(result_crickets, life_cycle, creature)

    for cycle, pop in result_parasites.items():
        print len(pop), " parasites with cycle ", cycle

    for cycle, pop in result_crickets.items():
        print len(pop), " crickets with cycle ", cycle


def test_0():

    parasite_settings = {"initial_count": 50,
                         "life_cycle": 2,
                         "pop_increase": 50,
                         "repro_distro": [(33, +1), (33, +0), (33, -1)],
                         "karma_cycles": 10}

    cricket_settings = {"initial_count": 50,
                        "life_cycle": 7,
                        "pop_increase": 50,
                        "repro_distro": [(33, +1), (33, +0), (33, -1)],
                        "baby_massacre": 25}

    test(cricket_settings, parasite_settings, max_year=1024)

def test_1():

    parasite_settings = {"initial_count": 10,
                         "life_cycle": 10,
                         "pop_increase": 5,
                         "repro_distro": [(33, +1), (33, +0), (33, -1)],
                         "karma_cycles": 2}

    cricket_settings = {"initial_count": 100,
                        "life_cycle": 10,
                        "pop_increase": 10,
                        "repro_distro": [(33, +1), (33, +0), (33, -1)],
                        "baby_massacre": 75}

    test(cricket_settings, parasite_settings, max_year=1024)

# test_0()
test_1()





#
# cricket_population = 10
# p = Cricket(0, cricket_settings)
# cricket_type = p.__class__
#
# current_year = 0
#
# population = [Parasite(current_year, parasite_settings)
#               for _ in xrange(parasite_population)] + \
#              [Cricket(current_year, cricket_settings)
#               for _ in xrange(cricket_population)]
#
# population = []
#
# for _ in xrange(parasite_population):
#     heappush(population, Parasite(current_year, parasite_settings["life_cycle"]))
#
# for _ in xrange(cricket_population):
#     heappush(population, Cricket(current_year, cricket_settings["life_cycle"]))
#
# while len(population) > 0:
#
#     creatures    = [heappop(population)]
#     current_year = creatures[0].next_cycle
#
#     print "Year ", current_year, "!"
#
#     while len(population) > 0:
#
#         creature = heappop(population)
#         if creature.next_cycle != current_year:
#             heappush(population, creature)
#             break
#         creatures.append(creature)
#
#     crickets  = [creature for creature in creatures if creature.__class__ == cricket_type]
#     parasites = [creature for creature in creatures if creature.__class__ == parasite_type]
#
#
#
#
#
#     if len(parasites) == 0:
#
#         pops = reproduction(crickets)
#         for pop in pops:
#
#             new_count = percent_increase(pop, cricket_settings["increase_in_pop"])
#             for _ in xrange(len(pops[pop])):
#                 heappush(population, Cricket(current_year, cricket_settings))
#
#     elif len(crickets) == 0:
#
#         pops = reproduction(parasites)
#
#         for pop in pops:
#             new_count = len(parasites)
#
#             count_1 = percent_increase(new_count, parasite_settings["chance_increase_life_cycle"])
#             life_cycle = pop + 1
#
#             for _ in xrange(count_1):
#                 heappush(population, Parasite(current_year, life_cycle))
#
#             count_2 = percent(new_count, parasite_settings["chance_keep_life_cycle"])
#             life_cycle = pop
#
#             for _ in xrange(count_2):
#                 heappush(population, Parasite(current_year, life_cycle))
#
#             count_3 = 100 - count_1 - count_2
#             life_cycle = pop - 1
#             if life_cycle == 0 or count_3 <= 0:
#                 continue
#
#             for _ in xrange(count_3):
#                 heappush(population, Parasite(current_year, life_cycle))
#
#     else:
#
#         pops = reproduction(crickets)
#
#         for pop in pops:
#             new_count = percent_increase(pop, cricket_settings["increase_in_pop"])
#
#             count_1 = percent_increase(new_count, cricket_settings["chance_increase_life_cycle"])
#             life_cycle = pop + 1
#
#             for _ in xrange(count_1):
#                 heappush(population, Cricket(current_year, life_cycle))
#
#             count_2 = percent(new_count, cricket_settings["chance_keep_life_cycle"])
#             life_cycle = pop
#
#             for _ in xrange(count_2):
#                 heappush(population, Cricket(current_year, life_cycle))
#
#             count_3 = 100 - count_1 - count_2
#             life_cycle = pop - 1
#             if life_cycle == 0 or count_3 <= 0:
#                 continue
#
#             for _ in xrange(count_3):
#                 heappush(population, Cricket(current_year, life_cycle))
#
#             pops = reproduction(parasites)
#             for pop in pops:
#                 new_count = percent_increase(pop, parasite_settings["increase_in_pop"])
#                 for _ in xrange(len(pops[pop])):
#                     heappush(population, Parasite(current_year, parasite_settings))
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#








