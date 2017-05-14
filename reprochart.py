#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv, itertools
import matplotlib.pyplot as plt
import matplotlib as mplt
import numpy as np
import argparse
import os
import io

# Convert to number
def to_number(x):
    try:
        return int(x)
    except:
        return float(x)
# Convert string to float or NaN if it can't
def to_float(x):
    try:
        return float(x)
    except:
        return np.nan
# Filter NaN points from the graph
def filter_nans(x,y):
    pairs = filter(lambda p: not np.isnan(p[1]), zip(x,y))
    if len(pairs) > 0:
        return zip(*pairs)
    else:
        return ([], [])
def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def process_chart(infile, outfile):
    # Option keys:
    FIGHEIGHT = 'figheight'
    FIGWIDTH = 'figwidth'
    TITLE = 'title'
    XTITLE = 'xtitle'
    YTITLE = 'ytitle'
    FONTSIZE = 'fontsize'
    XFONTSIZE = 'xfontsize'
    YFONTSIZE = 'yfontsize'
    XTITLESIZE = 'xtitlesize'
    YTITLESIZE = 'ytitlesize'
    LEGENDSIZE = 'legendsize'
    XMARGIN = 'xmargin'
    YMARGIN = 'ymargin'
    XLOGSCALE = 'xlogscale'
    YLOGSCALE = 'ylogscale'
    YLIMMIN = 'ylimmin'
    YLIMMAX = 'ylimmax'
    YNUMTICKS = 'ynumticks'
    # Read the rows of the CSV file
    rows = None
    options = dict()
    with io.open(infile, 'r', encoding='utf-8') as csvfile:
        line = csvfile.readline()
        while len(line) == 0 or line[0] != '=':
            line = line.strip()
            if len(line) == 0:
                line = csvfile.readline()
            elif ':' not in line:
                raise ValueError('Above the line (===), only empty lines or key:value options are allowed!')
            key, value = line.strip().split(':')
            value = value.strip()
            if len(value) >= 2 and value[0] in ['"', '"'] and value[0] == value[-1]:
                value = value[1:-1]
            elif value.lower() in ['true', 'false']:
                value = (value == 'true')
            else:
                value = to_number(value)
            options[key.lower()] = value
            line = csvfile.readline()
        reader = unicode_csv_reader(csvfile)
        rows = [r for r in reader]
    # Set defaults if not found:
    if FIGHEIGHT not in options:
        options[FIGHEIGHT] = 5
    if FIGWIDTH not in options:
        options[FIGWIDTH] = 5
    if FONTSIZE not in options:
        options[FONTSIZE] = 11
    if YFONTSIZE not in options:
        options[YFONTSIZE] = options[FONTSIZE]
    if XFONTSIZE not in options:
        options[XFONTSIZE] = options[FONTSIZE]
    if YTITLESIZE not in options:
        options[YTITLESIZE] = options[FONTSIZE]
    if XTITLESIZE not in options:
        options[XTITLESIZE] = options[FONTSIZE]
    if LEGENDSIZE not in options:
        options[LEGENDSIZE] = options[FONTSIZE]
    if YMARGIN not in options:
        options[YMARGIN] = 2
    if XMARGIN not in options:
        options[XMARGIN] = 0.3
    if YLOGSCALE not in options:
        options[YLOGSCALE] = False
    if XLOGSCALE not in options:
        options[XLOGSCALE] = False
    if YLIMMIN not in options:
        options[YLIMMIN] = 10
    if YLIMMAX not in options:
        options[YLIMMAX] = 100
    if YNUMTICKS not in options:
        options[YNUMTICKS] = 10
    # Convert the rows to headers, x values and the different y values
    headers = rows[0]
    data = rows[1:]
    cols = zip(*data)
    #x = map(to_float, cols[0])
    x = cols[0]
    ys = [map(to_float, y) for y in cols[1:]]
    # print LaTeX table
    print(u'\\begin{tabular}{%s}' % ('c' * len(x)))
    print(u'\\toprule')
    print(u'%s & %s \\\\' % (headers[0], u' & '.join(map(str,x))))
    print(u'\\midrule')
    best = [np.amax([y[i] if not np.isnan(y[i]) else -np.inf for y in ys]) for i in xrange(len(x))]
    for i in range(len(ys)):
        fx, fy = filter_nans(range(len(x)), ys[i])
        a = [' '] * len(x)
        for j, y in zip(fx, fy):
            formatstr = '\\textbf{%s}' if best[j] == y else '%s'
            a[j] = formatstr % str(y)
        name = unicode(headers[i+1]).replace(u'\u2020', '\\dag')
        print(u'%s & %s \\\\' % (name, u' & '.join(a)))
    print(u'\\bottomrule')
    print(u'\\end{tabular}')
    # Set font size of axes
    mplt.rc('ytick', labelsize=options[YFONTSIZE])
    mplt.rc('xtick', labelsize=options[XFONTSIZE]) 
    # Set the figure size
    plt.figure(figsize=(options[FIGWIDTH], options[FIGHEIGHT]))
    # Set the titles
    if TITLE in options:
        plt.title(options[TITLE])
    if XTITLE in options:
        plt.xlabel(options[XTITLE], fontsize=options[XTITLESIZE])
    if YTITLE in options:
        plt.ylabel(options[YTITLE], fontsize=options[YTITLESIZE])
    # Plot the series using unique colors and markers
    cm = plt.get_cmap('nipy_spectral')
    markers = ['v', 'o', '*', 's', 'x', '^','+']
    linestyles = ['-', '-.', '--']
    styles = itertools.cycle(itertools.product(linestyles, markers))
    chosen_styles = list(reversed([styles.next() for i in xrange(len(ys))]))
    for i in range(len(ys)):
        fx, fy = filter_nans(range(len(x)), ys[i])
        linestyle, marker = chosen_styles[i]
        plt.plot(fx, fy,
                 color=cm(float(i) / len(ys)),
                 linestyle=linestyle, marker=marker,
                 label=headers[i+1])
    # Setup y axis
    plt.yticks(np.linspace(options[YLIMMIN], options[YLIMMAX], num=options[YNUMTICKS], endpoint=True), )
    plt.ylim(options[YLIMMIN] - options[YMARGIN], options[YLIMMAX] + options[YMARGIN])
    if options[YLOGSCALE]:
        plt.yscale('log', basex=2)
    # Setup x axis
    plt.xticks(range(len(x)), x)
    plt.xlim(-options[XMARGIN], len(x) - 1 + options[XMARGIN])
    if options[XLOGSCALE]:
        plt.xscale('log', basex=2)
    # Set the figure to use a grid
    plt.grid()
    # Set the figure to use a legend and place it in the lower right corner
    plt.legend(loc='lower left', prop={'size':options[LEGENDSIZE]})
    # Save the plot to res.pdf using tight bounds around the figure
    plt.savefig(outfile, bbox_inches='tight')
    
def main():
    parser = argparse.ArgumentParser(description='Process csv files with special headers into pdf charts and latex tables.')
    # Required arguments: input and output files.
    parser.add_argument(
        "infile",
        help="Input file."
    )
    parser.add_argument(
        "--outfile",
        help="Output file",
        default="",
    )
    args = parser.parse_args()
    args.infile = os.path.normpath(args.infile)
    if not os.path.isfile(args.infile):
        raise ValueError("Cannot find input file!")
    if os.path.abspath(args.infile) == os.path.abspath(args.outfile):
        raise ValueError("The infile and outfile cannot be the same!")
    if args.outfile == "":
        filename = os.path.splitext(args.infile)[0]
        args.outfile = filename + '.pdf'
    if len(args.outfile.strip()) == 0:
        raise ValueError("Cannot use an empty string!")
    process_chart(args.infile, args.outfile)

if __name__ == '__main__':
    main()