import sys
from pylab import *


def setup_mpl():
    rcParams['text.usetex']=True


def parse_pat(pfile):
    """
        Returns a pattern file as a list of lists using floats and ints as
        suited from a given JavaNNS pattern file _pfile_. Comments and header
        information is skipped over
    """

    def convert_row(row):
        _row = []
        for elem in row:
            try:
                _row.append(int(elem))
            except ValueError:
                try:
                    _row.append(float(elem))
                except ValueError:
                    _row.append(elem)
        return _row

    # Initialize our data. We'll need to parse out how many input/outputs
    # there are
    data, inputs, outputs = [], 0, 0

    with open(pfile) as pattern_file:
        data = pattern_file.read().split('\n')

    # Strip out comments and empty rows
    data = [row.strip() for row in data if len(row) > 0 and '#' not in row]

    # Need to find out where the data starts, all pattern files will specify
    # some number of input/outputs prefixed with "No. of" so we can look for
    # that; the data will be the next row
    drow = 0
    for idx, row in enumerate(data):

        try:
            if 'No. of' in row:
                drow = idx + 1

                if 'input' in row:
                    inputs = int(row[-1])

                if 'output' in row:
                    outputs = int(row[-1])

                continue
        except IndexError:
            pass

    points = []
    for idx in range(drow, len(data)):
        points.append(convert_row(data[idx].split()))

    # convert to numpy array - will make slices much easier
    points = array(points)

    # Now return the data sliced into input & output arrays

    if outputs:
        data = points[:, :inputs], points[:, inputs:]
    else:
        data = (points, None)

    return data


def scatterplot_pattern(pfile):
    inputs, outputs = parse_pat(pfile)

    num_outputs = outputs.shape[1]
    num_inputs = inputs.shape[1]

    assert num_inputs == 2

    scatter(inputs[:, 0], inputs[:, 1], c='r')
    grid()
    show()


if __name__ == '__main__':
    setup_mpl()
    scatterplot_pattern(sys.argv[1])
