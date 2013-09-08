#!/usr/bin/env python2

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
    def valid(self):
        return self.weight <= self.capacity

    @property
    def value(self):
        return sum([value * int(self.bitstring[i]) for i, value in enumerate(self.values)])

    @property
    def weight(self):
        return sum([weight * int(self.bitstring[i]) for i, weight in enumerate(self.weights)])

    def __str__(self):
        return 'Knapsack %s [Valid: %s] (Value: %d, Weight: %d)' % \
            (self.bitstring, self.valid, self.value, self.weight)


if __name__ == '__main__':

    values = [60, 40, 50, 30, 30, 15]
    weights = [100, 70, 50, 30, 10, 15]

    sack = Knapsack(values, weights)
    sacks = ['000111', '010110', '100100', '111111']

    for bitstring in sacks:
        sack.bitstring = bitstring
        print sack
