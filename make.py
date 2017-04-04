# -*- coding: utf-8 -*-

import argparse
import csv
import math
import os
import sys
import time

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/1880-2016_land_ocean.csv", help="Input file")
parser.add_argument('-instr', dest="INSTRUMENTS_FILE", default="data/instruments.csv", help="Input file")
parser.add_argument('-bpm', dest="BPM", type=int, default=120, help="BPM")
parser.add_argument('-bpy', dest="BEATS_PER_YEAR", type=int, default=4, help="Beats per year")
parser.add_argument('-bpp', dest="BEATS_PER_PHASE", type=int, default=24, help="Beats per phase")
parser.add_argument('-outinstr', dest="OUTPUT_INSTRUMENTS_FILE", default="data/ck_instruments.csv", help="Input file")
parser.add_argument('-outseq', dest="OUTPUT_SEQUENCE_FILE", default="data/ck_sequence.csv", help="Input file")

args = parser.parse_args()
BPM = args.BPM
BEATS_PER_YEAR = args.BEATS_PER_YEAR
BEATS_PER_PHASE = args.BEATS_PER_PHASE
INSTRUMENTS_DIR = "instruments/"

# Config chord progression
PROGRESSION = [
    ["G", "Bb", "D"],
    ["Bb", "D", "F"],
    ["D", "F", "A"],
    ["Eb", "G", "Bb"]
]
# Config tempo/gains
OCTAVE_RANGE = (1, 5)
TEMPO_RANGE = (1.0, 2.0)
GAIN_RANGE = (0.1, 1.0)

# Calculations
BEAT_MS = round(60.0 / BPM * 1000)

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
beats = BEATS_PER_YEAR * yearCount + (BEATS_PER_PHASE - BEATS_PER_YEAR)
print "%s beats" % beats
durationMs = beats * BEAT_MS
duration = durationMs / 1000
yearMs = BEATS_PER_YEAR * BEAT_MS
print "Duration: %s (%ss)" % (time.strftime("%M:%S", time.gmtime(duration)), duration)

# Add normalized values
minValue = min([y["Value"] for y in years])
maxValue = max([y["Value"] for y in years])
for i,year in enumerate(years):
    years[i]["Norm"] = (1.0 * year["Value"] - minValue) / (maxValue - minValue)

# Read instruments
instruments = readCSV(args.INSTRUMENTS_FILE)
for i,instr in enumerate(instruments):
    instruments[i]["file"] = INSTRUMENTS_DIR + instr["instrument"] + "/" + instr["file"]

def lerp(r, amount):
    return (r[1] - r[0]) * amount + r[0]

def phase(r, amount):
    multiplier = math.sin(amount * math.pi)
    return lerp(r, amount)

# Build sequence
sequence = []

for i,year in enumerate(years):
    ms = i * yearMs
    value = year["Norm"]

    for beat in range(BEATS_PER_PHASE):
        gain = phase(GAIN_RANGE, 1.0 * beat / BEATS_PER_PHASE)
