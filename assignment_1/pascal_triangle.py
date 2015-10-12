__author__ = 'alexei'

from sos.agent import Agent
from sos.env import Environment
from sos.logger import logger
from random import randint


class PascalEnv(Environment):

    def __init__(self, size, num_agents):
        super(PascalEnv, self).__init__(num_agents, PascalBot)

        self.size     = size
        self.matrix   = [[1 for _ in xrange(i)] for i in xrange(1, size + 1)]
        self.count    = size * (size + 1) / 2 - size * 2 + 1
        self.agent_id = 0

    def print_results(self):

        if self.kill_switch:
            print "Mission success!"

        for row in xrange(len(self.matrix)):
            for col in xrange(len(self.matrix[row])):
                print self.matrix[row][col],
            print

        map(lambda agent: agent.print_turn_count(), self.agents)

    def init_agent(self, id):
        row = randint(2, self.size - 1)
        col = randint(1, row - 1)
        return PascalBot(self, id, row, col)

    def check_position(self, bot, row, col):

        # print "check_position", row + 1, col + 1

        if col == 0 or\
           col == len(self.matrix[row]) - 1:
            return self.matrix[row][col]  # position already configured

        with self.lock:
            if self.matrix[row][col] != 1:
                return self.matrix[row][col]
            return None

    def set_value(self, bot, pos, value):

        row, col = pos
        # print "set value", row + 1, col + 1

        with self.lock:
            if self.matrix[row][col] == 1:
                self.count -= 1
                if self.count == 0:
                    self.kill_switch = True

            self.matrix[row][col] = value

    def random_jump(self, bot):

        row, col = bot.row, bot.col
        jump = []

        if row > 0 and col < row - 1 and col != 0:
            jump.append((-1, 0))
        if row < len(self.matrix) - 1 and col != 0:
            jump.append((1, 0))

        if 0 < col != 1:
            jump.append((0, -1))
        if col < len(self.matrix[row]) - 2:
            jump.append((0, +1))

        return jump[randint(0, len(jump) - 1)]


class PascalBot(Agent):

    def __init__(self, env, id, row, col):

        super(PascalBot, self).__init__(env, id, max_turns=9000)
        self.row = row
        self.col = col

    @logger
    def jump(self, nx, ny):
        self.row += nx
        self.col += ny

    def random_jump(self):
        return self.env.random_jump(self)

    @logger
    def check_position(self, row, col):
        return self.env.check_position(self, row, col)

    @logger
    def set_value(self, pos, value):
        return self.env.set_value(self, pos, value)

    def act(self):

        if self.check_position(self.row, self.col) is not None:
            (nx, ny) = self.random_jump()
            self.jump(nx, ny)
        else:
            up      = self.check_position(self.row - 1, self.col)
            up_left = self.check_position(self.row - 1, self.col - 1)

            if up is None or up_left is None:
                (nx, ny) = self.random_jump()
                self.jump(nx, ny)
                return

            self.set_value((self.row, self.col), up + up_left)


def test():

    env = PascalEnv(10, 4)
    env.start()

if __name__ == "__main__":
    test()
