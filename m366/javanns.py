import sys
from pylab import *
from sympy import Symbol, solve


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
    data = [row.strip() for row in data if len(row) > 1 and '#' not in row]

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


def scatterplot_pattern(pfile, color='r'):
    inputs, outputs = parse_pat(pfile)

    num_outputs = outputs.shape[1]
    num_inputs = inputs.shape[1]

    assert num_inputs == 2

    # hacky - this is just for TMA work - the scatterplot itself is ok
    # but we want to group this into 3 x 5 elements (for the A patterns at least)
    shapes = ('o', '^', 's')
    colors = ('r', 'g', 'b')
    labels = ('Class 1', 'Class 2', 'Class 3')

    for idx, x in enumerate((0, 5, 10)):
        scatter(inputs[:, 0][x:x + 5], inputs[:, 1][x:x + 5], marker=shapes[idx], c=colors[idx], s=100, label=labels[idx])


def plot_partition(w1, w2, bias, color='red', label=None):
    """
        Given weights and bias solve the equation f(x)=0 for
        x2. We can then plot this. Plotting several of these
        functions should partition the scatterplot of the input
        space if the network has been trained suitably.
    """

    # Use sympy to solve this symbolically - i sort of prefer doing this stuff
    # in symbols rather than matrices in numpy/matlab etc
    x1, x2 = Symbol('x1'), Symbol('x2')
    solution = solve(w1 * x1 + w2 * x2 + bias, x2)[0]
    m, c = solution.coeff(x1, 1), solution.coeff(x1, 0)

    t = linspace(0, 1)
    plot(t, m*t + c, color=color, label=label)


def validation_table_assess():
    with open('/home/jaymz/development/mathematics/openuni-notes/courses/m366/tmas/tma03/q2a-validation.res') as f:
        table = f.read()

    def convert(x):
        try:
            return int(x)
        except ValueError:
            return float(x)
        except:
            raise Exception('Need either int or float to convert')

    def is_ambiguous(outputs, chosen, correct, is_correct):
        if is_correct:
            return min([abs(chosen - x) for x in outputs if x != chosen]) < 0.3
        else:
            return abs(correct - chosen) < 0.5

    SEGMENT_LENGTH = 4
    HEADER_LENGTH = 10
    data = table.split('\n')[HEADER_LENGTH:]
    data = [data[j: j + SEGMENT_LENGTH] for j in range(0, len(data), SEGMENT_LENGTH)]
    data = [[i[2].split(' '), i[3].split(' ')] for i in data if len(i) > 1]

    for idx, row in enumerate(data):
        data[idx][0] = [convert(x) for x in row[0]]
        data[idx][1] = [convert(x) for x in row[1]]

        training = data[idx][0]
        output = data[idx][1]

        max_training = training.index(max(training))
        max_output = output.index(max(output))

        is_correct =  max_training == max_output

        if is_ambiguous(output, output[max_output], output[max_training], is_correct):
            data[idx].append(0)
        elif is_correct:
            data[idx].append(1)
        else:
            data[idx].append(-1)

    return data

def partition_plot_example():

    # Plot a pattern - this is a bit hacky at the minute as it's
    # explicitly segmenting the data in a non-generic way. Each
    # pattern in the sample file has 5 outputs for each class
    scatterplot_pattern('/home/jaymz/development/mathematics/openuni-notes/courses/m366/notes/TMA03_A.pat')

    # These figures are from a simulation network file from JavaNNS. You can
    # read off the data, for example:
    #
    # unit definition section :
    #
    # no. | typeName | unitName | act      | bias     | st | position | act func | out func | sites
    # ----|----------|----------|----------|----------|----|----------|----------|----------|-------
    #   1 |          | Input    |  0.90000 | -0.72631 | i  | 3,6,1    |||
    #   2 |          | Input    |  0.10000 |  0.39628 | i  | 7,6,1    |||
    #   3 |          | Output   |  0.00000 |  3.38851 | o  | 1,1,1    |||
    #   4 |          | Output   |  0.13079 | 17.56716 | o  | 5,2,1    |||
    #   5 |          | Output   |  0.99868 | -13.04124 | o  | 9,1,1    |||
    # ----|----------|----------|----------|----------|----|----------|----------|----------|-------
    #
    #
    # connection definition section :
    #
    # target | site | source:weight
    # -------|------|------------------------------------------------------------------------------------------------------------
    #      3 |      | 2:12.66246, 1:-29.89602
    #      4 |      | 2:-27.89854, 1:-18.52970
    #      5 |      | 2: 8.80255, 1:20.88110
    # -------|------|------------------------------------------------------------------------------------------------------------
    #

    w1, w2, wb = -29.89062, 12.66246, 3.38851
    u1, u2, ub = -18.52970, -27.89854, 17.56716
    v1, v2, vb = 20.88110, 8.80255, -13.04124

    # Plot each partition for the given weights and biases
    plot_partition(w1, w2, wb, color='darkred', label='Output 1')
    plot_partition(u1, u2, ub, color='darkblue', label='Output 2')
    plot_partition(v1, v2, vb, color='darkgreen', label='Output 3')

    grid()
    legend()

    # Limit the axis for prettyness
    ylim(0, 1)
    xlim(0, 1)

    show()


if __name__ == '__main__':
    setup_mpl()
    data = validation_table_assess()
