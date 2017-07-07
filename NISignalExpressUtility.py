#-------------------
# Author: Christian A. Damo
# file name: NISignalExpressUtility.py
# rev. by: Reed Shinsato
# rev. date: 2014-07-11
#------------------
#
# Patch Notes: Cleaned up class
#
#------------------
"""
    This script convertes .tdms files from NISignalExpress into .csv files.
    Then, it pushes the .csv files to a server with a specified ip.
"""

# Import Libraries
from nptdms import TdmsFile
from contextlib import contextmanager
import os
import datetime
import csv

def separatefiles():
    #dataFolder = "CalibratedCSVs"
    #uniqueid = ["temp", "flow"]
    homeDir = os.path.dirname(os.path.abspath(__file__))
    dataFileDir = os.path.join(homeDir, "CalibratedCSVs")
    tempFileDir = os.path.join(homeDir, "ADASEED", "CalibratedFlow") #CalibratedTemperature
    flowFileDir = os.path.join(homeDir, "ADASEED", "CalibratedFlow")
    csvFiles = []
    #list all files in the directory
    #print "datafileDir =" + dataFileDir
    currentDirFiles = os.listdir(dataFileDir)
    #print currentDirFiles
    #get all csvs in the directory
    for filename in currentDirFiles:
        if ".csv" in filename:
            csvFiles.append(filename)
    #print csvFiles
    for csvFile in csvFiles:
        #create two output file names
        name = csvFile
        newName = name.split('.')
        tempName = list(newName)
        flowName = list(newName)
        tempName.insert(1, "_temp.")
        newTempName = ''.join(tempName)
        flowName.insert(1, "_flow.")
        newFlowName = ''.join(flowName)
        tempFilePath = os.path.join(tempFileDir, newTempName)
        flowFilePath = os.path.join(flowFileDir, newFlowName)
        csvFilePath = os.path.join(dataFileDir, csvFile)
       # print "asdjfl" + tempFilePath
        #print flowFilePath
        with open(csvFilePath, "rb") as inputFile:
            reader = csv.reader(inputFile)
            with open(tempFilePath, "wb") as outputT:
                with open(flowFilePath, "wb") as outputF:
                    outputTwriter = csv.writer(outputT)
                    outputFwriter = csv.writer(outputF)
                    for row in reader:
                        if "Temp" in row[3]:
                            outputTwriter.writerow(row)
                        elif "Flow" in row[3]:
                            outputFwriter.writerow(row)
                        elif "Anem" in row[3]:
                            outputFwriter.writerow(row)
                            
def move_to_output():
    #dataFolder = "CalibratedCSVs"
    #uniqueid = ["temp", "flow"]
    homeDir = os.path.dirname(os.path.abspath(__file__))
    dataFileDir = os.path.join(homeDir, "CalibratedCSVs")
    outputFileDir = os.path.join(homeDir, "Output") #CalibratedTemperature
    csvFiles = []
    #list all files in the directory
    #print "datafileDir =" + dataFileDir
    currentDirFiles = os.listdir(dataFileDir)
    #print currentDirFiles
    #get all csvs in the directory
    for filename in currentDirFiles:
        if ".csv" in filename:
            csvFiles.append(filename)
    #print csvFiles
    for csvFile in csvFiles:
        #create two output file names
        name = csvFile
        outputFilePath = os.path.join(outputFileDir, name)
        csvFilePath = os.path.join(dataFileDir, csvFile)
       # print "asdjfl" + tempFilePath
        #print flowFilePath
        with open(csvFilePath, "r") as inputFile:
            reader = csv.reader(inputFile)
            with open(outputFilePath, "w") as output:
                outputwriter = csv.writer(output)
                for row in reader:
                    if "Temp" in row[3]:
                        outputwriter.writerow(row)
                    elif "Flow" in row[3]:
                        outputwriter.writerow(row)
                    elif "Anem" in row[3]:
                        outputwriter.writerow(row)

