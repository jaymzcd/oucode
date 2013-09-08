#!/usr/bin/env python2
#
#   .,-:::::/ .,:::::::::.    :::..,:::::::::::::::::::::  .,-:::::
# ,;;-'````'  ;;;;''''`;;;;,  `;;;;;;;'''';;;;;;;;'''';;;,;;;'````'
# [[[   [[[[[[/[[cccc   [[[[[. '[[ [[cccc      [[     [[[[[[
# "$$c.    "$$ $$""""   $$$ "Y$c$$ $$""""      $$     $$$$$$
#  `Y8bo,,,o88o888oo,__ 888    Y88 888oo,__    88,    888`88bo,__,o,
#    `'YMUP"YMM""""YUMMMMMM     YM """"YUMMM   MMM    MMM  "YUMMMMMP"
#   :::.      :::      .,-:::::/      ...    :::::::..   ::::::::::::::: ::   .:  :::.        :   .::::::.
#   ;;`;;     ;;;    ,;;-'````'    .;;;;;;;. ;;;;``;;;;  ;;;;;;;;;;;'''',;;   ;;, ;;;;;,.    ;;; ;;;`    `
#  ,[[ '[[,   [[[    [[[   [[[[[[/,[[     \[[,[[[,/[[['  [[[     [[    ,[[[,,,[[[ [[[[[[[, ,[[[[,'[==/[[[[,
# c$$$cc$$$c  $$'    "$$c.    "$$ $$$,     $$$$$$$$$c    $$$     $$    "$$$"""$$$ $$$$$$$$$$$"$$$  '''    $
#  888   888,o88oo,.__`Y8bo,,,o88o"888,_ _,88P888b "88bo,888     88,    888   "88o888888 Y88" 888o88b    dP
#  YMM   ""` """"YUMMM  `'YMUP"YMM  "YMMMMMP" MMMM   "W" MMM     MMM    MMM    YMMMMMMMM  M'  "MMM "YMmMY"
#
# This is code to do some very basic GA things. I could use PyEvolve or PyGene
# or something like that and would/will for anything more complicated or
# practical. However the purpose of all this is working through the
# examples/tmas/papers to get a better understanding of the material. More 'pen
# and paper' than serious.
#
# If SHOW_MESSAGES is true then this will generate a pretty markdown file detailing
# the complete evolution of the population specified in the __main__ method

from __future__ import division
from random import random, randint

# Bit messy - this is going to basically write out my first TMA question
# but I might want to switch that off when using the functions elsewhere
SHOW_MESSAGES = True


def convert_frombitstring(x):
    """
        Convert '0110' into [0, 1, 1, 0]
    """
    return [int(b) for b in x]


def convert_fromlist(l):
    """
        Convert [0, 1, 1, 0] into '0110'
    """
    return ''.join([str(i) for i in l])


def convert_population_tolist(p):
    """
        Loops over a list of population bitstrings and returns them split
        into integer lists
    """
    population = []
    for gene in p:
        population.append(convert_frombitstring(gene))
    return population


def convert_population_tobitstring(p):
    """
        Loops over a list of population lists and returns bitstrings which
        are friendlier to input and output for the end user
    """
    population = []
    for gene in p:
        population.append(convert_fromlist(gene))
    return population


def biased_roulette_wheel(population, fitness_values):
    """
        Calculates the proportion based on fitness of each gene for passing
        into the selection process and the mating pool
    """

    proportions = []
    total = sum(fitness_values)
    for val in fitness_values:
        proportions.append(val/total)

    if SHOW_MESSAGES:
        print "For the fitness values: `%r` the proportions for each gene are:\n" % fitness_values
        for i, gene in enumerate(population):
            print "* %s: %0.3f%%" % (gene, proportions[i])
        print "\n"

    return proportions


def cumulative_proportions(proportions):
    """
        Returns the proportions summed up to each point to make calculating
        which one bins a given random value easier
    """
    return [sum(proportions[:i + 1]) for i, x in enumerate(proportions)]


def mating_pool(population, proportions):
    """
        Use the given proportions to select at random genes from
        the given population.
    """

    # generate a list of random percentages which are then used to select
    # genes using the random module. we'll need to select the same amount
    # of genes that is in the initial population. Using cumulative proportions
    # will make the selection much easier to deal with by filtering on a
    # particular bound

    population_size = len(population)
    selection_bounds = [random() for i in range(0, population_size + 1)]
    props = cumulative_proportions(proportions)

    # Get the index of where False first occurs in the list for if a given
    # proportion is less than the bound; if it is less than it then False will
    # first occur at the index which corresponds to the gene with that
    # particular proportion of the biased roulette wheel
    #
    # Oneliner:
    # indexes = [[proportion < bound for proportion in props].index(False) for bound in selection_bounds]

    indexes = []
    for bound in selection_bounds:
        filtered = [proportion < bound for proportion in props]
        gene_index = filtered.index(False)
        indexes.append(gene_index)

        if SHOW_MESSAGES:
            print "* Random value: %0.3f,  selected gene: %s" % (bound, population[gene_index])

    return [population[index] for index in indexes]


def mutate(bit, likelyhood=0.1):
    """
        Randomly mutate a bit dependant on a given likelyhood. Bits are 1 or 0
        so we cast this to a boolean then not that and recast back to integer.
        If we don't need to mutate we just return the bit untouched
    """
    die = random()
    should_mutate = die < likelyhood

    verb = 'stays'

    if should_mutate:
        bit = int(not(bool(bit)))
        verb = 'changes to'

    if SHOW_MESSAGES:
        print "* For %r, random number is %0.3f, should mutate is %r, bit %s %r" % (bit, die, should_mutate, verb, bit)

    return bit


