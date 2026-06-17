#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# *** Simple Single File PyAres Planner Template ***

# -----------------------------------------------------------------------------
# 1. Import Necessary Modules
# -----------------------------------------------------------------------------
from PyAres import AresDeviceService, DeviceSchemaEntry, DeviceCommandDescriptor, AresDataType # Required for the PyAres Service
import serial, time # For example logic, feel free to delete if not needed


# -----------------------------------------------------------------------------
# 2. Define Your Service Details 
# -----------------------------------------------------------------------------
name = "<The name of your device>"
description = "<Description of your device>"
serial_port = "<serial_port" # The port your device will use to communicate, e.g. something like 'COM3' on windows or '/dev/ttyUSB0' on Linux/Mac.
baud_rate = 9600 # The baud rate your device will use for serial communications.
version = "<X.X.X>" # device version numbering that will be reported to ARES OS.
port =  7310 # The network port your device will use to communicate with ARES OS.
local = True # Whether to use localhost or not

# ----------------------------------------------------------------------------- 
# 3. Define the Device Class(s)
# -----------------------------------------------------------------------------
# NOTE: This implements a basic python driver for the included arduino example, replace with your own device logic
class arduino_device:
    '''
    This an implementation of basic communication with the example arduino device
    '''
    def __init__(self,port,baud_rate=9600):
        self.port = port
        self.baud_rate=baud_rate
        try:
            # Initialize Serial Connection
            self.arduino = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2) # Wait for Arduino to reset after connection
            print(f"Connected to Arduino on {port}")
        
        except Exception as e:
            print(f"Error connecting: {e}")
            raise
    
    def send_command(self,cmd):
        """Helper function to send a command and return the response"""
        # Add newline character as the Arduino expects readStringUntil('\n')
        self.arduino.write((cmd + '\n').encode('utf-8')) 
        
        # Read the response line
        response = self.arduino.readline().decode('utf-8').strip()
        return response
    
    def close(self):
        #Closes the serial connection#
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            print("Connection closed.")


class pyares_device:
    '''
    Often we may not have direct access to the the device driver, so it makes sense to make a wrapper class that 
    can be used to implment ARES OS required functions or convenience commands
    '''
    def __init__(self, port, baud_rate=9600):
        self.device = arduino_device(port, baud_rate)
    
    # Define conveneince functions for all the device commands
    # Even if a function doesn't actually return anything useful it is still good practice to have a return in the function. Otherwise ARES will immediately move on 
    # to the next command, which can lead to unexpected behavior.
    def led_toggle(self):
        # Toggle LED
        return self.device.send_command('LED_TOGGLE')

    def led_state(self):
        # Query LED State
        return self.device.send_command('LED_STATE')
    
    def read_A0(self):
        # Read Voltage on pin A0
        return self.device.send_command('READ_A0')
    
    def set_value(self,value):
        # Set a stored value
        return self.device.send_command(f'SET_VAL:{value}')
    
    def get_value(self):
        #retreive a stored value
        return self.device.send_command('GET_VAL')

    # `get_device_state` and `enter_safe_mode` are required commands for ARES OS devices

    def get_device_state(self):
        state_dictionary = {
                            "LED State": self.led_state(),
                            "Voltage": self.read_A0(),
                            "User Value": self.get_value(),
                            }
        return state_dictionary
  
    def enter_safe_mode(self):
        # Turn off the LED and set the value to zero as an example of making a device "Safe"
        if self.led_state() == "ON":
            self.led_toggle()
        self.set_value(0)

    
# -----------------------------------------------------------------------------
# 4. Configure and Start Device Service.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    device = pyares_device(serial_port, baud_rate)

    device_service = AresDeviceService(device.enter_safe_mode,
                                       device.get_device_state,
                                       name,
                                       version,
                                       description, 
                                       use_localhost=local, 
                                       port=port)
    
    # Configuring input and output schema for the availible device commands
    # Toggle LED command
    toggle_led_desc = DeviceCommandDescriptor(name="Toggle LED",
                                              description="Toggles the state of LED on the device.", 
                                              input_schema={}, # The toggle LED commands has no Inputs or Outputs
                                              output_schema={})
    device_service.add_new_command(toggle_led_desc,device.led_toggle)

    # Get LED state command
    # Tell ARES what the output from the command should expect 
    led_state_output_schema = {
        "LED State": DeviceSchemaEntry(type=AresDataType.STRING,
                                       description="Current State of the device LED",
                                       unit="")
        }
    led_state_desc = DeviceCommandDescriptor("Get LED State","Gets the current state of the LED on the device.",{},led_state_output_schema)
    device_service.add_new_command(led_state_desc,device.led_state)

    # Get Voltage command
    voltage_output_schema = {
        "voltage": DeviceSchemaEntry(type=AresDataType.NUMBER,
                                     description="Voltage on Pin A0",
                                     unit="V")
        }
    voltage_desc = DeviceCommandDescriptor("Read Voltage on Pin A0","Reads the voltage from Pin A0 on the device",{},voltage_output_schema)
    device_service.add_new_command(voltage_desc,device.read_A0)

    # Set Value command
    # This command takes an input, so we need an input schema.
    # NOTE: The name(s) of the value in the input schema should match the name(s) of the input variables in your command
    value_schema = {
        'value':DeviceSchemaEntry(type=AresDataType.NUMBER,
                                  description="Value stored on the device",
                                  unit="")
    }
    set_value_desc = DeviceCommandDescriptor("Set the stored value","Sets the stored value on the device",value_schema,{})
    device_service.add_new_command(set_value_desc,device.set_value)

    # Get Value Command
    # NOTE: We can recycle the same schema for the value
    get_value_desc = DeviceCommandDescriptor("Get the stored value","Gets the stored value on the device",{},value_schema)
    device_service.add_new_command(get_value_desc,device.get_value)

    # It is a good idea to wrap running the service in a try/except/finally block to enable graceful shutdown of any connections
    try:
        device_service.start()
    except KeyboardInterrupt:
        print("Shutting down device service...")
    except Exception as e:
        print("An error occurred while running the device service: ", e)
    finally:
        device.device.close()