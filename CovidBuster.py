#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set GPIO Pins
GPIO_TRIGGER = 17
GPIO_ECHO = 21
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

Red=20
Green=12
Blue=19
GPIO.setup(Red,GPIO.OUT)
GPIO.setup(Green,GPIO.OUT)
GPIO.setup(Blue,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
p=GPIO.PWM(26,50)
p2=GPIO.PWM(16,50)
time.sleep(2)
#Function to move the servo motors by a specified angle
def setAngle(angle,motor,pin):
    duty = angle / 18 + 3  
    GPIO.output(pin, True)
    motor.ChangeDutyCycle(duty)
    time.sleep(0.1)
    GPIO.output(pin, False)
    motor.ChangeDutyCycle(duty)
    

setAngle(90,p,26)
setAngle(0,p2,16)
# Function to clean up LED
def Refresh(Red,Green,Blue):
    GPIO.output(Red,False)
    GPIO.output(Blue,False)
    GPIO.output(Green,False)

# Function to sense the object by sensor
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    stage = False
    try:
        while True:
            dist = distance()
            #print ("Measured Distance = %.1f cm" % dist)
            if dist < 25 :
                stage = True
                Refresh(Red,Green,Blue)
                GPIO.output(Blue,True)
                p.start(0)
                p2.start(90)
                setAngle(0,p,26)
                setAngle(90,p2,16)
                setAngle(90,p,26)
                setAngle(0,p2,16)
            else:
                if stage == True :
                    Refresh(Red,Green,Blue)
                    for x in range(20):
                        GPIO.output(Green,True)
                        time.sleep(0.5)
                        GPIO.output(Green,False)
                        time.sleep(0.5)
                    stage=False
                else:
                    Refresh(Red,Green,Blue)
                    GPIO.output(Red,True)
                    
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
