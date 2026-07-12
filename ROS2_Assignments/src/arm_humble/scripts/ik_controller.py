#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import threading

class IKController(Node):
    def __init__(self):
        super().__init__('ik_controller')
        
        # Publisher to handle joint movement
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
        
        # Link lengths matching standard 3D configurations
        self.L1 = 2.0  # Length of upper_arm_link
        self.L2 = 1.5  # Length of forearm_link to wrist_output_shaft_link
        
        # Initial position placed at the coords given in the assignment as example
        self.current_x = 2.10
        self.current_y = 0.75
        self.current_z = 0.00
        
        # Calculate initial joint positions matching initial cartesian coordinates
        ik_sol = self.calculate_ik(self.current_x, self.current_y, self.current_z)
        if ik_sol:
            self.base_yaw, self.shoulder, self.elbow = ik_sol
        else:
            self.base_yaw, self.shoulder, self.elbow = 0.0, 0.0, 0.0
            
        # ALL joint names explicitly matching the URDF model configurations
        self.joint_names = [
            'base_yaw_joint', 
            'shoulder_joint', 
            'elbow_joint',
            'wrist_pitch_joint',
            'wrist_roll_joint',
            'gripper_joint'
        ]
        
        # Continuous state broadcasting timer loop running at 10Hz
        self.timer = self.create_timer(0.1, self.publish_joint_states)
        self.get_logger().info("IK Controller Node successfully initialized.")

    def calculate_ik(self, x, y, z):
        """Solves 3D analytical Inverse Kinematics decoupled into base yaw and a 2D vertical plane."""
        
        try:
            # 1. Base Yaw Calculation
            base_yaw = math.atan2(y, x)
            
            # 2. PDIstance 
            r = math.sqrt(x**2 + y**2)
            
            # 3. Cosine Law
            cos_elbow = (r**2 + z**2 - self.L1**2 - self.L2**2) / (2.0 * self.L1 * self.L2)
            
            # Boundary check
            if not (-1.0 <= cos_elbow <= 1.0):
                return None
                
            elbow = math.acos(cos_elbow)
            
            # Shoulder adjustment angle calculation
            shoulder = math.atan2(z, r) - math.atan2(self.L2 * math.sin(elbow), self.L1 + self.L2 * math.cos(elbow))
            
            return base_yaw, shoulder, elbow
        except (ValueError, ZeroDivisionError):
            return None

    def publish_joint_states(self):
        """Publishes the tracked positions continuously to stop RViz flickering."""
        '''Isnt stopping the flicker :('''
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        # Provide calculated variables for controlled joints, and constant 0.0 for the remaining passive wrist/gripper joints
        msg.position = [self.base_yaw, self.shoulder, self.elbow, 0.0, 0.0, 0.0]
        self.joint_pub.publish(msg)

    def process_movement(self, axis, displacement):
        """Computes incremental target changes and enforces constraints."""
        
        target_x = self.current_x
        target_y = self.current_y
        target_z = self.current_z
        
        if axis == 'x':
            target_x += displacement
        elif axis == 'y':
            target_y += displacement
        elif axis == 'z':
            target_z += displacement

        # Run calculations on the coordinates
        ik_sol = self.calculate_ik(target_x, target_y, target_z)
        
        if ik_sol is not None:

            self.base_yaw, self.shoulder, self.elbow = ik_sol
            self.current_x = target_x
            self.current_y = target_y
            self.current_z = target_z
            print(f"Success! Position updated -> X: {self.current_x:.2f}, Y: {self.current_y:.2f}, Z: {self.current_z:.2f}")
        else:
            #Retain previous placement data
            print(f"[OUT OF WORKSPACE] Targeted coordinate ({target_x:.2f}, {target_y:.2f}, {target_z:.2f}) is unreachable! Action aborted.")

def non_blocking_user_input(node):
    """Monitors the CLI terminal sequence without freezing the ROS 2 background thread loop."""
   
    while rclpy.ok():
        print(f"\nCurrent Position: x={node.current_x:.2f} y={node.current_y:.2f} z={node.current_z:.2f}")
        try:
            axis = input("Enter axis to move (x/y/z): ").strip().lower()
            if axis not in ['x', 'y', 'z']:
                print("Invalid input. Select x, y, or z.")
                continue
                
            disp_str = input("Enter displacement (meters): ").strip()
            displacement = float(disp_str)
            
            node.process_movement(axis, displacement)
        except ValueError:
            print("Invalid numeric argument. Please try again.")
        except (KeyboardInterrupt, EOFError):
            break

def main(args=None):
    rclpy.init(args=args)
    node = IKController()
    
    input_thread = threading.Thread(target=non_blocking_user_input, args=(node,), daemon=True)
    input_thread.start()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()