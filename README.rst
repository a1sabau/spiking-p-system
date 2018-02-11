Spiking Neural P System
=======================


Examples
--------

Table cell details: ::

  r:2a;2->1!;1 = rule applied: condition, transformation, delay, (! denotes a firing event)
  c:0 = neuron charge after applying the rule
  i:1(0) = incoming spikes: charge(source neuron)
  c:2 = neuron charge after receiving the spikes

Compute numbers of form *3k + 2* using 3 neurons
************************************************

Neurons and corresponding rules: ::

  rule0 = [TransformationRule(div=1, mod=0, source=1, target=1, delay=2)]
  pn0 = PNeuron(targets=[1], transf_rules=rule0)
  pn0.charge = 2 * k - 1

  rule1 = [TransformationRule(div=k, mod=0, source=k, target=1, delay=1)]
  pn1 = PNeuron(targets=[2], transf_rules=rule1)
  pn1.charge = 0

  rule2 = [TransformationRule(div=1, mod=0, source=1, target=1, delay=0)]
  pn2 = PNeuron(targets=[], transf_rules=rule2, output=True)
  pn2.charge = 1

Generated table is for *k = 3*. ::

  +---------+----------------------+----------------------+----------------------+
  |  Step   |       Neuron 0       |       Neuron 1       |       Neuron 2       |
  +=========+======================+======================+======================+
  | initial | 3                    | 0                    | 1                    |
  | charge  |                      |                      |                      |
  +---------+----------------------+----------------------+----------------------+
  | 0       | r:1a;1->1!;2         | r:-                  | r:1a;1->1!;0         |
  |         | c:2                  | c:0                  | c:0                  |
  +---------+----------------------+----------------------+----------------------+
  | 1       | r:-                  | r:-                  | r:-                  |
  |         | c:2                  | c:0                  | c:0                  |
  +---------+----------------------+----------------------+----------------------+
  | 2       | r:-                  | r:-                  | r:-                  |
  |         | c:2                  | c:0                  | c:0                  |
  |         |                      | i:1(0)               |                      |
  |         |                      | c:1                  |                      |
  +---------+----------------------+----------------------+----------------------+
  | 3       | r:1a;1->1!;2         | r:-                  | r:-                  |
  |         | c:1                  | c:1                  | c:0                  |
  +---------+----------------------+----------------------+----------------------+
  | 4       | r:-                  | r:-                  | r:-                  |
  |         | c:1                  | c:1                  | c:0                  |
  +---------+----------------------+----------------------+----------------------+
  | 5       | r:-                  | r:-                  | r:-                  |
  |         | c:1                  | c:1                  | c:0                  |
  |         |                      | i:1(0)               |                      |
  |         |                      | c:2                  |                      |
  +---------+----------------------+----------------------+----------------------+
  | 6       | r:1a;1->1!;2         | r:2a;2->1!;1         | r:-                  |
  |         | c:0                  | c:0                  | c:0                  |
  +---------+----------------------+----------------------+----------------------+
  | 7       | r:-                  | r:-                  | r:-                  |
  |         | c:0                  | c:0                  | c:0                  |
  |         |                      |                      | i:1(1)               |
  |         |                      |                      | c:1                  |
  +---------+----------------------+----------------------+----------------------+
  | 8       | r:-                  | r:-                  | r:1a;1->1!;0         |
  |         | c:0                  | c:0                  | c:0                  |
  |         |                      | i:1(0)               |                      |
  |         |                      | c:1                  |                      |
  +---------+----------------------+----------------------+----------------------+

Compute a finite *{ 1, 2, ...k }* set using a one-neuron system
***************************************************************

Neurons and corresponding rules: ::

  rule0 = TransformationRule(div=1, mod=0, source=1, target=1, delay=i) for i in range(1, k)
  rule1 = TransformationRule(div=2, mod=0, source=1, target=1, delay=0))
  pn0 = PNeuron(targets=[], transf_rules=[rule0, rule1], output=True)
  pn0.charge = 2

Generated table is for *k = 10* with a system output of 6. ::

  +---------+----------------------+
  |  Step   |       Neuron 0       |
  +=========+======================+
  | initial | 2                    |
  | charge  |                      |
  +---------+----------------------+
  | 0       | r:1a;1->1!;5         |
  |         | c:1                  |
  +---------+----------------------+
  | 1       | r:-                  |
  |         | c:1                  |
  +---------+----------------------+
  | 2       | r:-                  |
  |         | c:1                  |
  +---------+----------------------+
  | 3       | r:-                  |
  |         | c:1                  |
  +---------+----------------------+
  | 4       | r:-                  |
  |         | c:1                  |
  +---------+----------------------+
  | 5       | r:-                  |
  |         | c:1                  |
  +---------+----------------------+
  | 6       | r:1a;1->1!;3         |
  |         | c:0                  |
  +---------+----------------------+

References
----------

* `Spiking neural P systems <https://www.semanticscholar.org/paper/Spiking-Neural-P-Systems-Ionescu-Paun/1db2b443a0fc71a3fae9a66c4ae16905a26baa17>`_

  Ionescu, Mihai, Gheorghe Păun, and Takashi Yokomori.
  Fundamenta informaticae 71.2, 3 (2006): 279-308.
