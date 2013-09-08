#!/usr/bin/env python2
#
#  :::  .   :::.    :::.  :::.  ::::::::::.  .::::::.   :::.       .,-:::::  :::  .    .::::::.
#  ;;; .;;,.`;;;;,  `;;;  ;;`;;  `;;;```.;;;;;;`    `   ;;`;;    ,;;;'````'  ;;; .;;,.;;;`    `
#  [[[[[/'    [[[[[. '[[ ,[[ '[[, `]]nnn]]' '[==/[[[[, ,[[ '[[,  [[[         [[[[[/'  '[==/[[[[,
# _$$$$,      $$$ "Y$c$$c$$$cc$$$c $$$""      '''    $c$$$cc$$$c $$$        _$$$$,      '''    $
# "888"88o,   888    Y88 888   888,888o      88b    dP 888   888,`88bo,__,o,"888"88o,  88b    dP
#  MMM "MMP"  MMM     YM YMM   ""` YMMMb      "YMmMY"  YMM   ""`   "YUMMMMMP"MMM "MMP"  "YMmMY"
#
# Knapsacks and the travelling salesmen seem to be the "hello world" of many
# GA demos and overviews. This code is focused around TMA04 and study work
# but could be somewhat useful for exploration. As such usual caveats apply
# about verbosity or unoptimized sections.

from __future__ import division
import math

# Convinence function for log to base 2
ln2 = lambda x: math.log(x, 2)


class Knapsack(object):
    """
        A representation class for a knapsack of items with weights
        and values; it has a total capacity which defines whether a
        solution is valid or not. Which items are selected depends
        on the bitstring set.
    """

    weights = []
    values = []
    capacity = 0

    def __init__(self, values, weights, capacity=100):
        assert(len(values) == len(weights))
        self.weights = weights
        self.values = values
        self.capacity = capacity

        # Set a default bitstring of all zeros
        self.bitstring = '0' * len(weights)

        print "Initialized knapsack with weights: %r, values: %r" % (weights, values)
        print "Total capacity: %d\n" % capacity

    @property
    def set_weights(self):
        return [w for i, w in enumerate(self.weights) if bitstring[i] == '1']

    @property
    def set_values(self):
        return [v for i, v in enumerate(self.values) if bitstring[i] == '1']

    @property
    def valid(self):
        return self.weight <= self.capacity

    @property
    def value(self):
        return sum([value * int(self.bitstring[i]) for i, value in enumerate(self.values)])

    @property
    def weight(self):
        return sum([weight * int(self.bitstring[i]) for i, weight in enumerate(self.weights)])

    def __str__(self):
        return 'Knapsack %s - Valid: %s\nValue: %s=%d\nWeight: %s=%d\n' % \
            (self.bitstring, self.valid, '+'.join([str(x) for x in self.set_values]), self.value, '+'.join([str(x) for x in self.set_weights]), self.weight)

    def fitness(self, penalty):
        """
            Returns fitness value with a given penalty function applied
        """
        if self.valid:
            return self.value
        else:
            return max(self.value - penalty(self), 0)


class Penalty(object):

    def __init__(self):
        pass

    def rho(self, values, weights):
        """
            Returns scaling constant based on Michalewicz and Arabas (1994) schemes
        """
        # Element by element division and then select the max value of this
        return max([values[i] / weights[i] for i in range(len(values))])

    # The following penalty functions are defined in the paper:
    #
    # Michalewicz, Z. and Arabas, J. (1994) Genetic algorithms for the 0/1
    # knapsack problem, Lecture Notes in Computer Science, vol. 869, pp. 134 -
    # 143, DOI 10.1007/3-540-58495-1_14.
    #
    # and are used as is

    @property
    def ap1(self):

        def penalty(knapsack):
            rho = self.rho(knapsack.values, knapsack.weights)
            return ln2(1 + rho * abs(knapsack.weight - knapsack.capacity))

        return penalty

    @property
    def ap2(self):
        """
            Returns a function that increases linearly with excess weight
        """

        def penalty(knapsack):
            rho = self.rho(knapsack.values, knapsack.weights)
            return rho * (knapsack.weight - knapsack.capacity)

        return penalty

    @property
    def ap3(self):

        def penalty(knapsack):
            rho = self.rho(knapsack.values, knapsack.weights)
            return (rho * (knapsack.weight - knapsack.capacity)) ** 2

        return penalty


if __name__ == '__main__':

    values = [60, 40, 50, 30, 30, 15]
    weights = [100, 70, 50, 30, 10, 15]

    sack = Knapsack(values, weights)
    sacks = ['000111', '010110', '100100', '111111']
    penalty = Penalty()

    for bitstring in sacks:
        sack.bitstring = bitstring
        # print '\n'.join(['%d/%d = %0.3f' % (sack.values[i], sack.weights[i], sack.values[i]/sack.weights[i]) for i, w in enumerate(sack.weights)])
        # print sack

        print "Fitness: AP1: %0.4f, AP2: %0.4f, AP3: %0.4f\n" % (
            sack.fitness(penalty.ap1),
            sack.fitness(penalty.ap2),
            sack.fitness(penalty.ap3),
        )
