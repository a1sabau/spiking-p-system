import unittest
from unittest.mock import MagicMock

from sps.PNeuron import PNeuron
from sps.SNPSystem import SNPSystem
from sps.SpikeUtils import TransformationRule

class SNPSystemTest(unittest.TestCase):

    def setUp(self):
        PNeuron.nid = 0

    def test_tick_neurons_not_triggering_rules(self):
        snps = SNPSystem(max_delay=5, max_steps=100)

        pn1 = PNeuron(targets=[], transf_rules=[])
        pn2 = PNeuron(targets=[], transf_rules=[])

        pn1.tick = MagicMock(return_value=None)
        pn2.tick = MagicMock(return_value=None)

        snps.neurons = [pn1, pn2]
        snps.init_history()

        # after a system tick where no neuron fired/consume a rule, return True in order to keep ticking
        self.assertEqual(snps.tick(), True)

        # each neuron was "ticked"
        pn1.tick.assert_called_with()
        pn2.tick.assert_called_with()

    def test_tick_output_neuron(self):
        """ the final system output should be [startTick, endTick] - the number of ticks passed between the first two firing of the output neuron"""
        snps = SNPSystem(max_delay=5, max_steps=100)
        
        p1 = PNeuron(targets=[], transf_rules=[])
        p_output = PNeuron(targets=[], transf_rules=[], output=True)

        p1.tick = MagicMock(return_value=None)
        output_fire_rule = TransformationRule(div=1, mod=0, source=5, target=1, delay=3)
        p_output.tick = MagicMock(return_value=output_fire_rule)

        snps.neurons = [p1, p_output]
        snps.init_history()

        # output neuron hasn't fired so far
        self.assertEqual(len(snps.output), 0)

        # after a system tick where the output neuron fired once, keep firing
        self.assertEqual(snps.tick(), True)

        # the current system output is [startTick] - recording the 1st firing of the output neuron
        self.assertEqual(len(snps.output), 1)

        # disable the output neuron for 5 ticks
        p_output.tick = MagicMock(return_value=None)
        for x in range(5):
            self.assertEqual(snps.tick(), True)

        # re-enable the output neuron
        # system will complete the computation, the output value is the number of ticks between 1st and 2nd fire events of the output neuron
        p_output.tick = MagicMock(return_value=output_fire_rule)
        self.assertEqual(snps.tick(), False)

        self.assertEqual(len(snps.output), 2)
        self.assertEqual(snps.result(), 6)

if __name__ == '__main__':
    unittest.main()
