__author__ = 'alexei'


def logger(fun):
    def inner(self, *args):
        # print "Bot ", self.id, ": ", fun.__name__, args
        return fun(self, *args)
    return inner
