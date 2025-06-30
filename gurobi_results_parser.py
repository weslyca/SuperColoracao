import os
import pandas as pd


filenames = os.listdir("GurobiResults/")


def parse_results(filename):

    print(filename)

    with open("GurobiResults/" + filename, 'r') as f:
        lines = f.readlines()

    reading_time = []
    relax_time = []
    exploring_time = []
    for line in lines:
        if "seconds" in line:
            # print(line[:-1])
            if "Reading" in line:
                time = float(line.split()[-2])
                reading_time.append(time)
            elif "relaxation" in line:
                time = float(line.split()[-5])
                relax_time.append(time)
            elif "Explored" in line:
                time = float(line.split()[-5])
                exploring_time.append(time)

    reading_time = reading_time[:20]
    relax_time = relax_time[:20]
    exploring_time = exploring_time[:20]

    reading_series = pd.Series(reading_time)
    if len(relax_time) > 0:
        solving_series = pd.Series([relax_time[i] + exploring_time[i] for i in range(20)])
    else:
        solving_series = pd.Series([exploring_time[i] for i in range(20)])
    # print("Reading time: %.2f (%.2f)" % (reading_series.mean(), reading_series.std()))
    # print("Solving time: %.2f (%.2f)"  % (solving_series.mean(), solving_series.std()))
    # print("Time:  %.2f (%.2f) &  %.2f (%.2f)" %  (reading_series.mean(), reading_series.std(), solving_series.mean(), solving_series.std()))
    print("Reading time: %.2f" % (reading_series.mean(),))
    print("Solving time: %.2f"  % (solving_series.mean()))
    print("Time:  %.2f &  %.2f" %  (reading_series.mean(), solving_series.mean()))    
    print()

for filename in filenames:
    parse_results(filename)