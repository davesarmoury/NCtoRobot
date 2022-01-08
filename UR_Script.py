from NC2Robot import NC2Robot

class UR_Script(NC2Robot):
    def __init__(self, config_name="config/ur_example_config.yaml"):
        super().__init__(config_name)

    def writeHeader(self, out_file, config):
        out_file.write("accel=" + self.controller_config.accel + "\n")
        out_file.write("vel=" + self.controller_config.l_speed + "\n")
        out_file.write("round=" + self.controller_config.rounding + "\n")
        out_file.write("f_name=" + self.controller_config.feature + "\n\n")

    def writeLinear(self, out_file, data):
        out_file.write("movel(pose_trans(f_name,p[")
        out_file.write(str("%1.5f" % (float(data[1])*0.875/1000.0)) + "," + str("%1.5f" % (float(data[2])*0.875/1000.0)) + "," + str("%1.5f" % (float(data[3])*0.875/1000.0)) + ",")
        angles = self.axis_angle(float(data[4]),float(data[5]),-float(data[4]))
        out_file.write(str("%1.5f" % angles[0]) + "," + str("%1.5f" % angles[1]) + "," + str("%1.5f" % angles[2]))
        out_file.write("]), a=accel, v=vel, t=0, r=round)\n")

    def writeJoint(self, out_file, data):
        out_file.write("movej(get_inverse_kin(pose_trans(f_name,p[")
        out_file.write(str("%1.5f" % (float(data[1])*0.875/1000.0)) + "," + str("%1.5f" % (float(data[2])*0.875/1000.0)) + "," + str("%1.5f" % (float(data[3])*0.875/1000.0)) + ",")
        angles = self.axis_angle(float(data[4]),float(data[5]),-float(data[4]))
        out_file.write(str("%1.5f" % angles[0]) + "," + str("%1.5f" % angles[1]) + "," + str("%1.5f" % angles[2]))
        out_file.write("])), a=accel, v=vel, t=0, r=round)\n")
