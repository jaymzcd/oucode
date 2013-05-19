#!/usr/bin/env python2

import sys
from pylab import *
from sympy import Symbol
from sympy.printing import latex
from sympy.parsing.sympy_parser import parse_expr

from common import setup_mpl


def draw_plot(f, lower=-10, upper=-10, num=250):
    y = parse_expr(f)
    xvals = linspace(lower, upper, num=num)
    vals = [y.evalf(subs={'x': x}) for x in xvals]
    plot(xvals, vals)
    title('$%s$' % latex(y))
    grid()
    savefig('/tmp/plot.png')
    show()


if __name__=='__main__':
    setup_mpl()
    draw_plot(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
