#!/usr/bin/env python2

import cairoplot
import serial
import time

#geigerPort = "/dev/ttyUSB0"
geigerPort = "bar"
plotLength = 30
chartPath  = "geiger.png"

# attempt to read from the counter for 1 minute, accumulating events
def countsPerMinute(geiger):
    start = time.time()
    count = 0
    while time.time() < start + 60:
        if geiger.read(1) != "":
            print("Count")
            count = count + 1
    return count

# our read attempts will time out after 1 second
geiger = serial.Serial(port = geigerPort, baudrate = 9600, timeout = 1)

# plot the past plotLength minutes, initially all zero
times  = [""] * 30
counts = [0] * 30

# once a minute, add a new count, drop the oldest, and replot
while 1 == 1:
    # drop the oldest data point
    counts = counts[1:len(counts)]
    times  =  times[1:len(times)]
    # append the newest data point
    counts.append(countsPerMinute(geiger))
    times.append(time.strftime("%I:%M %p"))
    # plot the resulting graph
    cairoplot.dot_line_plot(chartPath, counts, 400, 300,
                            background = "white white",
                            border = 1,
                            axis = True,
                            x_labels = times,
                            x_title  = "CPM as of %s" % time.asctime())
