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
  
  # Define the callback function
  def my_callback(channel):
    #print(f"Edge detected on channel {channel}!")
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

    
    #time.sleep(0.2)

  # Set up event detection and callback
  GPIO.add_event_detect(GPIO_PIN_DATA, GPIO.FALLING, callback=my_callback)
  
  #tenmin_lst = [f'{i:02d}:{j:02d}:00' for i in range(24) for j in range(0, 60, 10)]
  tenmin_lst = ['{:02d}:{:02d}:00'.format(i, j) for i in range(24) for j in range(0, 60, 10)]
  
  
  while True:

    #gpio_val = GPIO.input(GPIO_PIN_DATA)

    now = datetime.datetime.now()     
     

    curr_time_str = now.time().strftime("%H:%M:%S")
    
    #send 0mm to db every 10mins
    #problem if raingauge tips exactly at 10'th minute
    if curr_time_str in tenmin_lst:
    
        try:
          print "connecting to db"
          db = MySQLdb.connect("localhost", "root", "kpapcp", "pagasa")
          print "success"
          
          curs = db.cursor()
          
          print "saving to datalogs"
          curs.execute("INSERT INTO datalogs(logtime, logtype, value, unit, description) values(NOW(), 'rr', 0.0, 'mm', 'rain rate measurement')")
          db.commit()
          print "success"
        except Exception as error:
          print "failed", error
          db.rollback()
        finally:
          curs.close()
          db.close()
    
    
    
    time.sleep(0.2)


    #else:
      #pass

    
    
    
    

    #print("waiting for sensor ...")
    #GPIO.wait_for_edge(GPIO_PIN_DATA, GPIO.FALLING)
    

