import os

class Process:
    def __init__(self, process_chan, process_number, std_chan):
        self.chan = process_chan
        self.pid = self.chan.join('test')
        self.process_number = process_number
        self.std_chan = std_chan
        self.student = self.std_chan.join('student')

    def run(self):
        self.chan.bind(self.pid)
        self.std_chan.bind(self.student)
        otherProcess =self.chan.subgroup('test')
        student = self.chan.subgroup('student')
        self.chan.sendTo(otherProcess, str("Hello from process " + str(self.pid)))
        self.std_chan.sendTo(student, str("Hello for student " + str(self.pid)))

        print("I am", self.pid, "  I recieved: ",self.chan.recvFrom(otherProcess, 1))
        print("I am", self.pid, "  I recieved: ",self.std_chan.recvFrom(student, 1))


