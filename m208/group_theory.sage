#!/usr/bin/env sage

from sage.all import *
from sage.matrix.operation_table import OperationTable


def table_for_set(S, op):
    """
        Return a table for the set combined with a binary operation using
        the elements as the labels rather than letters
    """

    return OperationTable(S, operation=op, names=[str(x) for x in S])


def modulus_operation(base):
    """
        Create a function that returns the modulus
        of a given input number
    """
    return lambda x: mod(x, base)

def binary_mult_op(op):
    """
        Create a binary operator that applies the multiplcatation of 2 elements
        as it's argument
    """
    return lambda a, b: op(a * b)
