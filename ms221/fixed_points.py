# -*- coding: utf-8 -*-

from sympy import diff
from sympy.solvers import solve
from sympy.abc import x

from helpers import _eval

# .        :       ...    :::::::-.   ...    ::: :::    .,::::::    :::::::.
# ;;,.    ;;;   .;;;;;;;.  ;;,   `';, ;;     ;;; ;;;    ;;;;''''     ;;;'';;'
# [[[[, ,[[[[, ,[[     \[[,`[[     [[[['     [[[ [[[     [[cccc      [[[__[[\.
# $$$$$$$$"$$$ $$$,     $$$ $$,    $$$$      $$$ $$'     $$""""      $$""""Y$$
# 888 Y88" 888o"888,_ _,88P 888_,o8P'88    .d888o88oo,.__888oo,__   _88o,,od8P
# MMM  M'  "MMM  "YMMMMMP"  MMMMP"`   "YmmMMMM""""""YUMMM""""YUMMM  ""YUMMMP"


def fixed_points(func):
    """
        Module B1, Page 13

        A fixed pointsuch that f (a) = a of a real function f
        is a number a in the domain of f
    """
    # This is pretty simple, just solve f(x) = x, that is
    # f(x) - x = 0
    points = solve(func - x)
    print "Fixed points of %s are %s" % (func, points)
    return points


def classify_fixed_points(func):
    """
        Module B1, Page 23, 24 - Behaviour near a fixed point

        Let a be a fixed point of a smooth function f , and let xn be an
        iteration sequence generated by f .

        (a) If |f (a)| < 1, then there is an open interval I containing a with
        the property that if x0 is in I, then xn → a as n → ∞.

        (b) If |f (a)| > 1, then no iteration sequence generated by f
        converges to a, unless xn = a for some value of n.

        Takes a function as input, gets the fixed points and then classifies
        them returning a list of tuples of (point, gradient value, classification)
    """

    classified_points = list()

    points = fixed_points(func)
    # We'll need to use the first derivative of the function to classify the
    # points according to the above criteria.
    gradient_func = diff(func)

    for point in points:
        val = abs(_eval(gradient_func, point))
        if val > 1:
            point_type = 'repelling'
        if val < 1:
            point_type = 'attracting'
        if val == 1:
            point_type = 'indifferent'
        if val == 0:
            point_type = 'super-attracting'

        classified_points.append((point, val, point_type))

    print "Classified fixed points for %s:\n%r\n:" % (func, classified_points)
    return classified_points
