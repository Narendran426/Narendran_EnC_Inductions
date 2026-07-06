import rclpy
from rclpy.node import Node
from kratos_naren_msgs.msg import RoverStatus

class RoverCustomSubscriber(Node):
    def __init__(self):
        super().__init__('rover_custom_subscriber')
        
        # Subscribe to the exact same topic and data format structure
        self.subscription = self.create_subscription(
            RoverStatus,
            '/rover_status',
            self.listener_callback,
            10
        )
        self.get_logger().info('Q2 Custom RoverStatus Subscriber has started.')

    def listener_callback(self, msg):
        #print all 4 telemetry fields received
        self.get_logger().info('======== RECEIVING UNIFIED ROVER STATUS ========')
        self.get_logger().info(f'🔋 Battery Level: {msg.battery_percentage:.1f}%')
        self.get_logger().info(f'🏎️ Current Speed: {msg.velocity} m/s')
        self.get_logger().info(f'🚨 Emergency Stop Active: {msg.emergency_stop}')
        self.get_logger().info(f'⚙️ Operational Mode: {msg.mode}')

def main(args=None):
    rclpy.init(args=args)
    node = RoverCustomSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()