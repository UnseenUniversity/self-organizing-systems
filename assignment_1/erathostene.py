__author__ = 'alexei'

from sos.agent import Agent
from sos.env import Environment
from sos.logger import logger
from random import randint


class ErathoEnv(Environment):

    def __init__(self, size, num_agents):
        super(ErathoEnv, self).__init__(num_agents, ErathoBot)
        self.size   = size
        self.nums   = range(2, size)
        self.primes = range(2, size)

    def init_agent(self, id):
        start = self.random_start()
        return ErathoBot(self, id, self.size, start)

    def random_start(self):

        with self.lock:
            if len(self.nums) == 0:
                self.kill_switch = True
                return None

            start = randint(0, len(self.nums) - 1)
            elem  = self.nums[start]
            del self.nums[start]

            return elem

    def mark_as_not_prime(self, num):
        try:
            self.primes.remove(num)
        except ValueError:
            pass

    def print_results(self):
        print self.primes

class ErathoBot(Agent):

    def __init__(self, env, id, size, first):
        super(ErathoBot, self).__init__(env, id, max_turns=-1)
        self.size    = size
        self.first   = first
        self.current = first

    @logger
    def random_start(self):
        return self.env.random_start()

    @logger
    def mark_as_not_prime(self, num):
        self.env.mark_as_not_prime(num)

    def act(self):

        self.current += self.first
        if self.current > self.size:
            self.first = self.random_start()
            if self.first is None:
                return
            self.current = self.first
        else:
            self.mark_as_not_prime(self.current)


def test():

    env = ErathoEnv(1000, 3)
    env.start()

if __name__ == "__main__":
    test()