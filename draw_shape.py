from shapely.geometry import LineString
from pylab import *

from common import setup_mpl


def draw_shape(coords):
    _coords = coords + (coords[0], )  # Make complete loop
    pts = LineString(_coords)

    plot(pts.xy[0], pts.xy[1])
    _min = min(flatten(coords)) - 1
    _max = max(flatten(coords)) + 1
    ax = gca()
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    ax.spines['top'].set_position(('data', -1))
    ax.spines['right'].set_position(('data', -1))
    ylim(_min, _max)
    xlim(_min, _max)
    grid()
    title('Shape: %r' % (coords, ))
    show()
    savefig('/tmp/shape.png', dpi=150)
    return pts


if __name__=='__main__':
    setup_mpl()
    pts = ((2, 2), (-1, 1), (-2, -2), (1, -1))
    draw_shape(pts)
