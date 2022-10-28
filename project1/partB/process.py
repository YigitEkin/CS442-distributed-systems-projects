import os

class Process:
    def __init__(self, process_chan, process_number, std_chan, choice):
        self.chan = process_chan
        self.prof = self.chan.join('prof')
        self.process_number = process_number
        self.std_chan = std_chan
        self.student = self.std_chan.join('student')
        self.choice = choice

    def run(self):
        # Read the names.txt into a list
        names = []
        with open('names.txt', 'r') as f:
            for line in f:
                names.append(line.strip())

        self.chan.bind(self.prof)
        self.std_chan.bind(self.student)
        prof =self.chan.subgroup('prof')
        student = self.chan.subgroup('student')
    
        self.chan.sendTo(prof, str("Hello " + names[int(str(self.prof).encode('utf-8'))]))
        self.std_chan.sendTo(student, str("Hello there students"))

        print("I am", self.prof, "  I recieved: ",self.chan.recvFrom(prof, 1))
        print("I am", self.student, "  I recieved: ",self.std_chan.recvFrom(student, 1))


