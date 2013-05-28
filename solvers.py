# -*- coding: utf-8 -*-

import unittest

from sympy import Symbol, symbols, Matrix, simplify, exp, oo, diff, limit, \
    integrate
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

        Sympy has built in solvers for nth-order recurrence sequences, see
        rsolve: http://docs.sympy.org/dev/modules/solvers/solvers.html#recurrence-equtions
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


# .        :       ...    :::::::-.   ...    ::: :::    .,::::::    :::::::-.
# ;;,.    ;;;   .;;;;;;;.  ;;,   `';, ;;     ;;; ;;;    ;;;;''''     ;;,   `';,
# [[[[, ,[[[[, ,[[     \[[,`[[     [[[['     [[[ [[[     [[cccc      `[[     [[
# $$$$$$$$"$$$ $$$,     $$$ $$,    $$$$      $$$ $$'     $$""""       $$,    $$
# 888 Y88" 888o"888,_ _,88P 888_,o8P'88    .d888o88oo,.__888oo,__     888_,o8P'
# MMM  M'  "MMM  "YMMMMMP"  MMMMP"`   "YmmMMMM""""""YUMMM""""YUMMM    MMMMP"`


class DivisibilityTests(object):
    """
        Module D2, Page 15 - 18

        Tests for dividing by a particular number up to 14. Now obviously
        just calling mod on x with m would do the same job but these spell
        out the steps explicitly as expected in the exam.
    """

    def __init__(self):
        pass

    def digits(self, number, reverse=True):
        """
            Returns the digits of number in order as a list. Many of the tests
            involve manipulating the supplied number in such a way
        """
        num_str = str(number)
        if reverse:
            num_str = reversed(num_str)

        return [int(x, 10) for x in num_str]

    def digit_sum(self, x, modulus):
        """
            Returns the sum of digits successivly until the sum is under
            9 - used for testing by 3, 9
        """

        _sum = sum(self.digits(x, reverse=False))
        print "\tDigit sum: %d" % _sum

        if _sum > 9:
            return self.digit_sum(_sum, modulus)
        else:
            r = _sum % modulus
            print "Finished, remainder: %d\n" % r
            return r

    def inflate_digits(self, x):
        """
            Takes a list of digits and returns the number they represent
            if in order of powers of 10, so [1, 2] becomes 21.
        """
        return sum([d * 10**i for i, d in enumerate(x)])

    def by_2(self, x):
        """
            A number is divisible by 2 if the _last_ digit is
            divisible by 2
        """
        return self.digits(x)[0] % 2

    def by_3(self, x):
        """
            Module D2, Page 15

            A simple test for divisibility by 3 involves forming the sum of
            the digits of the given number. If the resulting digit sum has
            more than one digit, then the process is repeated until a single
            digit remains. The original number is divisible by 3 if and only
            if this single digit is divisible by 3.
        """

        print "Dividing %d by 3" % x
        return self.digit_sum(x, 3)

    def by_4(self, x):
        """
            This just needs to check the last _two_ digits (as opposed to one
            in the case of by_2)
        """
        # Remember, the returned digits are reversed so we need the first two
        # (they're in order of size, 10**0, 10**1, 10**2, etc)
        last_two_digits = self.inflate_digits(self.digits(x)[:2])
        r = (last_two_digits)  % 4
        print "Dividing %d by 4 - check %d: %d" % (x, last_two_digits, r)
        return r

    def by_5(self, x):
        pass

    def by_6(self, x):
        """
            Module D2, Page 18

            This involves testing the remainder by 2 and 3 and then using that
            info to get the remainder mod 6. The module text suggests using
            the following congreuence:

                r6 ≡ 3r2 − 2r3 (mod 6).
        """
        r2, r3 = self.by_2(x), self.by_3(x)
        val = (3 * r2 - 2 * r3)
        r6 = val % 6
        print "Dividing %d by 6, congruence relation: %d gives %d" % (x, val, r6)
        return r6

    def by_7(self, x):
        pass

    def by_8(self, x):
        """
            This just needs to check the last _three_ digits - like by_4, by_2
        """
        last_three_digits = self.inflate_digits(self.digits(x)[:3])
        r = (last_three_digits)  % 8
        print "Dividing %d by 8 - check %d: %d" % (x, last_three_digits, r)
        return r

    def by_9(self, x):
        """
            Module D2, Page 16, Activity 2.2

            The digit sum method depends on congruences (2.1) and these
            congruences also hold modulo 9, because 10 ≡ 1 (mod 9). Therefore
            the digit sum method works for division by 9.
        """
        print "Dividing %d by 9" % x
        return self.digit_sum(x, 9)

    def by_11(self, x):
        """
            Module D2, Page 16

            This uses the fact that 10 ≡ −1 (mod 11), from which we deduce
            that 10k ≡ (−1)k (mod 11), for k = 1, 2, . . . .

            Therefore, if a = a0 + a1 × 10 + a2 × 102 + · · · + am × 10m ,
            then a ≡ a0 − a1 + a2 − · · · + (−1)m am (mod 11).

            a has the same remainder on division by 11 as the alternating digit
            sum, which starts with the _units_ digit.

            This *could* be really big and be repeatedly applied again and again
            much like the by_3, by_9 examples but we'll forget about that for
            the purposes of this!
        """

        print "Dividing %d by 11" % x

        # We start by getting the digits in the order of least signifigant first
        digits = self.digits(x, reverse=True)
        alternating_sum = sum([(-1)**i * d for i, d in enumerate(digits)])
        r = alternating_sum % 11

        print "Alternating sum: %d gives %d" % (alternating_sum, r)
        return r

    def by_12(self, x):
        """
            Module D2, Page 18

            This uses a similar technique to that of by_6 only using the
            tests for 3 and 4. This time we use the following relation:

                r12 ≡ 4r3 − 3r4 (mod 12)
        """

    def by_13(self, x):
        pass


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
        # Module B1 Page 28
        points = fixed_points(parse_expr('-1/8*x**2+5/8*x+7/2'))
        self.assertEqual(points[0], -7)
        self.assertEqual(points[1], 4)

    def test_classified_fixedpoints(self):
        # Module B1 Page 28
        points = classify_fixed_points(parse_expr('-1/8*x**2+5/8*x+7/2'))
        self.assertEqual(points[0][2], 'repelling')
        self.assertEqual(points[1][2], 'attracting')


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


