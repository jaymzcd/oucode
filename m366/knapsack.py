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
        solution is valid or not.
    """

    weights = []
    values = []
    capacity = 0

    def __init__(self, values, weights, capacity=100):
        assert(len(values) == len(weights))
        self.weights = weights
        self.values = values
        self.capacity = capacity

    @property
    def valid(self):
        return self.weight <= self.capacity

    @property
    def value(self):
        return sum(self.values)

    @property
    def weight(self):
        return sum(self.weights)

    def __str__(self):
        return 'Knapsack [Valid: %s] (Value: %d, Weight: %d)' % (self.valid, self.value, self.weight)


class KnapsackParser(object):
    """
        Takes a set of weights and values and will then provides a method to
        return Knapsack objects from bitstrings
    """

    weights = []
    values = []

    def __init__(self, values, weights):
        assert(len(values) == len(weights))

        self.weights = weights
        self.values = values

    def knapsack(self, bitstring):
        """
            Convert an input bitstring into a Knapsack object. This will simply
            iterate over the bits and add the weight & value to lists if the
            given bit (and therefore index in data lists) is set
        """

        flags = [int(x) for x in bitstring]
        weights, values = [], []
        for index, flag in enumerate(flags):
            if flag:
                weights.append(self.weights[index])
                values.append(self.values[index])

        return Knapsack(values, weights)


if __name__ == '__main__':

    weights = [100, 70, 50, 30, 10, 15]
    values = [60, 40, 50, 30, 30, 15]

    parser = KnapsackParser(values, weights)

    sacks = ['000111', '010110', '100100', '111111']
    for sack in sacks:
        print parser.knapsack(sack)
