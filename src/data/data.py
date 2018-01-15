import sys
import os
import pickle

from matplotlib import pyplot as plt
import numpy as np
import csv
import pdb
#import settings

class Data():

    def __init__(self, name, path=None):
        """
        Initialize Data object.

        Parameters
        -----------------------------------
        name : String
            Name of data object. Used to as the filename when saving the data.
        path : String
            Path of desired directory where the data should be saved.
        """
        self.name = name
        self.file_name = str(self.name) + '.csv'
        self.metadata = None
        self.start_frame = None
        self.torsion = None

        # If save path is not specified, set it to the current directory
        if path is not None:
            self.path = os.path.abspath(path)
        else:
            self.path = os.path.curdir

    def set(self, torsion, start_frame=0, metadata=None, frame_index_list=None):
        """
        Populate data fields with values.

        Parameters
        -------------------------------------
        torsion : list
            List of ocular torsion values.
        start_frame : int
            Video frame index corresponding to the start point of torsion analysis.
        metadata : dict
            Any video/torsion metadata the user wishes to store.
        frame_index_list : list
            List of same length as torsion. Maps torsion values to corresponding video frame indeces.
            Specified when the video frames analyzed are not just subsequent frames.
        """
        self.metadata = metadata
        self.start_frame = start_frame
        self.torsion = torsion
        self.frame_index_list = frame_index_list

    def save(self):
        """
        Save data at data object path.

        Parameters
        -------------------------------------
        file_name : String
            Desired save file name.
            e.g. "saved_data1"

        path : String
            Optional parameter specifying a save location.

        mode : String
            Optional parameter specifiying the desired type of save file.
            'csv' - Save data as a csv file.
            'pickle' - save data as a pickled python object.
        """
        # Check to make sure file_name is string.
        if not isinstance(self.file_name, str):
            # TODO throw exception
            print('Please enter a valid file name string.')
            return None

        # Check to make sure path is valid
        # TODO use os.path.isfile to check file path
        if os.path.isdir(self.path):
            save_loc = self.path
        else:
            print(self.path)
            save_loc = os.path.abspath(settings.SAVE_PATH)

        save_str = os.path.join(save_loc, self.file_name)

        with open(save_str, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            # save metadata first
            csvwriter.writerow(['METADATA'])

            if self.metadata:
                for k, v in self.metadata.items():
                    csvwriter.writerow([k, v])

                # optional fps to calculate video time
                fps = self.metadata.get('VIDEO_FPS', None)

            csvwriter.writerow(['TORSION RESULTS'])
            csvwriter.writerow(['Frame Index', 'Frame Time', 'Torsion [deg]'])

            # default time is empty string
            time = ''

            # save to csv
            for i, deg in enumerate(self.torsion):
                if self.frame_index_list is None:
                    if fps:
                        time = 1/fps * (self.start_frame + i)
                    csvwriter.writerow([self.start_frame + i, time, repr(deg)])
                else:
                    if fps:
                        time = 1/fps * self.frame_index_list[i]
                    csvwriter.writerow([self.frame_index_list[i], time, repr(deg)])

    def load(self):
        """
        Load data saved in .csv file saved at path specified in self.path.
        """
        torsion = []
        start_frame = 0
        metadata = {}

        file_path = os.path.abspath(os.path.join(self.path, self.file_name))

        if os.path.isfile(file_path):
            with open(file_path, newline='') as f:
                line = next(f)

                metadata_flag = False
                if 'metadata' in line.lower():
                    metadata_flag = True

                i = 0

                for line in f:

                    if 'torsion' in line.lower():
                        metadata_flag = False
                        continue

                    line = line.replace('\n','').split(',')

                    if metadata_flag:
                        metadata[line[0]] = line[1]
                    else:
                        if i == 0:
                            start_frame = int(line[0])

                        torsion.append(float(line[2]))

                        i += 1

            # set object from file
            self.set(torsion, start_frame, metadata)

def load(file_str):
    """
    Load data from file into data object.
    Overwrites any currently existing data in that object.

    Parameters
    -------------------------------------
    file_str : String
        String pointing to file name to be loaded.
        e.g. "saved_data1"

    Returns
    -------------------------------------
    data : Data object
        Data object stored in file being loaded
    """

    # Check to make sure the string entered is valid
    if os.path.exists(file_str) and (file_str[-4:] == '.csv' or file_str[-4:] == '.pkl'):

        # If the file is a csv
        if file_str[-4:] == '.csv':
            # Initialize data object
            d = Data()
            d.frame_time = {}
            d.torsion = {}
            num_non_data_rows = 1

            with open(file_str, newline='') as csvfile:
                # Calculate how much data is being loaded
                row_count = sum(1 for row in csvfile)
                num_data_elements = row_count - num_non_data_rows
                d.frame_index_list = np.zeros(num_data_elements)

            with open(file_str, newline='') as csvfile:
                # Read the data
                csvreader = csv.reader(csvfile, delimiter=',')
                for idx, row in enumerate(csvreader):
                    if not idx==0:
                        frame_idx = int(row[0])
                        d.frame_index_list[idx-num_non_data_rows] = frame_idx
                        d.frame_time[frame_idx] = 2
                        d.frame_time[frame_idx] = float(row[1])
                        d.torsion[frame_idx] = float(row[2])

            return d

        # If the file is a pickled python object
        elif file_str[-4:] == '.pkl':
            print(os.path.abspath(file_str))
            return pickle.load( open( file_str, "rb" ) )
    else:
        print('Please enter a valid file path string.')
