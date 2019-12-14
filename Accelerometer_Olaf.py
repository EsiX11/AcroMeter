import board
import digitalio
import busio
import time
import adafruit_mma8451


class mode:
    #Pins start from the 6th from top
    in1 = digitalio.DigitalInOut(board.D18) 
    #DO NOT USE (gnd)
    in2 = digitalio.DigitalInOut(board.D23) 
    in3 = digitalio.DigitalInOut(board.D24)
    #DO NOT USE (gnd)
    #in4 = digitalio.DigitalInOut(board.D25)
    #in5 = digitalio.DigitalInOut(board.D8)
    #in6 = digitalio.DigitalInOut(board.D7)
    #DO NOT USE Reserved
    #DO NOT USE (gnd)
    #in7 = digitalio.DigitalInOut(board.D12)
    #DO NOT USE (gnd)
    #in8 = digitalio.DigitalInOut(board.D16)
    #in9 = digitalio.DigitalInOut(board.D20)
    #in10 = digitalio.DigitalInOut(board.D21)

    in1.direction = digitalio.Direction.INPUT 
    in2.direction = digitalio.Direction.INPUT
    in3.direction = digitalio.Direction.INPUT
    #in1.direction = digitalio.Direction.INPUT 
    #in2.direction = digitalio.Direction.INPUT
    #in3.direction = digitalio.Direction.INPUT
    #in4.direction = digitalio.Direction.OUTPUT 
    #in5.direction = digitalio.Direction.OUTPUT
    #in6.direction = digitalio.Direction.OUTPUT
    #in7.direction = digitalio.Direction.INPUT
    #in8.direction = digitalio.Direction.OUTPUT 
    #in9.direction = digitalio.Direction.OUTPUT
    #in10.direction = digitalio.Direction.OUTPUT
    
    in1.pull = digitalio.Pull.UP
    in2.pull = digitalio.Pull.UP
    in3.pull = digitalio.Pull.UP
    
    def getMode():
        modeSelect = 0
        if (not(mode.in1.value)):
            modeSelect = 1
        elif (not(mode.in2.value)):
            modeSelect = 2
        elif (not(mode.in2.value)):
            modeSelect = 3
        return(modeSelect)


class setup:
    
    #Sets the threshold of when the sensor should active. Takes 1G (9.8 m/s^2) and times that by user input number.
    #Standard is 1G
    def positiveThreshold(xMin, yMin):
        this = acroMeter
        this.xPosThreshold = (this.posOneG * xMin)
        this.yPosThreshold = (this.posOneG * yMin)
        
    #Sets the threshold of when the sensor should active. Takes -1G (-9.8 m/s^2) and times that by user input number.
    #Standard is -1G   
    def negativeThreshold(xMin, yMin):
        this = acroMeter
        this.xNegThreshold = (this.negOneG * xMin)
        this.yNegThreshold = (this.negOneG * yMin)
        
    #Sets the both threshold for negative G and positive G. Takes 1G (9.8 m/s^2) and -1G (-9.8 m/s^2) times that
    #by user input number. If you want to change negative seperate use bellow function
    #Standard is 1G and -1G if not changed
    def Threshold(xMin, yMin):
        setup.positiveThreshold(xMin, yMin);
        setup.negativeThreshold(xMin, yMin);

    #prints out set values to check whether it was set correct
    def printValues():
        this = acroMeter
        print("X positive threshold G:(" , (this.xPosThreshold / this.posOneG), ") Y positive threshold G:(",  (this.yPosThreshold / this.posOneG), ")")
        print("X negative threshold G:(" , (this.xNegThreshold / this.negOneG), ") Y negative threshold G:(" , (this.yNegThreshold / this.negOneG), ")")
      
   

class acroMeter:

    posOneG = float(9.8)
    negOneG = float(-9.8)
    
    xPosThreshold = float(format(9.8, '.3f'))
    yPosThreshold = float(format(9.8 , '.3f'))
    xNegThreshold = float(format(-9.8, '.3f'))
    yNegThreshold = float(format(-9.8 , '.3f'))
    
    
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_mma8451.MMA8451(i2c)

    sensor.range = adafruit_mma8451.RANGE_2G #2G is the lowest so we can update it the fastest
    sensor.data_rate = adafruit_mma8451.DATARATE_800HZ #800HZ is the fastest it can update
    

    #List of all outputs. Increase list to increase amount of outputs. (Left side of Raspi pins)
    out1 = digitalio.DigitalInOut(board.D17) #Red LED (Going Left)
    out2 = digitalio.DigitalInOut(board.D27) #Blue LED (Going forward) Both Red and Green (Braking or reverse)
    out3 = digitalio.DigitalInOut(board.D22) #Green LED (Going Right)

    #uncomment for more outputs. Output list going downwards. (DO NOT USE) = unusable output
    #DO NOT USE (3.3V)
    #out4 = digitalio.DigitalInOut(board.D10)#reserved 
    #out5 = digitalio.DigitalInOut(board.D9)#reserved
    #out6 = digitalio.DigitalInOut(board.D11)#reserved
    #DO NOT USE (gnd)
    #DO NOT USE (reserved)
    #out7 = digitalio.DigitalInOut(board.D5) #reserved
    #out8 = digitalio.DigitalInOut(board.D6) #reserved
    #out9 = digitalio.DigitalInOut(board.D13) #reserved
    #out10 = digitalio.DigitalInOut(board.D19) #reserved
    #out11 = digitalio.DigitalInOut(board.D26) #reserved
    #DO NOT USE (gnd)

    
    out1.direction = digitalio.Direction.OUTPUT 
    out2.direction = digitalio.Direction.OUTPUT
    out3.direction = digitalio.Direction.OUTPUT
    #out4.direction = digitalio.Direction.OUTPUT 
    #out5.direction = digitalio.Direction.OUTPUT
    #out6.direction = digitalio.Direction.OUTPUT
    #out7.direction = digitalio.Direction.OUTPUT 
    #out8.direction = digitalio.Direction.OUTPUT
    #out9.direction = digitalio.Direction.OUTPUT
    #out10.direction = digitalio.Direction.OUTPUT 
    #out11.direction = digitalio.Direction.OUTPUT

    out1.value = True
    out2.value = True
    out3.value = True
    
   
    def auto():
        this = acroMeter #cuz I'm lazy
        x, y, z = this.sensor.acceleration
        if (x > this.xPosThreshold):  #Left turn
            print("x = {0:0.3f} Left turn".format(x))
            this.out1.value = False
        if (y > this.yPosThreshold): #Forward (gas)
            print("y = {0:0.3f} Forward (Gas)".format(y))
            this.out2.value = False
        if (x < this.xNegThreshold): #Right turn
            print("x = {0:0.3f} Right turn".format(x))
            this.out3.value = False
        if (y < this.yNegThreshold): #brake
             print("y = {0:0.3f} Reverse or braking".format(y))
             this.out3.value = False
             this.out1.value = False
        elif (not(y < this.yNegThreshold)): #Makes sure that if braking it doesn't turn of the leds
            if (not(y > this.yPosThreshold)): #Not Forward (gas)
                this.out2.value = True
            if (not(x > this.xPosThreshold) and not(x < this.xNegThreshold)):  #Not turning
                this.out1.value = True
                this.out3.value = True
        if (z < -7.8):
            print("Ooh shit!")
    
    def fullWing():
        this = acroMeter #cuz I'm lazy
        this.out1.value = False
        this.out3.value = False
    
    def noWing():
        this = acroMeter #cuz I'm lazy
        this.out1.value = True
        this.out3.value = True