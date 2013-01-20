from shapely.geometry import LineString
from pylab import *

#     __  ___________  ___  ___
#    /  |/  / ___/__ \|__ \<  /
#   / /|_/ /\__ \__/ /__/ // /
#  / /  / /___/ / __// __// /
# /_/  /_//____/____/____/_/

#  :::     ::::::.    :::..,::::::   :::.    :::::::..
#  ;;;     ;;;`;;;;,  `;;;;;;;''''   ;;`;;   ;;;;``;;;;
#  [[[     [[[  [[[[[. '[[ [[cccc   ,[[ '[[,  [[[,/[[['
#  $$'     $$$  $$$ "Y$c$$ $$""""  c$$$cc$$$c $$$$$$c
# o88oo,.__888  888    Y88 888oo,__ 888   888,888b "88bo,
# """"YUMMMMMM  MMM     YM """"YUMMMYMM   ""` MMMM   "W"

# :::::::::::::::::::..    :::.   :::.    :::. .::::::. .-:::::'   ...    :::::::..   .        :
# ;;;;;;;;'''';;;;``;;;;   ;;`;;  `;;;;,  `;;;;;;`    ` ;;;'''' .;;;;;;;. ;;;;``;;;;  ;;,.    ;;;
#      [[      [[[,/[[['  ,[[ '[[,  [[[[[. '[['[==/[[[[,[[[,,==,[[     \[[,[[[,/[[['  [[[[, ,[[[[,
#      $$      $$$$$$c   c$$$cc$$$c $$$ "Y$c$$  '''    $`$$$"``$$$,     $$$$$$$$$c    $$$$$$$$"$$$
#      88,     888b "88bo,888   888,888    Y88 88b    dP 888   "888,_ _,88P888b "88bo,888 Y88" 888o
#      MMM     MMMM   "W" YMM   ""` MMM     YM  "YMmMY"  "MM,    "YMMMMMP" MMMM   "W" MMM  M'  "MMM

# ::::::::::::   ...         ...      :::     .::::::.
# ;;;;;;;;''''.;;;;;;;.   .;;;;;;;.   ;;;    ;;;`    `
#      [[    ,[[     \[[,,[[     \[[, [[[    '[==/[[[[,
#      $$    $$$,     $$$$$$,     $$$ $$'      '''    $
#      88,   "888,_ _,88P"888,_ _,88Po88oo,.__88b    dP
#      MMM     "YMMMMMP"   "YMMMMMP" """"YUMMM "YMmMY"

# Copyright (c) 2013 Jaymz Campbell

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def unit_square_transform(M='0, 3; 1, -1', saveas='/tmp/unit.png', show_fig=False):
    """
        Transforms the unit square with a given 2x2 matrix
        and plots the results. Returns the transformed points.
    """
    unit_square = ((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))
    square = LineString(unit_square)

    M = np.matrix(M)
    p = np.array([square.xy[0], square.xy[1]])
    t = [np.matrix(p[:, x]) * M for x in range(p.shape[1])]
    t = np.array(t).reshape(p.shape[1], 2).transpose()

    clf()

    plot(p[0, :], p[1, :], label='Unit square', marker='o')
    plot(t[0, :], t[1, :], label='Transformed', marker='o')

    max_i, max_j = np.unravel_index(abs(t).argmax(), t.shape)
    maxval = abs(t[max_i, max_j])

    limits = (-maxval - 2, maxval + 2)

    ylim(limits)
    xlim(limits)
    grid()
    legend()

    savefig(saveas)

    if show_fig:
        show()

    return t


def linear_sequence(m, initial, terms):
    """
        Returns up to item xn where n = terms + 1 of the linear recurrance
        sequence defined by matrix m using a specified initial term.
    """
    A = matrix(m)
    x0 = matrix(initial)
    vals = [A ** n * x0 for n in range(terms + 1)]
    return array(vals).reshape(terms + 1, 2).transpose()


def plot_sequence(m='5,7;-2,-4', initial='1;1', terms=4, saveas='/tmp/sequence.png', show_fig=False):
    seq = linear_sequence(m, initial, terms)

    clf()
    grid()
    plot(seq[0, :], seq[1, :], marker='o')

    savefig(saveas)

    if show_fig:
        show()
