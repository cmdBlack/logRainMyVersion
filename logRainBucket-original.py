import datetime
import RPi.GPIO as GPIO
import time
from time import sleep
import random
import MySQLdb
import os

SW_VER = "1.00"

GPIO_PIN_DATA = 3

if __name__ == '__main__':
  print "logRainBucket", "Version", SW_VER
  
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(GPIO_PIN_DATA, GPIO.IN, pull_up_down = GPIO.PUD_UP)
  #GPIO.setup(GPIO_PIN_DATA, GPIO.IN)

  while True:
    print "waiting for sensor ..."
    GPIO.wait_for_edge(GPIO_PIN_DATA, GPIO.FALLING)
    
    now = datetime.datetime.now()
    print now.strftime("%Y-%m-%d %H:%M:%S"), "rain sensor triggered"
    
    try:
      print "connecting to db"
      db = MySQLdb.connect("localhost", "root", "kpapcp", "pagasa")
      print "success"
      
      curs = db.cursor()
      
      print "saving to datalogs"
      curs.execute("INSERT INTO datalogs(logtime, logtype, value, unit, description) values(NOW(), 'rr', 0.5, 'mm', 'rain rate measurement')")
      db.commit()
      print "success"
    except Exception as error:
      print "failed", error
      db.rollback()
    finally:
      curs.close()
      db.close()
    
    time.sleep(0.2)

