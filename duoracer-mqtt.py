#!/usr/bin/env python3
import minimalmodbus
import serial
import paho.mqtt.client as mqtt
import json
import time

# MQTT setup
broker = "192.168.1.184"
client = mqtt.Client("duoracer_rs485")
client.connect(broker)

# modbus setup
instrument = minimalmodbus.Instrument("/dev/ttyXRUSB0", 1)

instrument.serial.baudrate = 115200
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 0.2

instrument.mode = minimalmodbus.MODE_RTU
instrument.clear_buffers_before_each_transaction = True

# Holding registers
PV_VOLTAGE = 0x3100
PV_CURRENT = 0x3101
PV_POWER = 0x3102
BAT_VOLTAGE = 0x331A
BAT_POWER = 0x3106
BAT_CURRENT = 0x331B
BAT_SOC = 0x311A
BAT_TEMP = 0x3110
BAT_VMIN = 0x3303
BAT_VMAX = 0x3302
EQUIPMENT_TEMP = 0x3111


# Read solar panel data from registers
pv_voltage = instrument.read_register(PV_VOLTAGE, 2, 4, False)
pv_current = instrument.read_register(PV_CURRENT, 2, 4, False)
pv_power = instrument.read_register(PV_POWER, 2, 4, False)

#print("Solar panel data:")
#print("Panel voltage:\t" + str(pv_voltage) + " V")
#print("Panel current:\t" + str(pv_current) + " A")
#print("Panel power:\t" + str(pv_power) + " W")
#print()

# Read battery data from registers
bat_voltage = instrument.read_register(BAT_VOLTAGE, 2, 4, False)
bat_power = instrument.read_register(BAT_POWER, 2, 4, False)
bat_current = instrument.read_register(BAT_CURRENT, 2, 4, False)
bat_soc = instrument.read_register(BAT_SOC, 2, 4, False)
bat_soc *= 100

bat_temp = instrument.read_register(BAT_TEMP, 2, 4, False)
bat_vmin = instrument.read_register(BAT_VMIN, 2, 4, False)
bat_vmax = instrument.read_register(BAT_VMAX, 2, 4, False)
#print("Battery data:")
#print("Battery voltage:\t" + str(bat_voltage) + " V")
#print("Battery power:\t" + str(bat_power) + " W")
#print("Battery current:\t" + str(bat_current) + " A")
#print("Battery SoC:\t" + str(bat_soc) + " %")
#print("Battery temperature:\t" + str(bat_temp) + " C")
#print("Battery Vmin today:\t" + str(bat_vmin) + " V")
#print("Battery Vmax today:\t" + str(bat_vmax) + " V")
#print()

# Read equipment temperature data
duoracer_temp = instrument.read_register(EQUIPMENT_TEMP, 2, 4, False)
#print("Duoracer temperature:\t" + str(duoracer_temp) + " C")
#print()



# MQTT Autodiscovery config
client.publish("homeassistant/sensor/solar_panel_voltage/config",
               json.dumps({"name": "Solar Panel Voltage",
                           "icon": "mdi:solar-power",
                           "unit_of_measurement": "V",
                           "state_topic": "homeassistant/sensor/solar_panel_voltage",
                           "unique_id": "spv_id"}),
               retain=True)

client.publish("homeassistant/sensor/solar_panel_current/config",
               json.dumps({"name": "Solar Panel Current",
                           "icon": "mdi:solar-power",
                           "unit_of_measurement": "A",
                           "state_topic": "homeassistant/sensor/solar_panel_current",
                           "unique_id": "spc_id"}),
               retain=True)

client.publish("homeassistant/sensor/solar_panel_power/config",
               json.dumps({"name": "Solar Panel Power",
                           "icon": "mdi:solar-power",
                           "unit_of_measurement": "W",
                           "state_topic": "homeassistant/sensor/solar_panel_power",
                           "unique_id": "spp_id"}),
               retain=True)

client.publish("homeassistant/sensor/battery_voltage/config",
               json.dumps({"name": "Leisure battery Voltage",
                           "icon": "mdi:battery",
                           "unit_of_measurement": "V",
                           "state_topic": "homeassistant/sensor/battery_voltage",
                           "unique_id": "bv_id"}),
               retain=True)

client.publish("homeassistant/sensor/battery_power/config",
               json.dumps({"name": "Leisure battery Power",
                           "icon": "mdi:battery",
                           "unit_of_measurement": "W",
                           "state_topic": "homeassistant/sensor/battery_power",
                           "unique_id": "bp_id"}),
               retain=True)

