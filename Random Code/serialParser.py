import serial
import threading



def readStream():
    stream = serial.Serial('/dev/ttyAMA0', 9600, timeout=3)

    output = open("guiWrite.txt", "w")

    blockID = 0
    while True:
        try:
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

                a1 = utc_time[0] + utc_time[1]
                a2 = (int(a1) - 4) % 24
                a3 = str(a2)
                stnd_utc_time = "{}:{}:{}".format(utc_time[0] + utc_time[1], utc_time[2] + utc_time[3], utc_time[4] + utc_time[5])
                stnd_est_time = "{}:{}:{}".format(a3, utc_time[2] + utc_time[3], utc_time[4] + utc_time[5])
            
                #Values: ID numbers, EST, UTC, date, status

                output.write("\n{}".format(blockID))
                output.write("\n{}".format(stnd_est_time))
                output.write("\n{}".format(stnd_utc_time))
                output.write("\n{}{}{}".format(date[2] + date[3], date[0] + date[1], date[4] + date[5]))

                #Values: Lat, lat dir, lon, lon dir, compass direction, speed

                if status == 'A':
                    output.write("good")
                    if(status == 'A' and latitude != '' and longitude != ''):
                        output.write("\n{}".format(latitude))
                        output.write("\n{}".format(lat_dir))
                        output.write("\n{}".format(longitude))
                        output.write("\n{}".format(lon_dir))
                        output.write("\n{}".format(compass_dir))
                        output.write("\n{}".format(speed))

                        blockID = blockID + 1
                        output.flush()
                        break
                    else:
                        #Status = "good", no latitude or longitude readings
                        output.write("\n0")

                        blockID = blockID + 1
                        output.flush()
                        break
                else:
                    #No fix
                    output.write("\n0")

                    blockID = blockID + 1
                    output.flush()
                    break

        except UnicodeDecodeError:
            continue
                
    


    

            

