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
    self.chan.bind(self.participant) #-
    professor     = self.chan.subgroup('professor') #-
    allStudents = self.chan.subgroup('student') #-
    self.log.info('INIT') 
#-
    msg = self.chan.recvFrom(professor, TIMEOUT)

    while (not msg):  # Professor has NOT sent message yet
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
#-
      else:
        self.chan.sendTo(professor, DRUNK_MSG)
        self.log.info('HOCAM I LOVE YOU BEEEEEEE!!!! (Drunk mumblings)')

        msg = self.chan.recvFrom(professor, TIMEOUT)
        while (not msg): # Crashed coordinator - check the others
          self.log.info('Waiting...')
          msg = self.chan.recvFrom(professor, TIMEOUT)
        if msg[1] in [DRUNK_MSG, GROUP_OBJECTION]:
          self.chan.sendTo(professor, GROUP_INFO)