#@contextmanager
#def network_share_auth(share, username = None, password = None, drive_letter = 'P'):
#    cmd_parts = ["NET USE %s: %s" % (drive_letter, share)]
#    if password:
#        cmd_parts.append(password)
#    if username:
#        cmd_parts.append("/USER:%s" % username)
#    os.system(" ".join(cmd_parts))
#    try:
#        yield
#    finally:
#        os.system("NET USE %s: /DELETE" % drive_letter)

#dictionary for tacking on a sensor name & location to a corresponding port
notes = {'Dev1ai0':"Temperature_1",
         'Dev1ai1':"Flow_1",
		 'Dev1ai2':"Temperature_2",
		 'Dev1ai3':"Flow_2",
		 'Dev1ai4':"Temperature_3",
		 'Dev1ai5':"Flow_3",
		 'Dev1ai6':"Temperature_5",
		 'Dev1ai7':"Flow_5",
		 'Dev1ai8':"Temperature_4",
		 'Dev1ai9':"Flow_4",
		 'Dev1ai10':"Flow_6",
		 'Dev1ai11':"Temperature_7",
		 'Dev1ai12':"Flow_8",
		 'Dev1ai13':"Temperature_8",
		 'Dev1ai14':"Flow_7",
		 'Dev1ai15':"Temperature_6",
         'Dev2ai0':"Temperature_9",
		 'Dev2ai8':"Flow_9",
		 'Dev2ai1':"Temperature_10",
		 'Dev2ai9':"Flow_10",
		 'Dev2ai2':"Temperature_Main",
		 'Dev2ai10':"Flow_Main",
         'Dev2ai11':"Flow_Main_Return",
         'Dev2ai3':"Temperature_Main_Return",
         'Dev2ai12':"Anem_3",
         'Dev2ai5':"Anem_2",
         'Dev2ai13':"Anem_4",
         'Dev2ai4':"Anem_1",
         'Dev2ai6':"Anem_5",
         'Dev2ai14':"Anem_6",
         'Dev2ai7':"Anem_7",
         'Dev2ai15':"Anem_8",
         'Dev3ai0':'Anem_1',
         'Dev3ai1':'Anem_1',
         'Dev3ai2':'Anem_1',
         'Dev3ai3':'Anem_1',
         'Dev3ai4':'Anem_1',
         'Dev3ai5':'Anem_1',
         'Dev3ai6':'Anem_1',
         'Dev3ai7':'Anem_1',
         'Dev3ai8':'Anem_1',
         'Dev3ai9':'Anem_1',
         'Dev3ai10':'Anem_1',
         'Dev3ai11':'Anem_1',
         'Dev3ai12':'Anem_1',
         'Dev3ai13':'Anem_1',
         'Dev3ai14':'Anem_1',
         'Dev3ai15':'Anem_1',
         'Dev3ai16':'Anem_1'
}



