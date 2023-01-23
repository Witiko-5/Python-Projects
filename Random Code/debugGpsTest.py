import serial
import time
import pynmeagps

#initialize serial port
stream = serial.Serial('/dev/ttyAMA0', 9600, timeout=3)

while True:
    try:
#Capture and split RMC NMEA data from serial /dev/ttyAMA0 port
        stm_bytes = stream.readline()
        decoded_stm = stm_bytes.decode("utf-8")
        stm = decoded_stm.split(",")
        
        if stm[0] == '$GPRMC':
            utc_time = stm[1]
            status = stm[2]
            latitude = stm[3]
            lat_dir = stm[4]
            longitude = stm[5]
            lon_dir = stm[6]
            speed = stm[7]
            compass_dir = stm[8]
            date = stm[9]
            
#Convert UTC time to EST, print as well
            a1 = utc_time[0] + utc_time[1]
            a2 = (int(a1) - 4) % 24
            a3 = str(a2)
            stnd_utc_time = "{}:{}:{}".format(utc_time[0] + utc_time[1], utc_time[2] + utc_time[3], utc_time[4] + utc_time[5])
            stnd_est_time = "{}:{}:{}".format(a3, utc_time[2] + utc_time[3], utc_time[4] + utc_time[5])
            
            print("\nTime (EST): {}".format(stnd_est_time), end='          ')
            print("Time (UTC): {}".format(stnd_utc_time), end='      ')
            print("Date: {}/{}/{}".format(date[2] + date[3], date[0] + date[1], date[4] + date[5]))

#Determine status / if lat or lon are empty, print shit
            if(status == 'A'):
                print("\nStatus: Good\n")
                if(status == 'A' and latitude != 0 and longitude != 0):
                    print("Latitude: {}, {}".format(latitude, lat_dir), end='          ')
                    print("Longitude: {}, {}".format(longitude, lon_dir))
                    
                    print("Current Direction: {}".format(compass_dir), end='          ')
                    print("Speed: {} knots".format(speed))
                else:
                    print("\nStatus Good, Lat or Lon = 0\n")
            else:
                print("\nStatus: No fix, please wait...\n")
        
        if stm[0] == '$GPGSA':
            sat_used = stm[3]
            if sat_used != '':
                print("Satellites used: {}".format(sat_used))
            else:
                print("null\n")
        
        if stm[0] == '$GPGSV':
            sats_in_view = stm[3]
            print("Sats in view: {}".format(sats_in_view), end=' ')
    break  
        
    except UnicodeDecodeError:
        print("oops                             ")
        continue

    # except serial.SerialException:
#     print("There is no GPS connected :(")