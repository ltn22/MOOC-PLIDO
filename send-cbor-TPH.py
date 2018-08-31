import BME280
import CBOR as cbor
from network import LoRa
import socket
import time
import binascii
import pycom

from machine import I2C

i2c = I2C(0, I2C.MASTER, baudrate=400000)
print (i2c.scan())

bme = BME280.BME280(i2c=i2c)

lora = LoRa(mode=LoRa.LORAWAN)

print ("devEUI {}".format(binascii.hexlify(lora.mac())))

app_eui = binascii.unhexlify('00 00 00 00 00 00 00 00'.replace(' ',''))
app_key = binascii.unhexlify('11 22 33 44 55 66 77 88 11 22 33 44 55 66 77 88'.replace(' ',''))
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key),  timeout=0)

pycom.heartbeat(False)
pycom.rgbled(0x111111)


while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

pycom.rgbled(0x000000)

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
#s.bind(5)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
s.setsockopt(socket.SOL_LORA,  socket.SO_CONFIRMED,  False)

nbMsg = 1

while True:
    temp = bme.read_temperature()
    humi = bme.read_humidity()
    pres = bme.read_pressure()

    c = cbor.dumps([nbMsg, int(temp*100), int(pres*100), int(humi*100)])
    print (c)
    nbMsg += 1


    s.setblocking(True)
    s.settimeout(10)

    try:
        s.send(c.value())
    except:
        print ('timeout in sending')

    try:
        data = s.recv(64)
        print(data)
        led_json = cbor.loads(data)
        print (led_json)
        led_color = 0x000000
        for i in range(0, 3):
            led_color <<= 8
            led_color += led_json[i]

        print (hex(led_color))
        pycom.rgbled(led_color)

    except:
        print ('timeout in receive')
        pycom.rgbled(0x000000)


    s.setblocking(False)

    time.sleep (10)
