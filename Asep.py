movement = input("Input movement : ")

str_part = str(movement[0])
int_part = int(movement[1:])
speed = float(int_part * 2 /100)

if(int_part < 0 or int_part > 100):
    print ("Value Invalid")

else :
    if (str_part == "L") :
        print ("Belok kiri " + str(speed) + " m/s")
    elif (str_part == "R") :
        print ("Kanan deh " + str(speed) + " m/s")
    elif (str_part == "F") :
        print ("Maju hei " + str(speed) + " m/s")
    elif (str_part == "S") :
        print ("Mundur bapak " + str(speed) + " m/s")
