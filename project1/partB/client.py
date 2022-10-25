from subprocess import Popen, PIPE
import professor

import os
import channel
import student

chan = channel.Channel()
chan.channel.flushall()

NP = 1
prof = professor.Professor()
stds = [student.Student() for i in range(NP)]

pid = os.fork()
if pid == 0:
    prof.run()
    os._exit(0)

for i in range(NP):
    pid = os.fork()
    if pid == 0:
        stds[i].run()
        os._exit(0)


