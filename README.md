# Open University Code

## About this code & who I am

Code that I write to help me work through my Open University degree. I have or am
studying the following modules:

* MST121 - Using Mathematics (Autumn 2011, pass, no other grade type)
* M248 - Analysing Data (Spring 2012, Grade 2 pass)
* MS221 - Exploring Mathematics (Currently studying - Autumn 2012)
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
_Machine Learning Library_ for Python.

