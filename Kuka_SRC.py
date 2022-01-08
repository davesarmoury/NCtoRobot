from NC2Robot import NC2Robot

class KUKA_SRC(NC2Robot):
    def __init__(self, config_name="config/kuka_example_config.yaml"):
        super().__init__(config_name)

    def writeFooter(self, out_file):
		self.writeHome(out_file)
		out_file.write("\nEND\n")

	def writeHeader(self, out_file):
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
		out_file.write("	$VEL_AXIS[INDX]=" + str(self.controller_config.j_speed) + "\n")
		out_file.write("ENDFOR\n")
		out_file.write("$VEL.CP = " + str(self.controller_config.l_speed) + "\n\n")

		#out_file.write("$IPO_MODE = #BASE\n"); # NORMAL
		out_file.write("$IPO_MODE = #TCP\n"); # RTCP
		out_file.write("$APO.CDIS = " + str(self.controller_config.c_dis) + "\n")
		out_file.write("$ADVANCE = 5\n\n")

		out_file.write("$ACT_BASE = " + str(self.controller_config.base) + "\n")
		out_file.write("$BASE=BASE_DATA[" + str(self.controller_config.base) + "]\n\n")

        self.writeHome(out_file)

    def writeHome(self, out_file):
		out_file.write("PTP {A1 " + str(self.controller_config.home[0]))
        out_file.write(",A2 " + str(self.controller_config.home[1]))
        out_file.write(",A3 " + str(self.controller_config.home[2]))
        out_file.write(",A4 " + str(self.controller_config.home[3]))
        out_file.write(",A5 " + str(self.controller_config.home[4]))
        out_file.write(",A6  " + str(self.controller_config.home[5]) + "}\n\n")

    def writeLinear(self, out_file, data):
        angles = self.rotation_angles(float(data[4]),float(data[5]),0.0)
        positions = [float(data[1])/1000.0,float(data[2])/1000.0,float(data[3])/1000.0]
        out_file.write("LIN {X " + str("%1.3f" % positions[0]) + ",Y " + str("%1.3f" % positions[1]) + ",Z " + str("%1.3f" % positions[2]) + ",A " + str("%1.3f" % angles[0]) + ",B " + str("%1.3f" % angles[1]) + ",C " + str("%1.3f" % angles[2]) + "} C_DIS\n")

    def writeJoint(self, out_file, data):
        angles = self.rotation_angles(float(data[4]),float(data[5]),0.0)
        positions = [float(data[1])/1000.0,float(data[2])/1000.0,float(data[3])/1000.0]
        out_file.write("PTP {X " + str("%1.3f" % positions[0]) + ",Y " + str("%1.3f" % positions[1]) + ",Z " + str("%1.3f" % positions[2]) + ",A " + str("%1.3f" % angles[0]) + ",B " + str("%1.3f" % angles[1]) + ",C " + str("%1.3f" % angles[2]) + "}\n")

    def writeToolInit(self, out_file, data):
		out_file.write("\n$ACT_TOOL = " + str(data[7]) + "\n")
		out_file.write("$TOOL=TOOL_DATA[" + str(data[7]) + "]\n\n")
