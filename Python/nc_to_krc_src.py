import math
from scipy.spatial.transform import Rotation as R

out_file = None

def cartesian(xin, yin, zin):
	scale = 1.0
	return [xin / scale, yin / scale, zin / scale]

def rotation_angles(rz1, rx, rz2):
	r = R.from_euler('ZYZ', [rz1, rx, rz2], degrees=True)
	r2 = R.from_euler('X', 180, degrees=True)
	r3 = r*r2
	eul = r.as_euler('ZYX', degrees=True)
	return eul

def new_file(filename):
	global out_file
	if out_file != None:
		out_file.write("PTP {A1 20.0,A2 -100.0,A3 140.0,A4 0.0,A5 -40.0,A6 0.0} \n\n")
		out_file.write("\nEND\n")
		out_file.close()

	if filename:
		print("Opening " + filename + ".src")
		out_file = open(filename + ".src", 'w')

		out_file.write("&ACCESS RVP\n")
		out_file.write("&REL 1\n")
		out_file.write("&PARAM TEMPLATE = C:\\KRC\Roboter\\Template\\vorgabe\n")
		out_file.write("&PARAM EDITMASK = *\n")

		out_file.write("DEF " + filename + "( )\n")

		out_file.write("EXT BAS (BAS_COMMAND :IN,REAL :IN )\n\n")

		out_file.write("INT INDX\n")
		out_file.write("FOR INDX=1 TO 6\n")
		out_file.write("	$ACC_AXIS[INDX]=50\n")
		out_file.write("ENDFOR\n\n")

		out_file.write("$VEL.ORI1=200\n")
		out_file.write("$VEL.ORI2=200\n")
		out_file.write("$ACC.ORI1=100\n")
		out_file.write("$ACC.ORI2=100\n\n")

		out_file.write("FOR INDX=1 TO 6\n")
		out_file.write("	$VEL_AXIS[INDX]=20\n")
		out_file.write("ENDFOR\n")
		out_file.write("$VEL.CP = 0.1\n\n")

		#out_file.write("$IPO_MODE = #BASE\n"); # NORMAL
		out_file.write("$IPO_MODE = #TCP\n"); # RTCP
		out_file.write("$APO.CDIS = 0.5\n")
		out_file.write("$ADVANCE = 5\n\n")

		out_file.write("$ACT_TOOL = 1\n")
		out_file.write("$TOOL=TOOL_DATA[1]\n")
		out_file.write("$ACT_BASE = 1\n")
		out_file.write("$BASE=BASE_DATA[1]\n\n")

		out_file.write("DECL EKI_STATUS RET\n")
		out_file.write("RET=EKI_Init(\"oxy\")\n")
		out_file.write("RET=EKI_Open(\"oxy\")\n\n")

		out_file.write("PTP {A1 20.0,A2 -100.0,A3 140.0,A4 0.0,A5 -40.0,A6 0.0} \n\n")

def krc_src(filename):
	global out_file

	print("Working on " + filename)
	path_num = 0
	in_file = open(filename + ".path", 'r')
	points = 0
	last_move = "XX"
	for line in in_file:
		if "StartHeader" in line:
			path_num = path_num + 1
			new_file(filename + "_" + str(path_num))
		data = line.split(",")
		if len(data) == 7:
			angles = rotation_angles(float(data[4]),float(data[5]),0.0)
			positions = cartesian(float(data[1]),float(data[2]),float(data[3]))

			if data[0] == "0":
				if last_move == "1":
					out_file.write("RET=EKI_SetBool(\"oxy\",\"torchState\",FALSE)\n")
					out_file.write("RET = EKI_Send(\"oxy\",\"torchState\")\n")
				out_file.write("PTP {X " + str("%1.3f" % positions[0]) + ",Y " + str("%1.3f" % positions[1]) + ",Z " + str("%1.3f" % positions[2]) + ",A " + str("%1.3f" % angles[0]) + ",B " + str("%1.3f" % angles[1]) + ",C " + str("%1.3f" % angles[2]) + "}\n")
			else:
				if last_move == "0":
					out_file.write("WAIT SEC 2\n")
					out_file.write("RET=EKI_SetBool(\"oxy\",\"torchState\",TRUE)\n")
					out_file.write("RET = EKI_Send(\"oxy\",\"torchState\")\n")
				out_file.write("LIN {X " + str("%1.3f" % positions[0]) + ",Y " + str("%1.3f" % positions[1]) + ",Z " + str("%1.3f" % positions[2]) + ",A " + str("%1.3f" % angles[0]) + ",B " + str("%1.3f" % angles[1]) + ",C " + str("%1.3f" % angles[2]) + "} C_DIS\n")

			last_move = data[0]
			points = points + 1

	in_file.close()
	new_file(None)
	print("Done")
	print("Processed " + str(points) + " points")

krc_src("firepit")
