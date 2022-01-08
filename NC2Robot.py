import math
from scipy.spatial.transform import Rotation as R
from tqdm import tqdm
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class NC2Robot:
    def __init__(self, config_name=None):
        self.config_name = config_name
        self.controller_config = {}

        if self.config_name.any():
            inFile = open(self.config_name, 'r')
            self.controller_config = load(inFile, Loader=Loader)
            inFile.close()

    def writeScript(self, filename, data):
        out_file = open(filename, 'w')
        current_tool = -1
        current_path = -1

        print("Writing " + filename)
        self.writeHeader(out_file)

        for idx in tqdm(range(len(data)):
            point = data[i]
            if point[8] != current_path:
                current_path = point[8]
                self.writePathInit(out_file, point)
            if point[7] != current_tool:
                current_tool = point[7]
                self.writeToolInit(out_file, point)

            if point[0] == 1 or self.controller_config.linearize:
                self.writeLinear(out_file, point)
            else:
                self.writeJoint(out_file, point)

        self.writeFooter(out_file)

    def writeLinear(self, out_file, data):
        '''
        Writes a linear motion

        Args:
            out_file (file): file object to write to
            data (list): point data
        '''
        pass

    def writeJoint(self, out_file, data):
        '''
        Writes a joint motion

        Args:
            out_file (file): file object to write to
            data (list): point data
        '''
        pass

    def writeToolInit(self, out_file, data):
        '''
        Writes anything needed to transition to a new tool

        Args:
            out_file (file): file object to write to
            data (list): point data
        '''
        pass

    def writePathInit(self, out_file, data):
        '''
        Writes anything needed to transition to a new path

        Args:
            out_file (file): file object to write to
            data (list): point data
        '''
        pass

    def writeHeader(self, out_file):
        '''
        Writes any initial header information to the robot script

        Args:
            out_file (file): file object to write to
        '''
        pass

    def writeFooter(self, out_file):
        '''
        Writes any final footer information to the robot script

        Args:
            out_file (file): file object to write to
        '''
        pass

    def loadSource(self, source):
        '''
        Loads the source script.  Converts all values to usable data.  Each line of the source file must have the format:
        Motion Type,X,Y,Z,rZ,rY,Speed,Tool,Path

        Motion Type 0 - PTP, 1 - LIN
        X in mm
        Y in mm
        Z in mm
        rZ in degrees
        rY in degrees (new y)
        Travel speed in mm/s
        Tool Number
        Path Number

        Args:
            source (string): Path to source file

        Returns:
            list: A list of all parsed points.  Each point is a list of its data
        '''

        parsed_data = []
        print("Parsing " + source)
        try:
            inFile = open(source, 'r')
            lines = inFile.readlines()
            inFile.close()

            for idx in tqdm(range(len(lines)):
                line = line[idx]
                temp = line.split(",")
                current_data = []
                current_data.append(int(temp[0]))   # Motion Type 0 - PTP, 1 - LIN
                current_data.append(float(temp[1])) # X in mm
                current_data.append(float(temp[2])) # Y in mm
                current_data.append(float(temp[3])) # Z in mm
                current_data.append(float(temp[4])) # rZ in degrees
                current_data.append(float(temp[5])) # rY in degrees (new y)
                current_data.append(float(temp[6])) # Travel speed in mm/s
                current_data.append(int(temp[7]))   # Tool Number
                current_data.append(int(temp[8]))   # Path Number
                parsed_data.append(current_data)

            print(str(len(parsed_data)) + " lines read")
            return parsed_data
        except Exception as e:
            print(e)
            return None

    def rotation_angles(self, rz1, rx, rz2, degrees=True, flip_vector=False):
        '''
        Takes compound rZ, rY, rZ and returns tuple of compound rotations ZYX.  Used for most robots.

        Args:
            rz1 (float): Rotation angle around local Z
            rx (float): Rotation angle around local X
            rz2 (float): Second rotation angle around local Z
            degrees (bool): Whether the returned angles should be in degrees or radians.  Defaults to True (degrees)
            flip_vector (bool): Whether the tool Z vector should be flipped to point out of the tool.  Defaults to False

        Returns:
            tuple: A tuple of compound rotation angles
        '''
    	r = R.from_euler('ZYZ', [rz1, rx, rz2], degrees=True)
    	if flip_vector:
            r2 = R.from_euler('X', 180, degrees=True)
    	    r = r*r2
    	eul = r.as_euler('ZYX', degrees=True)
    	return eul


    def axisAngle(self, rz1, rx, rz2, flip_vector=False):
        '''
        Takes compound rZ, rY, rZ and returns tuple of axis angle.  Used for UR.  See https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation

        Args:
            rz1 (float): Rotation angle around local Z
            rx (float): Rotation angle around local X
            rz2 (float): Second rotation angle around local Z
            flip_vector (bool): Whether the tool Z vector should be flipped to point out of the tool.  Defaults to False

        Returns:
            tuple: A tuple for axis angle
        '''
        r = R.from_euler('ZYZ', [rz1, rx, rz2], degrees=True)
    	if flip_vector:
            r2 = R.from_euler('X', 180, degrees=True)
    	    r = r*r2
        rv = r.as_rotvec()
        return rv