client.publish("homeassistant/sensor/battery_current/config",
               json.dumps({"name": "Leisure battery Current",
                           "icon": "mdi:battery",
                           "unit_of_measurement": "A",
                           "state_topic": "homeassistant/sensor/battery_current",
                           "unique_id": "bc_id"}),
               retain=True)

client.publish("homeassistant/sensor/battery_soc/config",
               json.dumps({"name": "Leisure battery State of Charge",
                           "icon": "mdi:battery",
                           "unit_of_measurement": "%",
                           "state_topic": "homeassistant/sensor/battery_soc",
                           "unique_id": "bsoc_id"}),
               retain=True)

client.publish("homeassistant/sensor/battery_temp/config",
               json.dumps({"name": "Leisure battery Temperature",
                           "icon": "mdi:thermometer",
                           "unit_of_measurement": "°C",
                           "state_topic": "homeassistant/sensor/battery_temp",
                           "unique_id": "bt_id"}),
               retain=True)

client.publish("homeassistant/sensor/battery_vmin/config",
               json.dumps({"name": "Leisure battery Minimum Voltage",
                           "icon": "mdi:battery",
                           "unit_of_measurement": "V",
                           "state_topic": "homeassistant/sensor/battery_vmin",
                           "unique_id": "bvm_id"}),
               retain=True)

client.publish("homeassistant/sensor/battery_vmax/config",
               json.dumps({"name": "Leisure battery Maximum Voltage",
                           "icon": "mdi:battery",
                           "unit_of_measurement": "V",
                           "state_topic": "homeassistant/sensor/battery_vmax",
                           "unique_id": "bvx_id"}),
               retain=True)

client.publish("homeassistant/sensor/equipment_temp/config",
               json.dumps({"name": "DuoRacer Controller Temperature",
                           "icon": "mdi:thermometer",
                           "unit_of_measurement": "°C",
                           "state_topic": "homeassistant/sensor/equipment_temp",
                           "unique_id": "et_id"}),
               retain=True)


client.publish("homeassistant/sensor/startbattery_voltage/config",
               json.dumps({"name": "Car Battery Voltage",
                           "icon": "mdi:car-battery",
                           "unit_of_measurement": "V",
                           "state_topic": "homeassistant/sensor/startbattery_voltage",
                           "unique_id": "startbattery_voltage"}),
               retain=True)

client.publish("homeassistant/sensor/startbattery_current/config",
               json.dumps({"name": "Car Battery Current",
                           "icon": "mdi:car-battery",
                           "unit_of_measurement": "A",
                           "state_topic": "homeassistant/sensor/startbattery_current",
                           "unique_id": "startbattery_current"}),
               retain=True)


client.publish("homeassistant/sensor/startbattery_power/config",
               json.dumps({"name": "Car Maximum Power",
                           "icon": "mdi:car-battery",
                           "unit_of_measurement": "W",
                           "state_topic": "homeassistant/sensor/startbattery_power",
                           "unique_id": "startbattery_power"}),
               retain=True)


# Read from modbus and publish to MQTT
client.publish("homeassistant/sensor/solar_panel_voltage", str(pv_voltage))
time.sleep(0.1)
client.publish("homeassistant/sensor/solar_panel_current", str(pv_current))
time.sleep(0.1)
client.publish("homeassistant/sensor/solar_panel_power", str(pv_power))
time.sleep(0.1)
client.publish("homeassistant/sensor/battery_voltage", str(bat_voltage))
time.sleep(0.1)
client.publish("homeassistant/sensor/battery_power", str(bat_power))
time.sleep(0.1)
client.publish("homeassistant/sensor/battery_current", str(bat_current))
time.sleep(0.1)
client.publish("homeassistant/sensor/battery_soc", str(bat_soc))
time.sleep(0.1)
client.publish("homeassistant/sensor/battery_temp", str(bat_temp))
time.sleep(0.1)
client.publish("homeassistant/sensor/battery_vmin", str(bat_vmin))
time.sleep(0.1)
client.publish("homeassistant/sensor/battery_vmax", str(bat_vmax))
time.sleep(0.1)
client.publish("homeassistant/sensor/equipment_temp", str(duoracer_temp))
time.sleep(0.1)

# disconnect from MQTT server
client.disconnect()
