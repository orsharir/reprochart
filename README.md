# Reprochart

This is a simple python script (tested on python 2.7) for easily reproducible charts. The general concept is to augment csv files with a simple header that keeps the configuration of the chart. The script also helps by automatically picking sensible defaults for most options, including colors and line types. The idea came while working on an article, where I was constently updating my data, and had to recreate my charts over and over again.

## Example

Let's assume the csv file is:
```
xtitle: "Probability of Missing Pixels"
ytitle: "Test Accuracy (%)"
fontsize: 11
legendsize: 7.5
xfontsize: 9
figheight: 2.3
figwidth: 5.3
================================
"P","KNN","Zero †","Mean †","GSN †","NICE †","DPM †","NADE †","MP-DBM *","CP-CAC","HT-CAC"
0.00,96.8,99.2,99.2,99.2,99.2,99.2,99.2,99,96.6,99.0
0.25,96.7,97.3,98.4,97.4,98.9,99.0,98.7,98,96.4,99.0
0.50,96.2,88.2,90.9,88.5,97.9,98.2,98.1,97,95.7,98.7
0.75,94.4,58.6,52.4,51.8,82.6,89.4,95.1,92,92.2,97.7
0.90,86.4,28.7,21.1,17.7,36.3,47.7,77.6,35,79.8,90.5
0.95,71.7,19.5,15.6,12.6,20.2,25.7,50.1,18,66.5,76.0
0.99,29.2,12.6,10.9,10.1,11.7,12.7,13.5,13,31.2,33.0
```

Then the resulting output is: [Example chart](examples/example1.png)

## Usage

```
./reprochart.py example.csv
```

The script takes as input the filename of a csv file. The csv is divided to two parts, seperated by the first line starting with the equal sign character, "=". The first part is the header, that contains either empty lines, or lines containing ``<key>:<value>`` pairs. The second part is a standard csv file, and the script assumes that the first row is the labels of each series, the first column represent the values on the x-axis, and the other colmuns each represent a different serie, by specifying the y-values matching the x-axis.

By default he script saves a pdf image of the resulted chart to ``<csv-filename>.pdf``, as well as print to stdout the LaTeX table representation. The default filename could be changed with the optional ``--outfile`` flag.

## Supported Key-Value Pairs for Configuration

The following keys are currently supported (all keys are optional):
    * title -- Large title for the chart.
    * xtitle -- Title for the x-axis.
    * ytitle -- Title for the y-axis.
    * figheight -- The height of the figure in points.
    * figwidth -- The width of the figure in points.
    * fontsize -- The global fontsize.
    * xfontsize -- Overrides global fontsize for the x values.
    * yfontsize -- Overrides global fontsize for the y values.
    * xtitlesize -- Overrides global fontsize for the x-axis title.
    * ytitlesize -- Overrides global fontsize for the y-axis title.
    * legendsize -- The size of the legend.
    * xmargin -- The margin from the x-axis.
    * ymargin -- The margin from the y-axis.
    * xlogscale -- If ``<value> = true`` then uses log-scale for x-axis.
    * ylogscale -- if ``<value> = true`` then uses log-scale for y-axis.
    * ylimmin -- The minimal value for the y-axis.
    * ylimmax -- The maximal value for the y-axis.
    * ynumticks -- The number of ticks in the y-axis.