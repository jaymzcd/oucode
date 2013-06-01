# -*- coding: utf-8 -*-

from helpers import _eval

# .        :       ...    :::::::-.   ...    ::: :::    .,::::::      .,-:::::
# ;;,.    ;;;   .;;;;;;;.  ;;,   `';, ;;     ;;; ;;;    ;;;;''''    ,;;;'````'
# [[[[, ,[[[[, ,[[     \[[,`[[     [[[['     [[[ [[[     [[cccc     [[[
# $$$$$$$$"$$$ $$$,     $$$ $$,    $$$$      $$$ $$'     $$""""     $$$
# 888 Y88" 888o"888,_ _,88P 888_,o8P'88    .d888o88oo,.__888oo,__   `88bo,__,o,
# MMM  M'  "MMM  "YMMMMMP"  MMMMP"`   "YmmMMMM""""""YUMMM""""YUMMM    "YUMMMMMP"

def is_even_function(func, i=range(1, 10)):
    """
        If the graph of a function f is unchanged under reflection in the
        y-axis, as in Figure 3.2(a), then f is said to be an even function.
        Thus f is even if

        f (−x) = f (x), for all x in the domain of f.
    """
    is_even = all([_eval(func, _x) == _eval(func, -_x) for _x in i])
    return is_even


def is_odd_function(func, i=range(1, 10)):
    """
        If the graph of f is unchanged by rotation through the angle π about
        the origin, as in Figure 3.2(b), then f is said to be an odd function.
        Thus f is odd if

        f (−x) = −f (x), for all x in the domain of f.
    """
    is_odd = all([_eval(func, -_x) == -_eval(func, _x) for _x in i])
    return is_odd


def function_type(func):
    """
        Module C1, Page 30

        Returns 'odd', 'even' or 'neither' for a given function
    """
    is_even = is_even_function(func)
    is_odd = is_odd_function(func)

    if is_even and not is_odd:
        ftype = 'even'
    if is_odd and not is_even:
        ftype = 'odd'
    if not is_odd and not is_even:
        ftype = 'neither'

    print "Function %s is %s" % (func, ftype)
    return ftype

def graph_sketching_strategy(func):
    """
        Module C1, Page 36

        Strategy: To sketch the graph of a given function f, determine the
        following features of f (where possible) and then show these features
        in your sketch.

        1.   The domain of f .
        2.   Whether f is even or odd.
        3.   The x- and y-intercepts of f .
        4.   The intervals on which f is positive or negative.
        5.   The intervals on which f is increasing or decreasing and any
             stationary points, local maxima and local minima.
        6.   The asymptotic behaviour of f .

    """

    # Step 2 - even or odd or neither? This isn't really that necessary
    # for this automated plot of the function but is nice to annotate
    # the graph with and will have to be shown in any TMA/exam working
    ftype = function_type(func)

    # Step 3 - intercepts are easy to work out with a bit of algebra
    # or evalutating it at x = 0

    y_intercepts = _eval(func, 0)  # y-intercept is solution(s) to f(0)
    x_intercepts = filter_reals(solve(func))  # x-intercepts is solution(s) to f(x) = 0

    # Step 4 - we need to find any poles (discontinuties). We can do that
    # symbolically by solving the equation 1/f(x) = 0. If f has a pole then
    # it will be a root of this equation
    poles = solve(1/func, x)

    # Now we'll check between these groups what the value of the function
    # is to determine if postive or negative in that region. Again this would
    # be obviously visible on the generated plot regardless but this is for
    # _sketching_ manually, so we want to summarise and work all this out
    # as if by hand too.
    points = [-oo, ] + poles + [oo, ]

    print """
        The function %(func)s is of type: %(ftype)s. The y-intercept
        are %(yints)r and the x-intercepts are %(xints)r.
    """ % {
        'func': func,
        'ftype': ftype,
        'yints': y_intercepts,
        'xints': x_intercepts,
    }

    return
