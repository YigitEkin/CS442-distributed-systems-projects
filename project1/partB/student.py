import channel, stablelog, random #-
from const2PC import * #-

class Student:
  def __init__(self): #-
    print("I AM EXISTING AS OF NOW")
    self.chan        = channel.Channel() #-
    self.student = self.chan.join('student') #-
    self.log         = stablelog.createLog(self.student) #-
#-
  def which_mail_to_send(self): 
    return random.choice([GROUP_INFO,GROUP_INFO,GROUP_INFO,GROUP_INFO,GROUP_INFO,GROUP_INFO,GROUP_INFO,GROUP_OBJECTION,DRUNK_MSG])
#-
  def run(self):
    self.chan.bind(self.student) #-
    professor     = self.chan.subgroup('professor') #-
    self.log.info('INIT STUDENT') 

    msg = self.chan.recvFrom(professor, TIMEOUT)
    self.log.info('Recieved message from professor')
    if (not msg):
      self.log.info('No professor')
    else :
      self.log.info('Professor is here')
      self.chan.sendTo(professor, self.which_mail_to_send())

    msg = self.chan.recvFrom(professor, TIMEOUT)
    if (not msg):
      while True:
        msg = self.chan.recvFromAny()
        if (msg[1] == CONCLUSION):
          self.log.info('CONCLUSION is sent')
          break
        else:
          self.log.info('I am drunk')

        


"""
#
    msg = self.chan.recvFrom(professor, TIMEOUT)

    if (not msg):  # Professor has NOT sent message yet
      self.log.info('Waiting...')
      msg = self.chan.recvFrom(professor, TIMEOUT)

    else: # Coordinator will have sent VOTE_REQUEST
      decision = self.which_mail_to_send() 
      if decision == GROUP_INFO:
        self.chan.sendTo(professor, GROUP_INFO)
        self.log.info('Group info is sent!!!')
#-
      elif decision == GROUP_OBJECTION:
        self.chan.sendTo(professor, GROUP_OBJECTION)
        self.log.info('Student objected the group requirements!!!')

      else:
        self.chan.sendTo(professor, DRUNK_MSG)
        self.log.info('HOCAM I LOVE YOU BEEEEEEE!!!! (Drunk mumblings)')

        msg = self.chan.recvFrom(professor, TIMEOUT)
        if (not msg): # Crashed coordinator - check the others
          self.log.info('Waiting...')
          msg = self.chan.recvFrom(professor, TIMEOUT)
        if msg[1] in [DRUNK_MSG, GROUP_OBJECTION]:
          self.chan.sendTo(professor, GROUP_INFO)
"""

