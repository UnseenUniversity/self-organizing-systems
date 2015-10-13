__author__ = 'alexei'

from sos.agent import Agent
from sos.env import Environment
from sos.logger import logger
from random import randint
import time

class PolyWeb(Environment):

    def __init__(self, size, num_agents):
        super(PolyWeb, self).__init__(num_agents, PolySpider)

        self.size = size
        self.poly = range(1, size + 1)
        self.webs = []

    def init_agent(self, id):
        return PolySpider(self, randint(0, len(self.poly) - 1))

    def throw_web(self, spider):

        # atomic action
        with self.lock:

            if len(self.poly) <= 3:
                self.kill_switch = True
                return None

            source = spider.id    % len(self.poly)
            mid    = (source + 1) % len(self.poly)
            target = (source + 2) % len(self.poly)
            web    = (self.poly[source], self.poly[target])

#           print self.poly, spider.id, source, target, web

            self.webs.append(web)
            del self.poly[mid]

            return web

    def print_results(self):

        print "Diagonals: "
        print self.webs


class PolySpider(Agent):

    def __init__(self, env, id):
        super(PolySpider, self).__init__(env, id, max_turns=9999)

    @logger
    def throw_web(self):
        return self.env.throw_web(self)

    def act(self):

        web = self.throw_web()
        if web is None:
            exit(0)

def test():

    env = PolyWeb(10, 5)
    env.start()

if __name__ == "__main__":
    test()
