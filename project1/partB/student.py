import channel, stablelog, random #-
from const2PC import * #-

class Student:
  def __init__(self): #-
    print("I AM EXISTING AS OF NOW")
    self.chan        = channel.Channel() #-
    self.student = self.chan.join('professor') #-
    self.log         = stablelog.createLog(self.student) #-
#-
  def which_mail_to_send(self): 
    return random.choice([GROUP_INFO,GROUP_INFO,GROUP_INFO,GROUP_INFO,GROUP_INFO,GROUP_INFO,GROUP_INFO,GROUP_OBJECTION,DRUNK_MSG])
#-
  def run(self):
    self.chan.bind(self.student) #-

    professor = self.chan.subgroup('student') #-

    print(professor, "professor in student")
    self.log.info('INIT STUDENT') 
    msg = 0
    msg = self.chan.recvFrom([0,1,2,3], TIMEOUT)
    self.log.info('Recieved message from professor')
    if (not msg):
      self.log.info('No professor')
    else :
      self.log.info('Professor is here')
      self.chan.sendTo(professor, self.which_mail_to_send())

    msg = self.chan.recvFrom(professor, TIMEOUT)
    while(not msg): 
      msg = self.chan.recvFrom(professor, TIMEOUT)
    self.log.info(msg)
  