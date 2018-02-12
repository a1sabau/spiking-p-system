"""Some examples using spiking neural p systems"""
from sps.SNPSystem import SNPSystem

def compute_fig2(k):
    snps = SNPSystem(max_delay=5, max_steps=100)
    snps.construct_scenario_fig2(k=k)
    snps.start()

    print(snps.history)
    #output is 3k+2
    print("input: ", k, "result", snps.result())

def compute_finite_set(k):
    snps = SNPSystem(max_delay=k, max_steps=100)
    snps.construct_scenario_finite_set(k=k)
    snps.start()

    print(snps.history)
    # output is value from the {1,2, ...k} set
    print("input: ", k, "result", snps.result())

compute_fig2(k=2)
#compute_finite_set(k = 10)