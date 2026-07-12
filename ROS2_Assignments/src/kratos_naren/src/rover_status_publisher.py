#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String, Bool

class RoverStatusPublisher(Node):
    def __init__(self):
        super().__init__('rover_status_publisher')
        
        # Define the three required publishers 
        self.battery_pub = self.create_publisher(Float32, '/battery_level', 10)
        self.mode_pub = self.create_publisher(String, '/rover_mode', 10)
        self.estop_pub = self.create_publisher(Bool, '/emergency_stop', 10)
        
        # Timer to publish data every 1 second (1 Hz)
        self.timer = self.create_timer(1.0, self.publish_status)

    def publish_status(self):
        # 1. Battery Level 
        battery_msg = Float32()
        battery_msg.data = 88.4
        self.battery_pub.publish(battery_msg)
        
        # 2. Rover Mode 
        mode_msg = String()
        mode_msg.data = "MANUAL"
        self.mode_pub.publish(mode_msg)
        
        # 3. Emergency Stop Status 
        estop_msg = Bool()
        estop_msg.data = False
        self.estop_pub.publish(estop_msg)
        
        self.get_logger().info('Published Status: Battery=88.4%, Mode=MANUAL, E-Stop=False')

def main(args=None):
    rclpy.init(args=args)
    node = RoverStatusPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()