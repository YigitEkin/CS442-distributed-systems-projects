from multiprocessing.connection import wait
import channel, stablelog 
from const2PC import *    
import pickle

class Professor:
  def __init__(self): #-
    self.chan        = channel.Channel() #-
    self.professor = self.chan.join('professor') #-
    self.log         = stablelog.createLog(self.professor) #-

  def run(self):
    students = self.chan.subgroup('student') #-
    self.chan.bind(self.professor)
    self.chan.join('student')
    self.log.info('INIT PROF')             #-
    yetToReceive = list(students)
    print(students, "sahe")
    self.log.info('Prof waiting for students')
    self.log.info(yetToReceive)
    for i in yetToReceive:
      yetToReceive[i] = str(yetToReceive[i])
    self.chan.sendTo(yetToReceive, bytes(INFO, 'utf-8'))
    self.log.info('Sent info to student')
