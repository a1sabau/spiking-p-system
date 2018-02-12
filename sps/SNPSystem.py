"""Spiking Neural P System"""
from .PNeuron import PNeuron
from .SpikeUtils import SpikeEvent, TransformationRule, History

class SNPSystem:
    """Spiking Neural P System"""
    def __init__(self, max_delay, max_steps):
        # init time step, history
        self.t_step = 0
        self.max_steps = max_steps
        self.history = None

        # init circular future spiking events based on max_delay
        self.max_delay = max_delay
        self.spike_events = [[] for x in range(self.max_delay)]

        # init neuron container
        self.neurons = []

        # record output
        self.output = []

    def init_history(self):
        """init tick history based on the system's neurons"""
        self.history = History(self.neurons)

    def start(self):
        """start sending and receiving spikes"""

        # init history
        self.init_history()

        # keep on ticking until output condition is met or max number of ticks is exceeded
        while True:
            if not self.tick():
                break

    def result(self):
        """system output as number of total ticks between 1st and 2nd spike of the output neuron"""
        return self.output[1] - self.output[0]

    def tick(self):
        """at each time step, first evolve and then receive spikes, cant do both in the same step, refractory will prevent it"""
        self.history.add_new_tick()

        # evolve each neuron
        for neuron in self.neurons:
            used_rule = neuron.tick()

            # fire event
            if used_rule and used_rule.target > 0:
                #print("--fire: ", neuron.nid)
                self.spike_events[(self.t_step + used_rule.delay) % self.max_delay].append(SpikeEvent(neuron.nid, used_rule.target, neuron.targets))
                # record output if neuron belongs to output
                if neuron.output:
                    self.output.append(self.t_step)

            self.history.record_rule(neuron, used_rule)


        # consume current spiking events
        for spike_event in self.spike_events[self.t_step % self.max_delay]:
            for idx in spike_event.targets:
                #print("--received: ", self.neurons[idx].nid, idx)
                self.neurons[idx].receive(spike_event.charge)
                self.history.record_incoming(self.neurons[idx], spike_event.charge, spike_event.nid)

        # clear current spiking events
        self.spike_events[self.t_step % self.max_delay].clear()

        # advance time
        self.t_step += 1

        # exit if closing condition is met, otherwise continue
        return False if (len(self.output) == 2 or self.t_step > self.max_steps) else True

    def construct_scenario_fig2(self, k):
        rule0 = [TransformationRule(div=1, mod=0, source=1, target=1, delay=2)]
        pn0 = PNeuron(targets=[1], transf_rules=rule0)
        pn0.charge = 2 * k - 1

        rule1 = [TransformationRule(div=k, mod=0, source=k, target=1, delay=1)]
        pn1 = PNeuron(targets=[2], transf_rules=rule1)
        pn1.charge = 0

        rule2 = [TransformationRule(div=1, mod=0, source=1, target=1, delay=0)]
        pn2 = PNeuron(targets=[], transf_rules=rule2, output=True)
        pn2.charge = 1

        self.neurons += [pn0, pn1, pn2]

    def construct_scenario_finite_set(self, k):
        rules = [TransformationRule(div=1, mod=0, source=1, target=1, delay=i) for i in range(1, k)]
        rules.append(TransformationRule(div=2, mod=0, source=1, target=1, delay=0))
        pn0 = PNeuron(targets=[], transf_rules=rules, output=True)
        pn0.charge = 2

        self.neurons += [pn0]
