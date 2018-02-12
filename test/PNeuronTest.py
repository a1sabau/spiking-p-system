import unittest
from sps.PNeuron import PNeuron
from sps.SpikeUtils import TransformationRule

class PNeuronTest(unittest.TestCase):
    def test_fire(self):
        fire_rule = TransformationRule(div=1, mod=0, source=5, target=1, delay=3)
        pn = PNeuron(targets=[], transf_rules=[fire_rule])
        pn.charge = 8
        pn.fire(pn.transf_rules[0])

        # after a firing event, the neuron current charge is diminished by rule source condition
        self.assertEqual(pn.charge, 8-5)

        # after a firing event, the neuron refractory period is equal to rule delay, diminishing by 1 per tick
        self.assertEqual(pn.refractory, 3)
        for x in range(3):
            self.assertEqual(pn.tick(), None)


    def test_consume(self):
        fire_rule = TransformationRule(div=1, mod=0, source=5, target=1, delay=3)
        pn = PNeuron(targets=[], transf_rules=[fire_rule])
        pn.charge = 8
        pn.consume(pn.transf_rules[0])

        # after a consume event, the neuron current charge is diminished by rule source condition
        self.assertEqual(pn.charge, 8-5)

        # after a consume event, the neuron does not enter a refractory period
        self.assertEqual(pn.refractory, 0)

if __name__ == '__main__':
    unittest.main()
