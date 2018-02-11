"""Spike related utils classes"""
from texttable import Texttable

class SpikeEvent:
    """contains originator neuron, charge and target neurons"""
    def __init__(self, nid, charge, targets):
        self.nid = nid
        self.charge = charge
        self.targets = targets

class TransformationRule:
    """
    E1/a^r1->a;t1
    E2/a^r2->a;t2
    a+/a->a | a^k -> a | ...
    a^2 exact condition, a^2n+1 | a^2n condition, a^+ condition
    # match condition:
        - exact, div = 1, mod = 0
        - match, an+b, div = a, mod = b
    # target
        - value = 0, forget
        - value = x, fire
    # source is always substracted from current charge
    """
    def __init__(self, div, mod, source, target, delay):
        self.div = div
        self.mod = mod
        self.source = source
        self.target = target
        self.delay = delay

    def check(self, charge):
        return charge > 0 and charge % self.div == self.mod

    def exec(self, charge):
        return charge -self.source

    def __str__(self):
        # condition
        rulecond = "{0}a{1}".format(self.div, "+{0}".format(self.mod) if self.mod > 0 else "")

        # transformation
        ruletransf = "{0}->{1}{2}".format(self.source, self.target, "!" if self.target > 0 else "")

        return "{0};{1};{2}".format(rulecond, ruletransf, self.delay)

class History:
    """
    responsible for recording each neuron status at each step
    takes of advantage of neuron ids starting from 0
    """
    def __init__(self, neurons):
        self.ticks = []
        self.n_len = len(neurons)

        # add initial charge
        self.add_new_tick()
        for neuron in neurons:
            self.ticks[-1][neuron.nid] = neuron.charge

    def add_new_tick(self):
        self.ticks.append([""] * self.n_len)

    def record_rule(self, neuron, used_rule):
        self.ticks[-1][neuron.nid] = "r:{0}\nc:{1}".format(str(used_rule) if used_rule else "-", neuron.charge)

    def record_incoming(self, neuron, charge, source_nid):
        self.ticks[-1][neuron.nid] += "\ni:{0}({2})\nc:{1}".format(charge, neuron.charge, source_nid)

    def __str__(self):
        ticks_wrapper = []
        for idx, tick in enumerate(self.ticks):
            pref = idx - 1 if idx > 0 else "initial\ncharge"
            ticks_wrapper.append([pref] + tick)

        table = Texttable()
        table.set_cols_width([7] + [20] * len(self.ticks[0]))
        table.header(["Step"] + ["Neuron " + str(nid) for nid in range(len(self.ticks[0]))])
        table.add_rows(ticks_wrapper[:], header=False)

        return str(table.draw())
        