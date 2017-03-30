# -*- coding: utf-8 -*-

import argparse
import csv
import os
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/1880-2016_land_ocean.csv", help="Input file")
parser.add_argument('-dur', dest="DURATION", default=120, help="Duration in seconds")

args = parser.parse_args()
DURATION = args.DURATION

def parseNumber(string):
    try:
        num = float(string)
        if "." not in string:
            num = int(string)
        return num
    except ValueError:
        return string

def parseNumbers(arr):
    for i, item in enumerate(arr):
        for key in item:
            arr[i][key] = parseNumber(item[key])
    return arr

def readCSV(filename):
    rows = []
    with open(filename, 'rb') as f:
        lines = [line for line in f if not line.startswith("#")]
        reader = csv.DictReader(lines, skipinitialspace=True)
        rows = list(reader)
        rows = parseNumbers(rows)
    return rows

# Read data
years = readCSV(args.INPUT_FILE)
yearCount = len(years)
print "Read %s years" % yearCount

secondsPerYear = 1.0 * DURATION / yearCount

# G
# Bb
# D
#
# Bb
# D
# F
#
# D
# F
# A
#
# Eb
# G
# Bb
