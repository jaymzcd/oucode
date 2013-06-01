# -*- coding: utf-8 -*-

from sympy import Symbol, symbols, Matrix, simplify, exp, oo, diff, limit, \
    integrate
from sympy.printing import pretty_print as pp
from sympy.solvers import solve


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

