#!/usr/bin/env python3
from math import *
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray

class DoubleAckermannController(Node):
    def __init__(self):
        super().__init__('double_ackermann_controller')
        
        # Subscribe to teleop/joystick commands
        self.cmd_sub = self.create_subscription(
            Twist, 
            '/cmd_vel', 
            self.cmd_callback, 
            10
        )
        
        # Publisher for the 4 steering hinges (Position in Radians)
        # Order matches YAML: [fl_steer, fr_steer, rl_steer, rr_steer]
        self.steer_pub = self.create_publisher(
            Float64MultiArray, 
            '/steering_controller/commands', 
            10
        )

        # Publisher for the 4 wheel axles (Velocity in Rad/s)
        # Order matches YAML: [fl_drive, fr_drive, rl_drive, rr_drive]
        self.drive_pub = self.create_publisher(
            Float64MultiArray, 
            '/drive_controller/commands', 
            10
        )

        # Rover Physical Constants
        self.wheelbase = 0.5
        self.track_width = 0.3
        self.wheel_radius = 0.12

        self.get_logger().info("Double Ackermann Controller Node Started. Waiting for /cmd_vel...")

    def cmd_callback(self, msg):
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        
        # =======================================================
        # APPLICANT TASK: Implement Double Ackermann Kinematics 
        # Calculate the 4 steering angles and 4 wheel velocities
        # =======================================================
        
        # 1. Calculate angles (radians)
        fl_angle, fr_angle, rl_angle, rr_angle = 0.0, 0.0, 0.0, 0.0
        
        if abs(angular_z) < 1e-5:
            fl_angle, fr_angle, rl_angle, rr_angle = 0.0, 0.0, 0.0, 0.0
            
            base_vel = linear_x / self.wheel_radius
            fl_vel, fr_vel, rl_vel, rr_vel = base_vel, base_vel, base_vel, base_vel

        elif abs(linear_x) < 1e-5:
            # Calculate the exact X-shape angle to point to the chassis center point
            spot_angle = atan2(self.wheelbase / 2.0, self.track_width / 2.0)
            
            # Form the 'X' shape orientation based on the turning direction
            sign_dir = 1.0 #if angular_z > 0 else -1.0
            fl_angle = -spot_angle * sign_dir
            fr_angle = spot_angle * sign_dir
            rl_angle = spot_angle * sign_dir
            rr_angle = -spot_angle * sign_dir
            
            # Turning speed is proportional to the distance from center to wheel hub
            r_center = sqrt((self.track_width / 2.0)**2 + (self.wheelbase / 2.0)**2)
            spin_vel = (angular_z * r_center) / self.wheel_radius
            
            # Symmetrical spin allocation (Left wheels pull back, right wheels push forward)
            fl_vel, rl_vel = -spin_vel, -spin_vel
            fr_vel, rr_vel = spin_vel, spin_vel

        else:   
            R=linear_x/angular_z
            R_abs=abs(R)
            sign_dir = 1.0 if angular_z > 0 else -1.0
            
            fl_angle = atan2(self.wheelbase / 2.0, R_abs - (self.track_width / 2.0)) * sign_dir
            fr_angle = atan2(self.wheelbase / 2.0, R_abs + (self.track_width / 2.0)) * sign_dir
            rl_angle = -atan2(self.wheelbase / 2.0, R_abs - (self.track_width / 2.0)) * sign_dir
            rr_angle = -atan2(self.wheelbase / 2.0, R_abs + (self.track_width / 2.0)) * sign_dir

            # 2. Calculate velocities (rad/s)
            fl_vel, fr_vel, rl_vel, rr_vel = 0.0, 0.0, 0.0, 0.0
            
            
            if angular_z > 0:  # Turning Left
                r_fl = sqrt((R_abs - self.track_width / 2.0)**2 + (self.wheelbase / 2.0)**2)
                r_rl = r_fl
                r_fr = sqrt((R + self.track_width / 2.0)**2 + (self.wheelbase / 2.0)**2)
                r_rr = r_fr
            else:              # Turning Right:
                r_fr = sqrt((R_abs - self.track_width / 2.0)**2 + (self.wheelbase / 2.0)**2)
                r_rr = r_fr
                r_fl = sqrt((R_abs + self.track_width / 2.0)**2 + (self.wheelbase / 2.0)**2)
                r_rl = r_fl

            fl_vel = linear_x * (r_fl / R_abs) / self.wheel_radius
            fr_vel = linear_x * (r_fr / R_abs) / self.wheel_radius
            rl_vel = linear_x * (r_rl / R_abs) / self.wheel_radius
            rr_vel = linear_x * (r_rr / R_abs) / self.wheel_radius
        # =======================================================
        
        # Publish Steering Commands
        steer_msg = Float64MultiArray()
        steer_msg.data = [fl_angle, fr_angle, rl_angle, rr_angle]
        self.steer_pub.publish(steer_msg)

        # Publish Drive Commands
        drive_msg = Float64MultiArray()
        drive_msg.data = [fl_vel, fr_vel, rl_vel, rr_vel]
        self.drive_pub.publish(drive_msg)

def main(args=None):
    rclpy.init(args=args)
    node = DoubleAckermannController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
