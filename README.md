# Open University Code

Code that I write to help me work through my Open University degree. I have or am
studying the following modules:

* MST121 (pass)
* M248 (Grade 2 pass)
* MS221 (Current)
* M336 (Current)

As a linux & python user I tend to do most of my work using [scipy](http://scipy.org)
within pylab. In addition I make use of [sympy](http://sympy.org). I do my formal
writing using [lyx](http://lyx.org).

![ou](http://www.open.ac.uk/includes/headers-footers/oulogo-56.jpg)

You can find some more about me on a rather stale blog at [jaymz.eu](http://jaymz.eu)

## MS221

### Linear transforms

Python code to (so far):

* Transform the unit square with an abritary 2x2 matrix and plot result
* Generate terms of a linear recurrance relation with given transform & inital term

Matplotlib provides output diagrams as PNGs:


![sequence example](http://i.imgur.com/4HneFIB.png)
![transform example](http://i.imgur.com/vRCDAAh.png)

### Function plots

Simple function plots of single parameter. The expression parsing is handled using
[sympy](http://docs.sympy.org/dev/modules/parsing.html). This is also used
to create Latex titles for matplotlib.

    plot_func.py "x**3-x**2+x-3+100*cos(10*x)" -10 10

![plot example](http://i.imgur.com/hafUmYy.png)

### Cayley tables for integer rings

Uses sage & matplotlib to visualize a multiplcation table for integer rings. That
is the remainders mod X for integers up to X. Imagemagick is used to montage
the resultant files together for comparassion.

By setting `exclude_zero` to `True` the 0-row will not be shown.

![ring 13](http://i.imgur.com/YzAn6jV.png)

![rings](http://i.imgur.com/FEud05mh.png)

### Handbook/Module Solvers

The code within the `solvers.py` module are a variety of functions that tackle
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

## M248 & MST121

I completed these prior to doing much so there's no code relating to these modules.

## M336

This AI course has yet to begin formally. The language used within it is _netlogo_.
Hopefully I'll end up trying some of the ideas and concepts around neural nets
in python using existing libraries and numpy.

