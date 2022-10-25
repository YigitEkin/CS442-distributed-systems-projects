import channel, stablelog 
from const2PC import *    
import pickle

class Professor:
  def __init__(self): #-
    self.chan        = channel.Channel() #-
    self.professor = self.chan.join('student') #-
    self.log         = stablelog.createLog(self.professor) #-

  def run(self):
    students = self.chan.subgroup('student') #-
    self.chan.bind(self.professor)
    self.chan.join('professor')
    self.log.info('INIT PROF')             #-
    yetToReceive = list(students)
    self.log.info('Prof waiting for students')
    self.log.info(yetToReceive)
    
    self.chan.sendTo([str(self.professor)], bytes(INFO, 'utf-8'))
    self.log.info('Sent info to student')
    """"
    while len(yetToReceive) > 0:
      msg = self.chan.recvFrom(students, TIMEOUT)
      if (not msg):
        self.log.info('Recieved nothing from students')
        self.chan.sendTo(students, WARN)
        return
      else:
        yetToReceive.remove(msg[0])
    self.log.info('All students have sent their info')
    self.chan.sendTo(students, CONCLUSION)
  
    yetToReceive = list(students)
    self.log.info('WAIT PROF')
    self.chan.sendTo(students, INFO )
    self.log.info('SENT PROF')
    for i in range(30):
      msg = self.chan.recvFrom(students, TIMEOUT)
      if (msg == GROUP_OBJECTION):
        self.log.info('OBJECTION is sent, denied')
        self.chan.sendTo(students, DENY)
        return
      elif (not msg) or (msg[1] != GROUP_INFO):
        self.log.info('WARNING is sent!')
        self.chan.sendTo(students, WARN)
        
    self.chan.sendTo(students, CONCLUSION)

    """