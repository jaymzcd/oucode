# Open University Code

## About this code & who I am

Code that I write to help me work through my Open University degree. I have or am
studying the following modules:

* MST121 - Using Mathematics (Autumn 2011, pass, no other grade type)
* M248 - Analysing Data (Spring 2012, Grade 2 pass)
* MS221 - Exploring Mathematics (Autumn 2012, Distinction)
* M336 - Artifical & Natural Intelligence (Currently studying - Spring 2013)

As a linux & python user I tend to do most of my work using [scipy](http://scipy.org)
within pylab. In addition I make use of [sympy](http://sympy.org). I do my formal
writing using [lyx](http://lyx.org). In the coming years I'm aiming to the following
in this order (availability permitting):

* M208 - Pure Mathematics (October 2013)
* MT365 - Graphs, networks and design (Spring 2014)
* MST210 - Mathematical methods, models and modelling (October 2014)
* SM358 - The quantum world (October 2015)
* M381 - Number theory and mathematical logic (Spring 2016)
* M336 - Groups and geometry (October 2016)


![ou](http://www.open.ac.uk/includes/headers-footers/oulogo-56.jpg)

Here I am at [Colossus](http://en.wikipedia.org/wiki/Colossus_computer) recently at
the [National Museum of Computing](http://www.tnmoc.org/).

![me at colossus](http://i.imgur.com/OZDz6Uw.png)

You can find some more about me on a rather stale blog at [jaymz.eu](http://jaymz.eu)

## Code by course

### MS221

#### Linear transforms

Classes to do general linear transforms and visualize the output, including:

* Transform the unit square with an abritary 2x2 matrix and plot result
* Generate terms of a linear recurrance relation with given transform & inital term

Matplotlib provides output diagrams as PNGs:

![sequence example](http://i.imgur.com/XIPeNek.png)

![transform example](http://i.imgur.com/vRCDAAh.png)

A `RotationTransform` and `ReflectionTransform` allow for specifing a given matrix
simply by providin the parameter _theta_. These inherit from the base `LinearTransform`
class so examining the effect on the unit square is easily visualised. For example:

```Python
    from helpers.linear_transforms import RotationTransform
    from sympy import pi
    r_pi4 = RotationTransform(pi/4)
    r_pi4.unit_square_transform()
    r_pi4.plot_line()
```

Using `plot_line` will draw the linear function whose gradient corresponds to the
tangent of the angle theta.

![reflection example](http://i.imgur.com/HsR0nmL.png)

![rotation example](http://i.imgur.com/fmXJWVW.png)

#### Function plots

Simple function plots of single parameter. The expression parsing is handled using
[sympy](http://docs.sympy.org/dev/modules/parsing.html). This is also used
to create Latex titles for matplotlib.

    plot_func.py "x**3-x**2+x-3+100*cos(10*x)" -10 10

![plot example](http://i.imgur.com/hafUmYy.png)

#### Cayley tables for integer rings

These are to be found within `number_theory/intring.py`.

Uses sage & matplotlib to visualize a multiplcation table for integer rings. That
is the remainders mod X for integers up to X. Imagemagick is used to montage
the resultant files together for comparassion.

By setting `exclude_zero` to `True` the 0-row will not be shown.

![ring 13](http://i.imgur.com/YzAn6jV.png)

![rings](http://i.imgur.com/FEud05mh.png)

#### Handbook/Module Solvers

The code within the MS221 module are a variety of functions that tackle
various key bits within the course in terms of the step by step solutions and
methods that you would work through. For example calculating eigenlines and values
for a particular matrix is very easy with sympy but rather than using a one line
built in library function the entire method is worked out as it is within
the course text.

This makes them a bit more useful for learning and testing / comparing work
with any examples rather than just those within the course texts or past papers.
There is code to deal with:

* Linear second order recurrences - closed forms
* Matrix eigen _values, lines, vectors_
* Graph sketching - function properties such as if even or odd,
  discontinuties, ranges and so on.
* Fixed points and cycles, classifications of such points as repelling,
  attracting, super-attracting etc.

Run `ms221_tests.py` to check a variety of sample questions - most of which
come from the various activities & excercises throughout the course.

```python

    from ms221.linear_recurrences import linear_second_order_recurrence
    from ms221.function_tests import function_type
    from ms221.divisibility_tests import DivisibilityTests
    from ms221.eigen import matrix_eigenvalues, matrix_eigenlines, matrix_eigenvector
    from ms221.fixed_points import classify_fixed_points, fixed_points
```

    Ran 20 tests in 0.461s
    OK


### M248 & MST121

I completed these prior to doing much so there's no code relating to these modules.

### M366

For this I'm making use of [PyBrain](http://pybrain.org/), a modular
_Machine Learning Library_ for Python as well as [JavaNNS](http://www.ra.cs.uni-tuebingen.de/software/JavaNNS/)
and [Netlogo](http://ccl.northwestern.edu/netlogo/) - both of which are used as
teaching and research tools on the course.

The code is a bit more specific than the more general stuff in the pure maths
modules so is perhaps not that suited for others use without being prepared
to hack on it.

#### JavaNNS Pattern (.PAT) to Numpy Array

The function `parse_pat` provides a means to read in pattern files for JavaNNS
and convert them into a numpy array - the benefit of this then is intutive slicing
and mapping operations across the entire matrix.

It assumes that the data begins after the last row specifing a number of units.

For example the following file:

    SNNS pattern definition file V3.2
    generated at Mon Apr 25 18:08:50 1994

    # For use in M366 2009B TMA03 Question 1

    No. of patterns : 15
    No. of input units : 2
    No. of output units : 3

    # Al   RfI  C1    C2    C3
    0.246   0.478   1   0   0
    0.239   0.608   1   0   0
    0.100   0.874   1   0   0
    0.299   0.513   1   0   0
    0.310   0.470   1   0   0
    0.367   0.384   0   1   0
    0.264   0.349   0   1   0
    0.356   0.332   0   1   0
    0.370   0.332   0   1   0
    0.335   0.349   0   1   0
    0.608   0.547   0   0   1
    0.552   0.900   0   0   1
    0.445   0.676   0   0   1
    0.619   0.263   0   0   1
    0.900   0.100   0   0   1

Results in an numpy array thus:

    (array([[ 0.246,  0.478],
           [ 0.239,  0.608],
           [ 0.1  ,  0.874],
           [ 0.299,  0.513],
           [ 0.31 ,  0.47 ],
           [ 0.367,  0.384],
           [ 0.264,  0.349],
           [ 0.356,  0.332],
           [ 0.37 ,  0.332],
           [ 0.335,  0.349],
           [ 0.608,  0.547],
           [ 0.552,  0.9  ],
           [ 0.445,  0.676],
           [ 0.619,  0.263],
           [ 0.9  ,  0.1  ]]),
     array([[ 1.,  0.,  0.],
           [ 1.,  0.,  0.],
           [ 1.,  0.,  0.],
           [ 1.,  0.,  0.],
           [ 1.,  0.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.],
           [ 0.,  0.,  1.],
           [ 0.,  0.,  1.],
           [ 0.,  0.,  1.],
           [ 0.,  0.,  1.]]))

#### Partitioning of input space

This is useful to visualize if a single layer perceptron is going to be any use
in classifying a given set of data.

![partitioning](http://i.imgur.com/bnLAuNg.png)

#### Assessment of validation table

The `validation_table_assess` function uses the strategy suggested in Block 4
to judge the effectivness of the networks perfomance according to the following
rules:

* score 1 for a correct response
* score -1 for an incorrect response
* score 0 for an _ambiguous_ response

Ambiguity is defined as comparing the other output responses and calculating
the difference between this and the chosen 'correct' response. Then:

* if the chosen response is the _true correct_ one and absolute differences are within threshold
* or the chosen response is _not the true correct_ and the absolute difference is within a second threshold

Then the score is defined to be 0. The scores can then be summed and divided by
the total to yield a percentage that refelcts the ability of the network to
effectivly classify data. If this is compared to the error graph within JavaNNS
when a data set is validated against a pre-trained network the figures should
over time agree quite closely (within a few %).

#### Genetic Algorithims

Within the `genetic_algorithims.py` file is code to mutate and crossover a supplied
population of bitstrings. This was created mainly whilst working through TMA04
so it uses a supplied list of inital fitness values for the population through
a dummy function. Replacing this with a real fitness calculation turns this into
actual working GA evolution code, albeit very simply implemented.
