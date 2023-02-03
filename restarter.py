from datetime import datetime
from time import sleep
from os import system

def updateLog(text:str):
  now = datetime.now()
  date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
  f = open("Log.txt", "a")
  f.write(date_time + " | " + text + "\n")
  f.close()

log = 'System use kill 1'
updateLog(log)
sleep(10)
system('kill 1')
print('kill')