# -*- coding: utf-8 -*-

import unittest

from sympy import exp, Matrix
from sympy.abc import x
from sympy.parsing.sympy_parser import parse_expr

from ms221.linear_recurrences import linear_second_order_recurrence
from ms221.function_tests import function_type
from ms221.divisibility_tests import DivisibilityTests
from ms221.eigen import matrix_eigenvalues, matrix_eigenlines, matrix_eigenvector
from ms221.fixed_points import classify_fixed_points, fixed_points


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

    def test_divisibility_by_5(self):
        self.assertEqual(self.div_tester.by_5(9338187834735), 0)
        self.assertEqual(self.div_tester.by_5(6341723110832864), 4)

    def test_divisibility_by_6(self):
        self.assertEqual(self.div_tester.by_6(61671142), 4)  # D2,p18
        self.assertEqual(self.div_tester.by_6(98234278215), 3)

    def test_divisibility_by_7(self):
        self.assertEqual(self.div_tester.by_7(61671142), 1)  # D2,p19
        self.assertEqual(self.div_tester.by_7(6341723110832864), 6) # D2,p42

    def test_divisibility_by_8(self):
        self.assertEqual(self.div_tester.by_8(9898243523873937), 1)
        self.assertEqual(self.div_tester.by_8(6341723110832864), 0)  # D2,p17

    def test_divisibility_by_9(self):
        self.assertEqual(self.div_tester.by_9(10093), 4)
        self.assertEqual(self.div_tester.by_9(6341723110832864), 5)  # D2,p16

    def test_divisibility_by_11(self):
        self.assertEqual(self.div_tester.by_11(61671142), 5)  # D2,p16
        self.assertEqual(self.div_tester.by_11(6341723110832864), 7)  # D2,p17

    def test_divisibility_by_13(self):
        self.assertEqual(self.div_tester.by_13(61671142), 0)  # D2,p19
        self.assertEqual(self.div_tester.by_13(6341723110832864), 1)  # D2,p42


if __name__ == '__main__':
    # Might as well run some tests!
    unittest.main()