# Create Classes
class GroupChannel:
    """
        This class holds the group and channel names from a metafile.
    """
    def __init__(self, meta_filename):
        #print
        self._channel_type = ""
        self._start_time = datetime.datetime.now()
        self._meta_filename = meta_filename
        self._group_name = ""
        self._channel_names = []
        self.__get_group_name(self._meta_filename)
        # self.__str__()

    def __str__(self):
        print("\nCalling GroupChannels __str__()")
        print("Type: ", self._channel_type)
        print("Start: ", self._start_time)
        print("Group Name: ", self._group_name)
        print("Channel Names: \n\n", self._channel_names)

    def __get_start_and_names(self, meta_filename, temp_names):
        """
            This function stores the start time and channel names
        """
        # Check the meta_file for " ", which is the line of the channel names.
        # Check the meta_file for "Log start time", which holds the start time.
        meta_file = open(meta_filename)
        for line in meta_file:
            if line[0] == " ":
                temp_names.append(line)
            if "Log start time" in line:
                self._start_time = self.__start_convert_to_datetime_object(line)
        meta_file.close()

    def __start_convert_to_datetime_object(self, line):
        """
            This function turns the given line into a datetime object.
        """
        # Find each element of the given line
        # Turn the elements into a datetime object
        # Return the datetime object
        line = line.split(" ")
        date = line[3]
        date = date.split("/")
        year = int(date[2])
        day = int(date[1])
        month = int(date[0])
        time = line[4]
        time = time[:-1]
        time = time.split(":")
        hour = int(time[0])
        minute = int(time[1])
        second = time[2].split(".")
        second = int(second[0])
        begin_time = datetime.datetime(year, month, day, hour, minute, second)
        return begin_time

    def __get_group_name(self, meta_filename):
        """
            This functions determines the group_name
        """
        # Get the start time and channel names
        # Determine the timestamp
        # Store the channel names
        # Determine the data type
        # Create the group name
        temp_names = []
        self.__get_start_and_names(meta_filename, temp_names)
        for line in temp_names:
            temp_line = line.split("-")
            timestamp = temp_line[0]
            timestamp = timestamp[5: -1]
            channel_name = temp_line[-1]
            channel_name = channel_name[1: -1]
            self._channel_names.append(channel_name)
            data_type = temp_line[1]
            data_type = data_type[1: -1]
            self._channel_type = data_type
            self._group_name = (timestamp + " - " + data_type +
                                " - " + "All Data")

    def return_group_name(self):
        """
            This function returns the group name.
        """
        # Retunr group_name
        return self._group_name

    def return_channel_names(self):
        """
            This function returns the channel names.
        """
        # Return channel_names
        return self._channel_names

    def return_start_time(self):
        """
            This function returns the start time.
        """
        # Return start_time
        return self._start_time

