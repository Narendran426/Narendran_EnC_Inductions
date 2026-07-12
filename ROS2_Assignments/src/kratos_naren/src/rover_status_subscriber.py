#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String, Bool

class RoverStatusSubscriber(Node):
    def __init__(self):
        super().__init__('rover_status_subscriber')
        
        # Subscribe to all three required topics [cite: 104, 105]
        self.battery_sub = self.create_subscription(
            Float32, '/battery_level', self.battery_callback, 10)
            
        self.mode_sub = self.create_subscription(
            String, '/rover_mode', self.mode_callback, 10)
            
        self.estop_sub = self.create_subscription(
            Bool, '/emergency_stop', self.estop_callback, 10)

    def battery_callback(self, msg):
        self.get_logger().info(f'Received Battery Level: {msg.data}%')

    def mode_callback(self, msg):
        self.get_logger().info(f'Received Rover Mode: {msg.data}')

    def estop_callback(self, msg):
        status = "TRUE" if msg.data else "FALSE"
        self.get_logger().info(f'Received Emergency Stop: {status}')

def main(args=None):
    rclpy.init(args=args)
    node = RoverStatusSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()