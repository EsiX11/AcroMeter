import Accelerometer_Olaf as sensor

def main():
    print("==============================Running==============================")
    #Postive X = Left turn
    #Negative X = Right turn
    #Positive Y = Forward (Gas)
    #Negative Y = Reverse or braking
    #Setting threshold to 1G means it will trigger after going over 1G
    sensor.setup.Threshold(0.7,0.7); #X & Y values in 1G. So 0.5 is Half a G (0.5G)
    #setup.positiveThreshold(1,1); #Uncomment to change X and Y values separtly
    #setup.negativeThreshold(1,1); #Uncomment to change X and Y values separtly
    sensor.setup.printValues();
    while True:
        if (sensor.mode.getMode() == 0):
            sensor.acroMeter.auto();
        elif (sensor.mode.getMode() == 1):
            sensor.acroMeter.fullWing();
        elif (sensor.mode.getMode() == 2):
            sensor.acroMeter.noWing();
main();
