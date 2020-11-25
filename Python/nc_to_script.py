import math
from scipy.spatial.transform import Rotation as R

out_file = None

def axis_angle(rz1, rx, rz2):
		 
    r = R.from_euler('ZYZ', [rz1, rx, rz2], degrees=True)
    r2 = R.from_euler('X', 180, degrees=True)
    r3 = r*r2
    rv = r.as_rotvec()
    return rv
 
def new_file(filename):
    global out_file
    if out_file != None:
        out_file.close()
        
    out_file = open(filename + ".script", 'w')
    
    out_file.write("accel=0.5\n")
    out_file.write("vel=0.04\n")
    out_file.write("round=0.001\n\n")
    
def ur_script(filename):
    global out_file
    
    print("Working on " + filename)
    path_num = 0
    in_file = open(filename + ".path", 'r')
    points = 0
    for line in in_file:
        if "StartHeader" in line:
            path_num = path_num + 1
            new_file(filename + "_" + path_num)
        data = line.split(",")
        if len(data) == 7:
            out_file.write("movel(pose_trans(Pumpkin,p[")
            out_file.write(str("%1.5f" % (float(data[1])/(25.4*1000.0))) + "," + str("%1.5f" % (float(data[2])/(25.4*1000.0))) + "," + str("%1.5f" % (float(data[3])/(25.4*1000.0))) + ",")
            angles = axis_angle(float(data[4]),float(data[5]),float(-data[4]))
            out_file.write(str("%1.5f" % angles[0]) + "," + str("%1.5f" % angles[1]) + "," + str("%1.5f" % angles[2]))
            out_file.write("]), a=accel, v=vel, t=0, r=round)\n")
            points = points + 1
            
    in_file.close()
    out_file.close()
    print("Done")
    print("Processed " + str(points) + " points")
    
ur_script("ch3")
ur_script("mm3")