def mutate_population(population, rate=0.1):
    """
        Mutate a given population subject to a particular rate
    """

    # First convert our given bitstrings into lists that are easier to deal
    # with, we'll convert back before returning
    pop = convert_population_tolist(population)
    mutated_pop = []
    for gene in pop:

        if SHOW_MESSAGES:
            print "### %s\n" % convert_fromlist(gene)
            print "Gene input: `%s`\n" % convert_fromlist(gene)

        mutated_gene = [mutate(bit, likelyhood=rate) for bit in gene]

        if SHOW_MESSAGES:
            print "\nMutated output: `%s`\n" % convert_fromlist(mutated_gene)

        mutated_pop.append(mutated_gene)

    return convert_population_tobitstring(mutated_pop)


def crossover_genes(gene_1, gene_2):
    assert(len(gene_1) == len(gene_2))
    crossover_point = randint(0, len(gene_1) - 1)

    if SHOW_MESSAGES:
        print "Crossover point for Gene 1 `%s` and Gene 2 `%s` is %d\n" % (gene_1, gene_2, crossover_point)

    gene_1 = convert_frombitstring(gene_1)
    gene_2 = convert_frombitstring(gene_2)

    gene_1x = gene_1x_a = gene_1[:crossover_point]
    gene_1x_b = gene_1[crossover_point:]
    gene_2x = gene_2x_a = gene_2[:crossover_point]
    gene_2x_b = gene_2[crossover_point:]

    if SHOW_MESSAGES:
        print "* Gene 1 fragment A: `%s`, Gene 2 fragment B: `%s`" % (convert_fromlist(gene_1x_a), convert_fromlist(gene_2x_b))
        print "* Gene 2 fragment A: `%s`, Gene 1 fragment B: `%s`" % (convert_fromlist(gene_2x_a), convert_fromlist(gene_1x_b))

    gene_1x.extend(gene_2x_b)
    gene_2x.extend(gene_1x_b)

    gene_1x = convert_fromlist(gene_1x)
    gene_2x = convert_fromlist(gene_2x)

    if SHOW_MESSAGES:
        print "\nNew genes are Child 1 `%s` and Child 2 `%s`\n" % (gene_1x, gene_2x)

    return [gene_1x, gene_2x]


def crossover_population(population, rate=0.5):
    """
        Crosses over genes in the population at a given rate. We need to "dip into"
        the mating pool enough times to create a population of the same size as the
        one input. Each time we take out 2 genes
    """
    crossed_population = []
    population_size = len(population)
    population_index_size = population_size - 1

    if SHOW_MESSAGES:
        print "Crossing over population of size %d.\n" % population_size

    def _select_genes(limit):
        assert(limit > 1)

        genes = []
        for i in range(limit):
            gene_index = randint(0, population_index_size)
            genes.append(population[gene_index])
        return genes

    cnt = 1
    while len(crossed_population) < population_size:

        # Select 2 genes for the potential crossover
        gene_1, gene_2 = _select_genes(2)

        # Roll our die and decide if we should cross over based on the input
        # gene crossover rate
        die = random()
        should_crossover = die < rate

        if should_crossover:
            if SHOW_MESSAGES:
                print "Random number #%d is %0.3f and rate is %0.3f, applying crossover to genes:\n" % (cnt, die, rate)
            # Get 2 new genes crossed over at a random point
            new_genes = crossover_genes(gene_1, gene_2)
            crossed_population.extend(new_genes)
        else:
            # Or just extend the 2 selected genes to the new population
            if SHOW_MESSAGES:
                print "Random number #%d is %0.3f and rate is %0.3f, skipping crossover and adding genes to generation unaltered.\n" % (cnt, die, rate)
            crossed_population.extend([gene_1, gene_2])

        cnt += 1

    if len(crossed_population) > population_size:
        # If we have an extra one (we add 2 genes each time, so if the
        # population is an odd size) then we need to remove one
        crossed_population = crossed_population[: population_size]

    return crossed_population


if __name__ == '__main__':

    population = [
        '01111010',
        '11001101',
        '00010111',
        '10000101',
        '00001101',
        '11110011',
    ]

    def fitness_func(gene):
        """
            A dummy function that just uses the inital supplied data to
            return the fitness of a given gene
        """
        vals = [84, 12, 55, 66, 68, 43]
        index = population.index(gene)
        return vals[index]

    initial_fitness = [fitness_func(gene) for gene in population]

    if SHOW_MESSAGES:
        print "# Genetic Algorithims - Evolution of populations\n"
        print "## Inital population"

        data = zip(population, initial_fitness)
        for i, (p, f) in enumerate(data, 1):
            print "* Gene S%d: `%s`, fitness: *%d*" % (i, p, f)

        print "\n## Roulette Wheel Selection\n"

    proportions = biased_roulette_wheel(population, initial_fitness)

    if SHOW_MESSAGES:
        print "With the proportions calculated we can now use random numbers to decide"
        print "which of the genes will make it through to the mutation and crossover"
        print "stages and ultimately the next generation.\n"

    new_population = mating_pool(population, proportions)

    if SHOW_MESSAGES:
        print "\n## Population Mutation\n\n"

    mutated_population = mutate_population(population)

    if SHOW_MESSAGES:
        print "## Population Crossover\n\n"

    crossed_population = crossover_population(mutated_population)

    if SHOW_MESSAGES:
        print "## Next Generation\n\n"
        print "Evolution of the population is complete. The new generation is as follows:\n"
        print "\n".join(["* %s" % x for x in crossed_population])