class ModuleD_Tests(unittest.TestCase):

    def setUp(self):
        self.div_tester = DivisibilityTests()

    def test_inflater(self):
        self.assertEqual(self.div_tester.inflate_digits([1, 2]), 21)
        self.assertEqual(self.div_tester.inflate_digits([4, 4, 5]), 544)

    def test_divisibility_by_2(self):
        self.assertEqual(self.div_tester.by_2(50), 0)
        self.assertEqual(self.div_tester.by_2(3), 1)

    def test_divisibility_by_3(self):
        self.assertEqual(self.div_tester.by_3(61671142), 1)  # D2,p15
        self.assertEqual(self.div_tester.by_3(6341723110832864), 2)  # D2,p16

    def test_divisibility_by_4(self):
        self.assertEqual(self.div_tester.by_4(9338187834737), 1)
        self.assertEqual(self.div_tester.by_4(6341723110832864), 0)  # D2,p17

    def test_divisibility_by_6(self):
        self.assertEqual(self.div_tester.by_6(61671142), 4)  # D2,p18
        self.assertEqual(self.div_tester.by_6(98234278215), 3)

    def test_divisibility_by_8(self):
        self.assertEqual(self.div_tester.by_8(9898243523873937), 1)
        self.assertEqual(self.div_tester.by_8(6341723110832864), 0)  # D2,p17

    def test_divisibility_by_9(self):
        self.assertEqual(self.div_tester.by_9(10093), 4)
        self.assertEqual(self.div_tester.by_9(6341723110832864), 5)  # D2,p16

    def test_divisibility_by_11(self):
        self.assertEqual(self.div_tester.by_11(61671142), 5)  # D2,p16
        self.assertEqual(self.div_tester.by_11(6341723110832864), 7)  # D2,p17


if __name__ == '__main__':
    # Might as well run some tests!
    unittest.main()
