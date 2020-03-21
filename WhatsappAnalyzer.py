import sys
from datetime import datetime
import re
from prettytable import PrettyTable
from collections import Counter
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


def radar_factory(num_vars, frame='circle'):
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def draw(self, renderer):
            if frame == 'polygon':
                gridlines = self.yaxis.get_gridlines()
                for gl in gridlines:
                    gl.get_path()._interpolation_steps = num_vars
            super().draw(renderer)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)

                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def getArray(line):
    try:
        dateRegex = re.compile(
            r"^[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,2}, [0-9]{1,2}:[0-9]{2} (a|p)m")
        date = dateRegex.search(line).group()
        d = datetime.strptime(date, '%d/%m/%y, %I:%M %p')
    except:
        print("The chat is either not in 12h format or doesn't follow D/M/Y format.")
        print("Try changing your phone settings before exporting chat")
        sys.exit()
    m = line[1+line.index(":"):][1+line[1+line.index(":"):].index(":"):].strip()
    return [d, m]


def setup(f):
    di = {}
    pattern = "^[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}, [0-9]{1,2}:[0-9]{2} (a|p)m"
    current = None
    for line in f:
        if ':' not in line or line.index(':') + line[::-1].index(':') + 1 == len(line):
            continue
        elif re.match(pattern, line):
            current = line[1+line.index('-'): line.index(':') +
                           line[line.index(':')+1:].index(':')+1].strip()
            temp = getArray(line)
            if current in di:
                di[current].append(temp)
            else:
                di[current] = [temp]
        else:
            print(line)
            di[current][-1][1] += " " + line
    return di


def wordAnalysis(arr):
    messages = [x[1] for x in arr]
    wordsCount = 0
    allWords = []
    for message in messages:
        if "<Media omitted>" in message:
            continue
        wordsCount += len(message.split())
        for word in message.split():
            allWords.append(word.lower())
    freq = Counter(allWords).most_common(10)
    return [wordsCount, freq]


def makeTable():
    t = PrettyTable([' ']+[i for i in di.keys()])
    t.add_row(["Messages Sent"] + [len(di[i]) for i in di.keys()])
    t.add_row(["Media Sent"] + [len([x for x in di[i]
                                     if "<Media omitted>" in x]) for i in di.keys()])
    wordFreq = [wordAnalysis(di[i]) for i in di.keys()]
    t.add_row(["Words Sent"] + [i[0] for i in wordFreq])
    t.add_row(["Words per Message"] + ["{:.2f}".format(words[0]/len(di[name]))
                                       for (words, name) in zip(wordFreq, di.keys())])
    t.add_row(["Most Freq Words"] + ["-------" for x in di.keys()])

    for i in range(10):
        t.add_row([" "] + [str(x[1][i][0]) + " - " +
                           str("{:.2f}".format(100*x[1][i][1]/x[0])) + "%" for x in wordFreq])
    print(t)


def radarChart(title, arr, labels):
    theta = radar_factory(len(labels), frame='polygon')

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(
        15, 10), subplot_kw=dict(projection='radar'))
    ax1, ax2 = ax[0], ax[1]
    fig.subplots_adjust(top=0.85, bottom=0.05)
    num = max([max(i) for i in arr])//7
    ax1.set_rgrids([i*num for i in range(7)], angle=180, alpha=0.5)
    ax1.set_title(str(title)+": Individual",  position=(0.5, 1.1),
                  ha='center', size="xx-large", family="serif", weight="bold")
    for x in arr:
        line = ax1.plot(theta, x)
        ax1.fill(theta, x, alpha=0.2)
    ax1.set_varlabels(labels)
    ax1.legend(tuple(i for i in di.keys()), loc="best", fontsize="large", frameon=False, borderpad=-3,
               prop=dict(family="cursive", style="italic", weight="normal"))

    total = []
    for i in range(len(arr[0])):
        temp = 0
        for j in range(len(arr)):
            temp += arr[j][i]
        total.append(temp)

    num = max(total)//7
    ax2.set_rgrids([i*num for i in range(7)], angle=180, alpha=0.5)
    ax2.set_title(str(title)+": Cumulative",  position=(0.5, 1.1),
                  ha='center', size="xx-large", family="serif", weight="bold")
    line = ax2.plot(theta, total, label="Total Messages")
    ax2.fill(theta, total, alpha=0.2)
    ax2.set_varlabels(labels)
    ax2.legend(loc="best", fontsize="large", frameon=False, borderpad=-3,
               prop=dict(family="cursive", style="italic", weight="normal"))

    plt.show()


def weekChart():
    arr = [[[x[0].weekday() for x in di[i]].count(x) for x in range(7)]
           for i in di.keys()]
    labels = ["Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday", "Sunday"]
    radarChart("Weekly Analysis", arr, labels)


def hourChart():
    arr = [[[x[0].hour for x in di[i]].count(
        x) for x in range(24)] for i in di.keys()]
    labels = [i for i in range(24)]
    radarChart("Hourly Analysis", arr, labels)


try:
    file = sys.argv[1]
except:
    print("Error!!! You didn't enter the name of file!!!")
    print("Try again!")
    sys.exit()

try:
    with open(file, "r") as f:
        di = setup(f)
except:
    print("File doesn't exist. Make sure to put the file in same folder and also use extension")
    sys.exit()

makeTable()
hourChart()
weekChart()
