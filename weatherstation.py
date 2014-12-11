import os
import glob
import time
import httplib
import urllib

os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')

from datetime import datetime, timedelta

base_dir = '/sys/bus/w1/devices/'
device_folder = ''
# = glob.glob(base_dir + '*')[0]
device_file = ''
#device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
#    lines = read_temp_raw()

    for filename in os.listdir(base_dir):
        global device_folder
        device_folder = filename
        global device_file
        device_file = base_dir + device_folder + '/w1_slave'
        print device_file
        if device_file.find('master') == -1:
            lines = read_temp_raw()
    
#            print(lines)
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = read_temp_raw()
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
               # return temp_c

#while True:
                try:
#        temp = read_temp()

                    print(temp_c)
                    params = urllib.urlencode({'UID': filename, 'Temperature': temp_c})
                    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                    conn = httplib.HTTPConnection("temperature.thematthewshouse.co.uk")
                    conn.request("POST", "/api/TemperatureReadingsAPI", params, headers)
                    response = conn.getresponse()
                    print response.status, response.reason
                    data = response.read()
                    conn.close()
                except Exception, e:
                    print e.__doc__
                    print e.message
#    time.sleep(60)


while True:
    if datetime.now().second == 0:
        read_temp()
    else:
        time.sleep(60-datetime.now().second)
