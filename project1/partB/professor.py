import channel, stablelog 
from const2PC import *    

class Professor:
  def __init__(self): #-
    self.chan        = channel.Channel() #-
    self.coordinator = self.chan.join('professor') #-
    self.log         = stablelog.createLog(self.professor) #-

  def run(self):
    self.chan.bind(self.professor)  
    self.log.info('INIT')             #-
    students = self.chan.subgroup('student') #-
    yetToReceive = list(students)
    self.log.info('WAIT')
    self.chan.sendTo(students, INFO )
    while len(yetToReceive) > 0:
      msg = self.chan.recvFrom(students, TIMEOUT)
      if (msg == GROUP_OBJECTION):
        self.log.info('OBJECTION is sent, denied')
        self.chan.sendTo(students, DENY)
        return
      elif (not msg) or (msg[1] != GROUP_INFO):
        self.log.info('WARNING is sent!')
        self.chan.sendTo(students, WARN)
        
    self.chan.sendTo(students, CONCLUSION)