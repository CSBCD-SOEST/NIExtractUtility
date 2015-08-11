import copy
import csv
import os

"""
Engineering Notes:

[#1] VFS 1-20 @port_assignments
================================================================================
ai0  : temperature sensor
ai1  : flow sensor
ai2  : Temperature_2 
ai3  : Flow_2 
ai4  : Temperature_3 
ai5  : Flow_3 
ai6  : Temperature_5 
ai7  : Flow_5 
ai8  : Temperature_4 
ai9  : Flow_4 
ai10 : Flow_6 
ai11 : Temperature_7 
ai12 : Flow_8 
ai13 : Temperature_8 
ai14 : Flow_7 
ai15 : Temperature_6 

Input File
================================================================================
Datetime Stamp, Sensor ID, Value, Comments

Output File
================================================================================
Datetime Stamp, Sensor ID, Value, Comments, Converted Value
"""

def convert_flow(voltage):
    """
    Input(s):
    @voltage: (int/float) The output voltage from the Grundfos sensor

    Returns: (float) The flow rate in l/min

    Notes:
    Computes the l/min:
        flow_rate = 6.6522 x output_voltage - 2.5396

    This equation was derived from experiments to measure the accuracy of the
    sensor, which can be located as an Excel spreadsheet in the data sheet
    folder

    The ideal equation provided by the company is:
        flow_rate = (187/30) x voltage - (109/60)
    """
    return 6.6522*float(voltage)-2.5396

def convert_temperature(voltage):
    """
    Input(s):
    @voltage: (int/float) The output voltage from the Grundfos sensor

    Returns: (float) The temperature in Fahrenheit

    Notes:
    Computes the ideal temperature:
        temperature = (100/3) x output_voltage - (100/6)
    """
    return celsius_fahrenheit((100.0/3.0)*float(voltage)-(100.0/6.0))

def celsius_fahrenheit(temperature):
    """
    Input(s):
    @temperature: (int/float) Temperature in Celsius

    Returns: (float) The temperature in Fahrenheit

    Notes:
    Converts from Celsius to Fahrenheit
        F = (9/5) x C + 32
    """
    return (9.0/5.0)*temperature+32.0

def convert_output(input_location, output_location):
    """
    Input(s):
    @input_location: (string) input direction path
    @output_location: (string) output direction path

    Returns: Nothing, however it will generate a CSV with the tag '_output'

    Notes:
    Takes a CSV with data collected from a Grundfos VFS sensor and converts the
    voltage data to something that is usable for research
    """
    print "Input:\t", input_location
    print "Output:\t", output_location
    print "\nStarting conversion...\n"
    error_count = 0
    data_count = 0
    for item in os.listdir(input_location):
        item_target = item.split(".")
        #Target the extension of the file name
        extension_target = item_target[len(item_target)-1]
        if extension_target == "CSV" or extension_target == "csv":
            print "Input File:\t", item
            output = ""
            #Create output file name
            for part in item_target:
                #Reconstruct the file name
                if part != extension_target:
                    output = output + part
                #Insert the output tag and finalize the file name
                else:
                    output = output + "_output." + extension_target
            print "Output File:\t", output
            #Generate a path to the output file
            output_path = os.path.join(output_location, output)
            with open(output_path, "wb") as output_file:
                output_writer = csv.writer(output_file)
                #Generate a path to the input file
                item_path = os.path.join(input_location, item)
                with open(item_path, "r") as item_file:
                    item_reader = csv.reader(item_file)
                    #Skip the header
                    item_reader.next()
                    for row in item_reader:
                        output_buffer = []
                        output_buffer = copy.deepcopy(row)

                        #Edit following list when adding more sensors
                        #=======================================================
                        #[#1] VFS 1-20 temperature sensor
                        if row[1] == "ai0":
                            output_buffer.append(convert_temperature(row[2]))
                        #[#1] VFS 1-20 flow sensor
                        elif row[1] == "ai1":
                            output_buffer.append(convert_flow(row[2]))
                        elif row[1] == "ai2":
                            output_buffer.append(convert_temperature(row[2]))
                        elif row[1] == "ai3":
                            output_buffer.append(convert_flow(row[2]))
                        elif row[1] == "ai4":
                            output_buffer.append(convert_temperature(row[2]))
                        elif row[1] == "ai5":
                            output_buffer.append(convert_flow(row[2]))
                        elif row[1] == "ai6":
                            output_buffer.append(convert_temperature(row[2]))
                        elif row[1] == "ai7":
                            output_buffer.append(convert_flow(row[2]))
                        elif row[1] == "ai8":
                            output_buffer.append(convert_temperature(row[2]))
                        elif row[1] == "ai9":
                            output_buffer.append(convert_flow(row[2]))
                        elif row[1] == "ai10":
                            output_buffer.append(convert_flow(row[2]))
                        elif row[1] == "ai11":
                            output_buffer.append(convert_temperature(row[2]))
                        elif row[1] == "ai12":
                            output_buffer.append(convert_flow(row[2]))
                        elif row[1] == "ai13":
                            output_buffer.append(convert_temperature(row[2]))
                        elif row[1] == "ai14":
                            output_buffer.append(convert_flow(row[2]))
                        elif row[1] == "ai15":
                            output_buffer.append(convert_temperature(row[2]))
                        else:
                            #Increment error count
                            error_count = error_count + 1
                            print "error @ "  + row[1]
                            continue
                        #======================================@port_assignments

                        data_count = data_count + 1
                        output_writer.writerow(output_buffer)
    print "\nConversion completed...\n"
    print "Number of data points: ", data_count
    print "Number of errors: ", error_count
