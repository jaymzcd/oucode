# -*- coding: utf-8 -*-

import unittest

from sympy import Symbol, symbols, Matrix, simplify, exp, oo
from sympy.abc import x
from sympy.parsing.sympy_parser import parse_expr
from sympy.printing import pretty_print, pretty
from sympy.solvers import solve, solvers

# .        :   .::::::.   .:::.    .:::.  :.
# ;;,.    ;;; ;;;`    `  ,;'``;.  ,;'``;. ;;
# [[[[, ,[[[[,'[==/[[[[, ''  ,[[' ''  ,[['[[
# $$$$$$$$"$$$  '''    $ .c$$P'   .c$$P'  $$
# 888 Y88" 888o88b    dPd88 _,oo,d88 _,oo,88
# MMM  M'  "MMM "YMmMY" MMMUP*"^^MMMUP*"^^MM
#
#  .::::::.     ...      :::  :::      .::..,:::::: :::::::..   .::::::.
# ;;;`    `  .;;;;;;;.   ;;;  ';;,   ,;;;' ;;;;'''' ;;;;``;;;; ;;;`    `
# '[==/[[[[,,[[     \[[, [[[   \[[  .[[/    [[cccc   [[[,/[[[' '[==/[[[[,
#   '''    $$$$,     $$$ $$'    Y$c.$$"     $$""""   $$$$$$c     '''    $
#  88b    dP"888,_ _,88Po88oo,.__Y88P       888oo,__ 888b "88bo,88b    dP
#   "YMmMY"   "YMMMMMP" """"YUMMM MP        """"YUMMMMMMM   "W"  "YMmMY"
#
# These are general solvers based on methods in the Handbook and throughout the
# MS221 course. They're designed to be step by step so that they show the
# general level of working for the activity & examples. In many cases there
# are functions within scipy/sympy/sage that can do these in one line but the
# point is to use it as a learning resource.
#
# Firstly by writing code to do these sorts of manipulations I get some more
# familiarity with using python for this sort of math and secondly it's like
# a note taking session of sorts converting the steps and algorithims in the
# handbook to working python code.
#
# Unit tests are included for methods with source data coming from activities
# and examples thoughout the module and exam resources.
#
#       ~jaymz / 2013
#
#
# Copyright (c) 2013, Jaymz Campbell
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

#  - Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#   ::   .: .,::::::   :::  ::::::::::. .,:::::: :::::::..   .::::::.
#  ,;;   ;;,;;;;''''   ;;;   `;;;```.;;;;;;;'''' ;;;;``;;;; ;;;`    `
# ,[[[,,,[[[ [[cccc    [[[    `]]nnn]]'  [[cccc   [[[,/[[[' '[==/[[[[,
# "$$$"""$$$ $$""""    $$'     $$$""     $$""""   $$$$$$c     '''    $
#  888   "88o888oo,__ o88oo,.__888o      888oo,__ 888b "88bo,88b    dP
#  MMM    YMM""""YUMMM""""YUMMMYMMMb     """"YUMMMMMMM   "W"  "YMmMY"


def filter_reals(vals):
    """
        In many cases we'll need to only consider real roots or intercepts so
        filter out any complex values when returning results
    """
    return [val for val in vals if val.is_real]


def _eval(func, x):
    """
        Evaluates the sympy function func for a given x
    """
    return func.evalf(subs={'x': x})


# Alias the sympy pretty function as pp for convinence
pp = pretty


# .        :       ...    :::::::-.   ...    ::: :::    .,::::::      :::.
# ;;,.    ;;;   .;;;;;;;.  ;;,   `';, ;;     ;;; ;;;    ;;;;''''      ;;`;;
# [[[[, ,[[[[, ,[[     \[[,`[[     [[[['     [[[ [[[     [[cccc      ,[[ '[[,
# $$$$$$$$"$$$ $$$,     $$$ $$,    $$$$      $$$ $$'     $$""""     c$$$cc$$$c
# 888 Y88" 888o"888,_ _,88P 888_,o8P'88    .d888o88oo,.__888oo,__    888   888,
# MMM  M'  "MMM  "YMMMMMP"  MMMMP"`   "YmmMMMM""""""YUMMM""""YUMMM   YMM   ""`


