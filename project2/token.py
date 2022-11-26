import sys
from socket  import *
import random
import simpy
import math


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




SIM_TIME = 1000     # Simulation time in minutes
TOTAL_BYTES = 0

class Ring(object):
    """
    Hosts have to request the token. When they get the token, they
    can be served.
    """
    def __init__(self, env):
        self.env = env
        self.token = simpy.Resource(env)

    def serve(self, host):
        global TOTAL_BYTES
        bytes = random.randint(64, 1518)
        TOTAL_BYTES += bytes
        yield self.env.timeout(bytes / 10e8 * 60)
        print("Ring served %s." % (host))


def host(env, name, ring):
    """The host process (each host has a ``name``) arrives at the ring
    (``ring``) and waits for a token.
    """
    print('%s enters the ring at %.2f.' % (name, env.now))
    with ring.token.request() as request:
        yield request

        print('%s is handed a token at %.2f.' % (name, env.now))
        yield env.process(ring.serve(name))


def setup(env, numberOfHosts, lmda):
    """Create a ring, a number of initial hosts."""
    # Create the ring
    ring = Ring(env)

    # Create n hosts
    for i in range(numberOfHosts):
        env.process(host(env, 'Host %d' % i, ring))

    # Create more packets for the hosts
    while True:
        yield env.timeout(nedTime(lmda))
        print("A new process has arrived at %s" % (i))


# Return a random number (negativeExponentiallyDistributedTime)
def nedTime(rate):
    u = random.random()
    return (-1 / rate) * math.log(1 - u)

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, numberOfHosts=10, lmda=0.01))

# Execute!
env.run(until=SIM_TIME)

