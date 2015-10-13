__author__ = 'alexei'

import threading
import time


class Agent(threading.Thread, object):

    def __init__(self, env, id, max_turns=999):
        super(Agent, self).__init__()
        self.env       = env
        self.id        = id
        self.turns     = 0
        self.max_turns = max_turns

    def print_turn_count(self):
        print "Bot", self.id, " turns: ", self.turns, " / ", self.max_turns

    def act(self):
        pass

    @staticmethod
    def _yield():
        time.sleep(0.01)

    def run(self):

        while not self.env.kill_switch:
            self.act()
            self.turns += 1
            if self.max_turns != -1 and\
               self.turns == self.max_turns:
                break

            self._yield()