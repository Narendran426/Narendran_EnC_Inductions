#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

# Import your custom compiled message type from your package
from kratos_naren_msgs.msg import RoverStatus

class RoverCustomPublisher(Node):
    def __init__(self):
        super().__init__('rover_custom_publisher')
        
        # Create a publisher on the single unified topic named '/rover_status'
        self.publisher_ = self.create_publisher(RoverStatus, '/rover_status', 10)
        
        # 2 Hz frequency calculation: 1 second / 2 = 0.5 seconds timer interval
        self.timer_period = 0.5  
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        # Initial dummy values
        self.battery = 100.0
        self.velocity = 0.0
        self.e_stop = False
        self.mode = "AUTONOMOUS"
        
        self.get_logger().info('Q2 Custom RoverStatus Publisher has started at 2 Hz.')

    def timer_callback(self):
        # 1. Instantiate a blank message object of your custom structure
        msg = RoverStatus()
        
        # 2. Simulate fluctuating data points to watch the numbers change live
        if self.battery > 10.0:
            self.battery -= 0.2  # Slowly discharge battery
        self.velocity = round(1.2 + (self.battery % 0.5), 2)  # Vary speed slightly
        
        # 3. Populate all 4 specific fields defined in your custom RoverStatus.msg
        msg.battery_percentage = float(self.battery)
        msg.velocity = float(self.velocity)
        msg.emergency_stop = bool(self.e_stop)
        msg.mode = str(self.mode)
        
        # 4. Ship the entire message structure
        self.publisher_.publish(msg)
        
        self.get_logger().info(
            f'📦 Sent Snapshot -> Battery: {msg.battery_percentage:.1f}%, '
            f'Speed: {msg.velocity}m/s, E-Stop: {msg.emergency_stop}, Mode: {msg.mode}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = RoverCustomPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()