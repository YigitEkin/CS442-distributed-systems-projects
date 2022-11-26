import sys


def main():
    # Get the input file name
    numOfProcess = sys.argv[1]
    if (numOfProcess < 2 or numOfProcess > 20):
        print("Number of processes must be between 2 and 20")
        return
    # Get the input file name
    inputFileName = sys.argv[2]
    # Get increment delta
    delta = sys.argv[3]
    if delta < 0:
        print("Delta must be greater than 0")
        return
    # Get exit count
    exitCount = sys.argv[4]
    # Get log file name
    logFileName = sys.argv[5]
    # Get max time
    maxTime = sys.argv[6]