class NISignalExpressUtility:
    def __init__(self, data_location = os.path.dirname(\
        os.path.abspath(__file__)), csv_location = os.path.dirname(\
        os.path.abspath(__file__)), reshaped_location = os.path.dirname(\
        os.path.abspath(__file__)), calibrated_location = os.path.dirname(\
        os.path.abspath(__file__))):
        self._data_location = data_location
        self._csv_location = csv_location
        self._reshaped_location = reshaped_location
        self._calibrated_location = calibrated_location
        self._meta_voltage_filename = (os.path.join(self._data_location,\
            "Voltage_meta.txt"))
        self._meta_current_filename = (os.path.join(self._data_location,\
            "Current_meta.txt"))
        self._tdms_voltage_filename = (os.path.join(self._data_location,\
            "Voltage.tdms"))
        self._tdms_current_filename = (os.path.join(self._data_location,\
            "Current.tdms"))
        self._channel_names = []
        self._tdms_filenames = []
        self._GroupChannels = []
        self._tdms_to_csv_filename = str(os.path.split(data_location)[-1]) +\
            "_converted.csv"
        self._reshaped_filename = str(os.path.split(data_location)[-1]) +\
            "_reshaped.csv"
        self._converted_to_csv = False

    def __check_for_group_channels(self, tdms_filename, tdms_filenames,\
            meta_filename, channel_names, GroupChannels):
        """
            This function creates the GroupChannels.
        """
        # Create a tdms object
        # Create a GroupChannel object
        # Add to the list of channel_names
        # Add to the list of tdms_filenames
        # Add to the list of GroupChannels
        tdms_file = TdmsFile(tdms_filename)
        TypeGroupChannel = GroupChannel(meta_filename)
        type_channel_names = TypeGroupChannel.return_channel_names()
        channel_names.append(type_channel_names)
        tdms_filenames.append(tdms_file)
        GroupChannels.append(TypeGroupChannel)

    def __tdms_to_csv_file(self, channel_names, tdms_filenames,
                           GroupChannels):
        """
            This function will convert .tdms files into .csv files
        """
        # Get the data from the .tdms file
        #    Create a channel object from a tdms object
        #    Get the data from the channel
        #    Get the time from the channel
        # Clean up the channel_names to be a single array
        # Save the data into the output file
        #    Save the timestamp using delta from the start_time
        #    Save the data in a row relative to the channel_id column

        datas = []
        times = []
        for channel_names_index in range(0, len(channel_names)):
            for channel_name in channel_names[channel_names_index]:
                channel = (tdms_filenames[channel_names_index].
    		  object(GroupChannels[channel_names_index].
    		  return_group_name(), channel_name))
                data = channel.data
                datas.append(data)
                times = channel.time_track()

        temp_channel_names = []
        for channel_names_index in range(len(channel_names)):
            for name in channel_names[channel_names_index]:
                temp_channel_names.append(name)

        channel_names = []
        channel_names = temp_channel_names

        #TODO: confirm this change
        converted_file = open(os.path.join(self._csv_location,\
            self._tdms_to_csv_filename),"w")
        writer = csv.writer(converted_file)

        new_row = list(channel_names)
        new_row.insert(0, "timestamp")
        writer.writerow(new_row)
        #iterates through each time element
        for times_index in range(len(times)):
            #created delta object
            delta = datetime.timedelta(seconds = times[times_index] + 1)
            #creates the actual printed time
            current_time = GroupChannels[0].return_start_time() + delta
            #creates new line with time as element 0
            new_row = [current_time]
            #iterating through the datas list
            for datas_index in range(len(datas)):
                data = datas[datas_index][times_index]
                new_row.append(data)
            writer.writerow(new_row)
            #print new_row
            #print len(new_row)
            #raw_input("Press Enter to continue...")
        converted_file.close()


    def reshape_csv(self):
        """
            This function reshapes the data to a specific table format.
        """
        # Find the correct input file
        # Create an output file
        # Write the header
        # Clean up the channel_names
        # Write the output row with the correct format
        #    Add time to the output row
        #        Add the channel_names to the row
        #        Add the data to the row
        #        Write the row with [time, channel_names, data]
        if self._converted_to_csv == True:
            channel_names = list(self._channel_names)
            input_file = (open(os.path.join(self._csv_location,\
                self._tdms_to_csv_filename), "r"))
            reader = csv.reader(input_file)

            reshaped_file = (open(os.path.join(self._reshaped_location,\
                self._reshaped_filename), "w"))
            writer = csv.writer(reshaped_file)

            next(reader)
            new_row = ["datetime", "position", "value"]
            writer.writerow(new_row)

            temp_channel_names = []
            for channel_names_index in range(len(channel_names)):
                for names in channel_names[channel_names_index]:
                    temp_channel_names.append(names)

            channel_names = []
            channel_names = temp_channel_names
            new_channel_names = []
            for name in channel_names:
                name = name.split("_")
                name = name[0] + name[1]
                new_channel_names.append(name)
             
            for row in reader:
                current_time = row[0]
                row = row[1:]
                for new_channel_names_index in range(len(new_channel_names)):
                    new_row = []
                    new_row.append(current_time)
                    new_row.append(new_channel_names[new_channel_names_index])
                    new_row.append(float(row[new_channel_names_index]))
                    writer.writerow(new_row)

            input_file.close()
            reshaped_file.close()

    def convert_to_csv(self):
        """
            This function extracts the tdms data to the correct format.
        """
        # Check for voltage and current group channels
        # Convert the tdms files to csv
        # Reshape the csv files to the correct format
        files_found_voltage = True
        files_found_current = True
        try:
            self.__check_for_group_channels(self._tdms_voltage_filename,\
                self._tdms_filenames, self._meta_voltage_filename,\
                self._channel_names, self._GroupChannels)
        except:
            print("Note: No Voltage Files")
            files_found_voltage = False
        try:
            self.__check_for_group_channels(self._tdms_current_filename,\
                self._tdms_filenames, self._meta_current_filename,\
                self._channel_names, self._GroupChannels)
        except:
            print("Note: No Current Files")
            files_found_current = False

        if files_found_current == True or files_found_voltage == True:
            self.__tdms_to_csv_file(self._channel_names, self._tdms_filenames,\
                self._GroupChannels)
            self._converted_to_csv =  True
   