def linear_second_order_recurrence(p, q, _u0, _u1):
    """
        Module A1

        Solve a second order linear recurrence step by step using the method
        in the MS221 handbook and chapter A1 of the course. Some bits here
        are more explict than they would need to be by using Sympy so that
        each step is outlined.
    """

    # Initalize our symbols we'll be using
    r, A, B, n = symbols('r, A, B, n')

    # Create a the auxillary equation first
    aux = r ** 2 - p * r - q
    roots = solve(aux)

    # We've two options for the general solution based on if the root repeats
    if len(roots) == 2:
        print "Auxillary equation solutions (a, b) = (%s, %s)" % (pp(roots[0]), pp(roots[1]))
        general_solution = A * roots[0] ** n + B * roots[1] ** n
    else:
        print "Auxillary equation repeated root a = %s" % roots[0]
        general_solution = (A + B*n) * roots[0] ** n
        # Now for ease of referencing make the repeated root a list
        roots = roots * 2

    # Could use solvers.solve_linear_system but this spells
    # out the steps of the algebra for reference as if you
    # were doing it by hand

    # Evaluate u0 and u1 by substituting for n in the general solution
    u0 = general_solution.subs({'n': 0})
    u1 = general_solution.subs({'n': 1})

    # Solve for the given inital values _u0 & _u1. Sympy will return
    # a solution in terms of the variable A, it's a list so we need
    # the first value back
    b0, b1 = solve(u0 - _u0)[0], solve(u1 - _u1)[0]

    # If the above equations have a single variable they'll be integer
    # solutions, otherwise they'll be in terms of the variable A
    if type(b0) == dict:
        b0 = b0[A]
    if type(b1) == dict:
        b1 = b1[A]

    # Now solve the two simulataeous equations to get B
    _B = solve(b0 - b1)[0]
    # And replace this into one of the initial value equations
    # to get the value of A
    _A = b0.subs({'B': _B})

    print "A: %s\nB: %s\n" % (_A, _B)

    # Finally for the specific solution we replace our general solution
    # with the found values of A & B
    solution = general_solution.subs({'A': _A, 'B': _B})

    print "Solution:\n" + "%s\n" % pp(solution)
    return (roots, _A, _B), solution


# .        :       ...    :::::::-.   ...    ::: :::    .,::::::    :::::::.
# ;;,.    ;;;   .;;;;;;;.  ;;,   `';, ;;     ;;; ;;;    ;;;;''''     ;;;'';;'
# [[[[, ,[[[[, ,[[     \[[,`[[     [[[['     [[[ [[[     [[cccc      [[[__[[\.
# $$$$$$$$"$$$ $$$,     $$$ $$,    $$$$      $$$ $$'     $$""""      $$""""Y$$
# 888 Y88" 888o"888,_ _,88P 888_,o8P'88    .d888o88oo,.__888oo,__   _88o,,od8P
# MMM  M'  "MMM  "YMMMMMP"  MMMMP"`   "YmmMMMM""""""YUMMM""""YUMMM  ""YUMMMP"


def matrix_eigenvalues(m):
    """
        Module B3, page 14

        This is one example of something easier with just using the libaries!
        You could just do Matrix(m).eigen_values()! m should be a sympy
        Matrix, e.g. Matrix([[0, 1], [1, 0]]).
    """

    k = symbols('k')

    # To make it clearer, lets assign out the matrix elements
    a, b, c, d = m[0, 0], m[0, 1], m[1, 0], m[1, 1]
    # See B3 page 19, equation 2.5 for this definition
    characteristic_equation = k ** 2 - (a + d) * k + (a * d - b * c)
    roots = solve(characteristic_equation)

    print "Characteristic equation:\n\n%s\n" % pp(characteristic_equation)

    if len(roots) == 1:
        # Make dupe of repeated root
        roots = roots * 2

    if roots[0].is_real:
        print "Eigenvalues: %s\n" % pp(roots)
        return roots
    else:
        # Note that the statement 'no eigenvalues' is by definition
        print "Roots are complex, no eigenvalues"
        return None


def matrix_eigenlines(m):
    """
        Module B3, page 21
    """

    eigenvalues = matrix_eigenvalues(m)
    # Now make sure we've got something to work with!
    assert(eigenvalues is not None)

    # Now to work out the eignlines we use the eigenvector equation
    # Ax = kx where A is our matrix m, k is a particular eigenvalue
    # and x represents the (x, y) vector
    x, y = symbols('x, y')
    x_vector = Matrix([x, y])

    eigenlines = list()
    for eigenvalue in eigenvalues:
        # Now we evaluate Ax = kx, since we can't do a 'a = b' style expression
        # in sympy/python we subtract the right hand side so we are basically
        # skipping a small step and writing Ax - kx = 0
        equations = m * x_vector - eigenvalue * x_vector
        print "Set of equations for eigenvalue %s:\n\n%s" % (eigenvalue, pp(equations))

        # For a given eigenvalue the equations returned above both reduce
        # to the same expression, so we can pick the first one, simplify it
        # down to the lowest terms. Then we solve for y which basically
        # rearranged it into standard form. This is the eigenline equation.
        # As we're dealing with solve, we take the first (only) result
        eigenline = solve(simplify(equations[0]), y)[0]
        print "Eigenline equation for eigenvalue %s:\n\n%s\n" % (eigenvalue, pp(eigenline))
        eigenlines.append(eigenline)

    return eigenlines

