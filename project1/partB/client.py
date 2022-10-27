import sys,os,time
import channel
import process

n = 3
chan = channel.Channel()
std_chan = channel.Channel()
chan.channel.flushall()
std_chan.channel.flushall()

procs  = [process.Process(chan, n, std_chan) for i in range(n)]

for i in range(n):
	pid = os.fork()
	if pid == 0:
		procs[i].run()
		os._exit(0)
	time.sleep(0.25)

os._exit(0)

