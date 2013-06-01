# -*- coding: utf-8 -*-

from sympy import Symbol, symbols, Matrix, simplify, exp, oo, diff, limit, \
    integrate
from sympy.solvers import solve
from sympy.printing import pretty_print as pp

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