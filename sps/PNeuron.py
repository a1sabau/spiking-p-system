"""P Neuron"""
import random

class PNeuron:
    """
    each neuron has a unique nid, 
    connects to other neurons (targets),
    follows a set of charge transformation rules, 
    can be an internal or output neuron with output neurons terminating the computation
    """
    nid = 0

    @staticmethod
    def get_nid():
        return PNeuron.nid

    @staticmethod
    def increment_nid():
        PNeuron.nid += 1

    def __init__(self, targets, transf_rules, output=False):
        self.nid = PNeuron.get_nid()
        PNeuron.increment_nid()
        
        self.targets = targets

        self.charge = 0
        self.refractory = 0 # can not fire or receive outside spikes between firing at t0 and spiking at to+delay

        self.transf_rules = transf_rules

        # whether or not this neuron is an output one
        self.output = output

    def receive(self, charge):
        # only receive input if outside the refractory period
        if self.refractory == 0:
            self.charge += charge

    def tick(self):
        """tick and use all available rules: fire|forget"""

        # recover from refractory period after a spike
        if (self.refractory > 0):
            self.refractory = self.refractory -1
            return None

        # randomly apply either a firing or reducing rule meeting the current charge criteria
        idxs = list(range(len(self.transf_rules)))
        random.shuffle(idxs)
        for idx in idxs:
            rule = self.transf_rules[idx]
            #print("checking rule ", idx)
            if rule.check(self.charge):
                if rule.target > 0:
                    return self.fire(rule)
                else:
                    return self.consume(rule)

        return None

    def fire(self, rule):
        self.charge = self.charge - rule.source
        self.refractory = rule.delay
        return rule

    def consume(self, rule):
        self.charge = self.charge - rule.source
        return rule
