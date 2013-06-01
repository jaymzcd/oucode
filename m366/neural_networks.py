from random import random
from sympy import exp

# :::.    :::..,::::::  ...    ::::::::::..    :::.      :::
# `;;;;,  `;;;;;;;''''  ;;     ;;;;;;;``;;;;   ;;`;;     ;;;
#   [[[[[. '[[ [[cccc  [['     [[[ [[[,/[[['  ,[[ '[[,   [[[
#   $$$ "Y$c$$ $$""""  $$      $$$ $$$$$$c   c$$$cc$$$c  $$'
#   888    Y88 888oo,__88    .d888 888b "88bo,888   888,o88oo,.__
#   MMM     YM """"YUMMM"YmmMMMM"" MMMM   "W" YMM   ""` """"YUMMM
# :::.    :::..,::::::::::::::::::.::    .   .:::  ...    :::::::..    :::  .    .::::::.
# `;;;;,  `;;;;;;;'''';;;;;;;;''''';;,  ;;  ;;;'.;;;;;;;. ;;;;``;;;;   ;;; .;;,.;;;`    `
#   [[[[[. '[[ [[cccc      [[      '[[, [[, [[',[[     \[[,[[[,/[[['   [[[[[/'  '[==/[[[[,
#   $$$ "Y$c$$ $$""""      $$        Y$c$$$c$P $$$,     $$$$$$$$$c    _$$$$,      '''    $
#   888    Y88 888oo,__    88,        "88"888  "888,_ _,88P888b "88bo,"888"88o,  88b    dP
#   MMM     YM """"YUMMM   MMM         "M "M"    "YMMMMMP" MMMM   "W"  MMM "MMP"  "YMmMY"


class ActivationFunction(object):
    """
        A base class for activation functions.
    """

    def activate(self, netinput):
        """
            Apply activation to the netinput. This simply returns
            the original input untouched
        """
        return netinput


class WeightedActivation(ActivationFunction):

    def __init__(self, weight):
        self.weight = weight

    def activate(self, netinput):
        """
            Simply multiples the netinput by the weight
        """
        return netinput * self.weight


class ThresholdActivation(ActivationFunction):

    def __init__(self, threshold):
        self.threshold = threshold

    def activate(self, netinput):
        """
            Returns 1 if the threshold is passed
        """
        return 1 if netinput > self.threshold else 0


class SigmoidActivation(ActivationFunction):

    def activate(self, netinput):
        """
            Block 4, Page 39
            Uses a typical sigmoid function.
        """
        return 1 / (1 + exp(netinput))


class NetUnit(object):

    def __init__(self, activation):
        self.input = random()
        self.activation = activation
        self.time = 0

    def step(self):
        self.input = self.activation.activate(self.input)
        self.time += 1

    def __str__(self):
        return 'Unit: t(%d) %f' % (self.time, self.input)