def matrix_eigenvector(m, line=0, x=1):
    """
        Module B3, page 22

        Returns a possible eigenvector for eigenline #line, usually by
        evaluting x = 1 but this can be changed on demand to get a
        particular eigenvector
    """
    # First we need to get the eigenlines for the matrix
    eigenlines = matrix_eigenlines(m)
    # Now evaluate the equation of the line
    val = eigenlines[line].subs({'x': x})
    # Finally the eigenvector is simply the given x value with the
    # evaluated y value from above in vector form
    eigenvector = Matrix([x, val])

    print 'Eigenvector for eigenline %s (x=%0.2f):\n\n%s\n' % (eigenlines[line], x, pp(eigenvector))
    return eigenvector

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
    points = [oo, ] + poles + [oo, ]

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


# ::::::::::::.,:::::: .::::::.:::::::::::: .::::::.
# ;;;;;;;;'''';;;;'''';;;`    `;;;;;;;;'''';;;`    `
#      [[      [[cccc '[==/[[[[,    [[     '[==/[[[[,
#      $$      $$""""   '''    $    $$       '''    $
#      88,     888oo,__88b    dP    88,     88b    dP
#      MMM     """"YUMMM"YMmMY"     MMM      "YMmMY"
#
# These are taken from the various examples, activities and TMA/past papers
# so that they should be pretty well vetted in the first place! References
# to page numbers correspond to the course texts supplied as PDFs.

class ModuleA_Tests(unittest.TestCase):

    def test_lin2ndrec_different_roots(self):
        # Module A1 Page 24
        p, q, u0, u1 = 12, -20, 3, 22
        (roots, A, B), soln = linear_second_order_recurrence(p, q, u0, u1)
        self.assertEqual(roots[0], 2)
        self.assertEqual(roots[1], 10)
        self.assertEqual(A, 1)
        self.assertEqual(B, 2)

    def test_lin2ndrec_repeated_roots(self):
        # Module A1 Page 25
        p, q, u0, u1 = 4, -4, 3, 8
        (roots, A, B), soln = linear_second_order_recurrence(p, q, u0, u1)
        self.assertEqual(roots[0], 2)
        self.assertEqual(roots[1], 2)
        self.assertEqual(A, 3)
        self.assertEqual(B, 1)


class ModuleB_Tests(unittest.TestCase):

    def test_real_eigenvalues(self):
        # Module B3 Page 20, Example 2.1 a
        m = Matrix([[2, 1], [3, 4]])
        eigenvals = matrix_eigenvalues(m)
        self.assertEqual(eigenvals[0], 1)
        self.assertEqual(eigenvals[1], 5)

    def test_no_eigenvalues(self):
        # Module B3 Page 20, Example 2.1 b
        m = Matrix([[-2, 7], [-1, 3]])
        eigenvals = matrix_eigenvalues(m)
        self.assertIsNone(eigenvals)

    def test_eigenline(self):
        # Module B3 Page 21, sample problem
        m = Matrix([[1, 2], [3, 2]])
        eigenlines = matrix_eigenlines(m)
        self.assertEqual(eigenlines[0], parse_expr('-1 * x'))
        self.assertEqual(eigenlines[1], parse_expr('3/2 * x'))

    def test_eigenvector(self):
        # Module B3 Page 22, sample problem
        m = Matrix([[1, 2], [3, 2]])
        eigenvector = matrix_eigenvector(m, line=1, x=2)
        self.assertEqual(eigenvector, Matrix([2, 3]))

    def test_fixedpoints(self):
        # Module B1 Page 26
        points = fixed_points(parse_expr('x**2 + 1/8'))
        self.assertEqual(points[0], parse_expr('1/2 - 1/4 * sqrt(2)'))
        self.assertEqual(points[1], parse_expr('1/2 + 1/4 * sqrt(2)'))


class ModuleC_Tests(unittest.TestCase):

    def test_function_types(self):
        # Module C1 Page 30, 37, 38, 39

        funcs = {
            x ** 2: 'even',
            x: 'odd',
            (2 * x - 3) / (x - 1): 'neither',
            x / (x**2 + 1): 'odd',
            (x - 2) * exp(x): 'neither',
        }

        for func in funcs:
            self.assertEqual(function_type(func), funcs[func])


if __name__=='__main__':
    # Might as well run some tests!
    unittest.main()
