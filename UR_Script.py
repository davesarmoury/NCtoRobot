import math
from scipy.spatial.transform import Rotation as R

class UR_Script(NC2Robot):
    def __init__(self, script_name, source_name, config_name=None):
        super().__init__(script_name, source_name, config_name)

    def write_header(self, out_file, config):
        out_file.write("accel=0.5\n")
        out_file.write("vel=0.04\n")
        out_file.write("round=0.001\n")
        out_file.write("f_name=Square\n\n")

    def write(filename):
        global out_file

        print("Working on " + filename)
        path_num = 0
        in_file = open(filename + ".path", 'r')
        points = 0
        for line in in_file:
            if "StartHeader" in line:
                path_num = path_num + 1
                new_file(filename + "_" + str(path_num))
            data = line.split(",")
            if len(data) == 7:
                out_file.write("movel(pose_trans(f_name,p[")
                out_file.write(str("%1.5f" % (float(data[1])*0.875/1000.0)) + "," + str("%1.5f" % (float(data[2])*0.875/1000.0)) + "," + str("%1.5f" % (float(data[3])*0.875/1000.0)) + ",")
                angles = axis_angle(float(data[4]),float(data[5]),-float(data[4]))
                out_file.write(str("%1.5f" % angles[0]) + "," + str("%1.5f" % angles[1]) + "," + str("%1.5f" % angles[2]))
                out_file.write("]), a=accel, v=vel, t=0, r=round)\n")
                points = points + 1

        in_file.close()
        out_file.close()
        print("Done")
        print("Processed " + str(points) + " points")
