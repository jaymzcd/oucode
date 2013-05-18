#!/usr/bin/env sage

# import sage library
from sage.all_cmdline import *
_sage_const_1 = Integer(1)

import sys
from pylab import *
from subprocess import call


def cayley(x):
    """
        Generates a cayley table for Z_x and saves the output as a
        color coded image using matplotlib.
    """
    clf()
    Zx = Integers(x)  # Create integer ring of order x
    t = Zx.multiplication_table()
    table = t.table()
    imshow(table, interpolation='nearest')
    colorbar()
    fout = '/tmp/ring-%02d.png' % x
    savefig(fout)
    return fout, table


def show(f):
    """
        Helper to call feh to show output
    """
    call(['feh', f])


def grid(lower, upper):
    """
        Generate a montaged grid using imagemagick of cayley tables
        for integer rings from range lower to upper
    """
    for x in range(lower, upper):
        cayley(x)
        print "Created %d" % x

    call(['montage', '-label', '%f', '/tmp/ring-*.png', '-geometry', '300x', '-tile', '6x', '/tmp/rings.png'])


if __name__=='__main__':
    def _arg(x, default):
        try:
            return int(sys.argv[x], 10)
        except IndexError:
            return default

    grid(_arg(1, 2), _arg(2, 10))