#   def add_calibration(self, sensor_id, premultiplier,
#                        preoffset, multiplier, offset):
        #  This function adds a calibration to NICalibrate.csv.
        # Open the calibration file
        # Check if the sensor_id is in the calibration file
        # Delete the calibration for the sensor_id
        # if it is in the calibration file
        # Append the new calibration to the calibration file
        #calibration_filename = "NICalibrate.csv"
        #delete_id = False
        #sensor = str(sensor_id)
        #with open(calibration_filename, "r") as calibration_file:
        #    for row in csv.reader(calibration_file):
        #        if sensor in row:
        #            delete_id = True

        #if delete_id == True:
        #    self.delete_calibration(sensor_id)

        #with open(calibration_filename, "a") as calibration_file:
        #    row = (str(sensor_id) + "," +\
        #           str(premultiplier) + "," +\
        #           str(preoffset) + "," +\
        #           str(multiplier) + "," +\
        #           str(offset) + "\n")
        #    calibration_file.write(row)
 
#    def delete_calibration(self, sensor_id):
#        """
#            This function deletes a calibration from NICalibrate.csv.
#        """
        # Copy NICalibrate.csv into a temp.csv
        # skipping the sensor_id to be deleted
        # Delete the old calibration file NICalibrate.csv
        # Rename temp.csv into the new calibration file NICalibrate.csv
#        calibration_filename = "NISignalExpressCalibrate.csv"
#        temp_filename = "temp.csv"
#        sensor = str(sensor_id)
#        with open(temp_filename, "wb") as temp_file:
#            with open(calibration_filename, "r") as calibration_file:
#                for row in csv.reader(calibration_file):
#                    if sensor not in row:
#                        csv.writer(temp_file).writerow(row)

#        os.remove(calibration_filename)
#        os.rename(temp_filename, calibration_filename)


    def __calibrate_value(self, sensor_id, value):
        """
            This function calibrates the value of the senor_id.
        """
        # Open the calibration file
        # Check if the sensor_id of the calibration file
        # to determine the multipliers and offsets
        # Return the value with calibration
        calibration_filename = "NISignalExpressCalibrate.csv"
        calibration_file = open(calibration_filename, "r")
        reader = csv.reader(calibration_file)

        value = float(value)

        premultiplier = 1.0
        preoffset = 0.0
        multiplier = 1.0
        offset = 0.0
        row = next(reader)
        for row in reader:
            if row[0] == str(sensor_id):
                premultiplier = float(row[1])
                preoffset = float(row[2])
                multiplier = float(row[3])
                offset = float(row[4])
        value = multiplier * ((premultiplier * value) + preoffset) + offset

        calibration_file.close()
        return value

    def clean_folder(self, folder_location):
        """
            This function deletes all the output files created.
        """
        folder_files_list = os.listdir(folder_location)

        for folder_files in folder_files_list:
            if ".py" not in folder_files:
                try:
                    os.remove(os.path.join(folder_location, folder_files))
                except:
                    pass

    def calibrate_output(self):
        """
            This function calibrates the output for given callibrations.
        """
        # Find the correct input file
        # Create a output file for the calibrated values
        # Write the header row
        # Go through each input row and callibrate the value of the row
        # Write the callibrated row to the output file

        input_file = (open(os.path.join(self._reshaped_location,\
            self._reshaped_filename), "r"))
        reader = csv.reader(input_file)

        output_filename = str(self._reshaped_filename).replace(".csv",\
            "_calibrated.csv")
        output_file = (open(os.path.join(self._calibrated_location,\
            output_filename), "w"))
        writer = csv.writer(output_file)
        new_row = next(reader)
        new_row.append('comments')
        writer.writerow(new_row)

        for row in reader:
            #value = self.__calibrate_value(row[1], row[2])
            value = float(row[2])
            try:
                 #May change this if you have a sensor that you want more digits of precision on
                 new_row = [row[0], row[1], round(value,5), notes[row[1]]]
            except Exception as e:
                print("Update the notes dictionary located in this file. Entries present in TDMS file do not correnspond to a channel-value pairing.") 
            writer.writerow(new_row)

        input_file.close()
        output_file.close()
