# -*- coding: utf-8 -*-
from shapely.geometry import LineString
from sympy import latex
from pylab import *

from common import setup_mpl

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

# Some matplotlib housekeeping
setup_mpl()


class StandardShapes(object):
    unit_square = ((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))


class LinearTransform(object):
    """
        A base class to do general linear transforms on shapes or more generally
        sets of points. Some of the work here is more explicit to show the
        detail and revise over the course material.

        Plotting is handled using matplotlib. When matrices or sets of points
        from shapely LineString's are to be shown they are cast to np.array's.
        This creates proper connecting lines between them, otherwise matplotlib
        will show simply the distinct points which is much harder to visualize.

        Sequences can be calculated & plotted from an initial term for any
        given number of terms.

        In most cases returned results are numpy arrays
    """

    def __init__(M):
        self.m = self.set_matrix(M)


    def set_matrix(self, M):
        """
            Try and handle variable convinent ways to define the matrix.
            For strings this is the usual 'a, b; c, d' format. Alternatively
            pass as a list of (x, y) tuples.
        """

        if type(M) in (str, tuple):
            self.m = np.matrix(M)
        else:
            self.m = M


    def linear_transform(self, shape, M=None):
        """
            Transforms a general set of points shape using matrix M returning
            the transformed points
        """

        if M is not None:
            m = np.matrix(M)
        else:
            m = self.m

        transformed = m * shape
        transformed = np.array(transformed)

        return transformed


    def plot_points(self, sets, saveas='/tmp/unit.png', clear=False, show_legend=False):
        """
            Show the given sets on a plot with grid. Note that your figures will
            'overprint' on each other unless you explicitly clear the figure. The
            limits are set to the same scale and will bound the largest point
            present so all of the transform should be visible.
        """

        if clear:
            clf()

        max_pt = 0  # The limits will be set to +/-2 this to give a square grid

        for s in sets:
            points, label = s['points'], s['label']
            plot(points[0, :], points[1, :], label=label, marker='o')

            cur_max_pt= points[np.unravel_index(abs(points).argmax(), points.shape)]

            if cur_max_pt > max_pt:
                max_pt = cur_max_pt

        limits = (-max_pt - 2, max_pt + 2)

        ylim(limits)
        xlim(limits)
        grid()

        if show_legend:
            legend()


    def unit_square_transform(self, M=None):
        """
            Transforms the unit square with a given 2x2 matrix
        """
        self.shape_transform(StandardShapes.unit_square, M=M, shape_label='Unit Square')


    def convert_shape(self, shape):
        """
            Converts a shape into a matrix suitable for the transform
        """

        converted = np.matrix(shape)
        if type(shape) == tuple:
            # If we build the matrix from sets of points as tuples we'll
            # need to finish by transposing it so the next step applies
            converted = converted.transpose()

        return np.array(converted)


    def shape_transform(self, shape, M=None, shape_label='Shape'):
        """
            Plots a general shape transformed by matrix M
        """
        shape = self.convert_shape(shape)
        transformed = self.linear_transform(shape, M=M)

        sets = [
            {
                'label': shape_label,
                'points': shape,
            }, {
                'label': 'Transformed',
                'points': transformed,
            },
        ]
        self.plot_points(sets)

        return sets


    def linear_sequence(self, initial, terms):
        """
            Returns up to item xn where n = terms + 1 of the linear recurrance
            sequence defined by matrix m using a specified initial term.
        """
        A = matrix(self.m)
        x0 = matrix(initial)
        vals = [A ** n * x0 for n in range(terms + 1)]
        return array(vals).reshape(terms + 1, 2).transpose()


    def plot_sequence(self, initial='1;1', terms=4, plot_title=None):
        """
            Plots terms of the transform M starting from a given initial term
            on a chart
        """
        seq = self.linear_sequence(initial, terms)

        clf()
        grid()

        if plot_title is None:
            title('$%d$ terms of the linear transform matrix for %s' % (terms, self.m))

        plot(seq[0, :], seq[1, :], marker='o')


class AngleBasedTransform(LinearTransform):
    """
        Base class for reflection & rotation transforms that are based
        on an angle as parameter
    """

    def __init__(self, theta):
        """
            Module B2, Page 13

            Draws _shape_ transformed by a reflection using matrix defined as:

              [ cos(2θ), sin(2θ)
                sin(2θ), -cos(2θ) ]
        """
        self.theta = theta
        self.set_matrix(theta)


    def set_matrix(self, m):
        super(AngleBasedTransform, self).set_matrix(m)


    def plot_line(self):
        """
            Plots the line going through the angle theta used in the transform.
        """
        x = linspace(-5, 5)
        plot(x, x * tan(self.theta))


class ReflectionTransform(AngleBasedTransform):
    """
        A reflection transform with parameter theta. This will reflect
        shapes in the line that makes angle 2θ with the x-axis & origin.
    """

    def set_matrix(self, theta=None):

        if theta is None:
            theta = self.theta

        m = ((cos(2*theta), sin(2*theta)), (sin(2*theta), -cos(2*theta)))
        super(ReflectionTransform, self).set_matrix(m)


class RotationTransform(AngleBasedTransform):
    """
        A rotation transform with parameter theta. This takes transforms
        shapes by rotating them by theta degrees (in radians).
    """

    def set_matrix(self, theta=None):

        if theta is None:
            theta = self.theta

        m = ((cos(theta), -sin(theta)), (sin(theta), cos(theta)))
        super(RotationTransform, self).set_matrix(m)
