__author__ = 'alexei'

import threading


class Environment(object):

    def __init__(self, num_agents, agent_type, default_timeout=1):

        self.agent_num  = num_agents
        self.agent_type = agent_type
        self.agents     = []

        self.kill_switch = False
        self.lock  = threading.Lock()
        self.timer = threading.Timer(default_timeout, self.end)

    def init_agent(self, id):
        return self.agent_type(self, id)

    def start(self):
        self.agents = [self.init_agent(id) for id in xrange(self.agent_num)]
        map(lambda agent: agent.start(), self.agents)
        self.timer.start()

    def end(self):
        map(lambda agent: agent.join(), self.agents)
        self.print_results()

    def print_results(self):
        print "Mission success!"
