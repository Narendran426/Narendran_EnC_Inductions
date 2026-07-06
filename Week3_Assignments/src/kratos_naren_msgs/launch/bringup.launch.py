from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        #QUESTION 1 NODES
        Node(
            package='kratos_naren',               
            executable='rover_status_publisher.py',
            name='rover_status_publisher',
            output='screen'
        ),
        Node(
            package='kratos_naren',               
            executable='rover_status_subscriber.py',
            name='rover_status_subscriber',
            output='screen'
        ),

        #QUESTION 2 NODES
        Node(
            package='kratos_naren_msgs',          
            executable='rover_custom_publisher.py',
            name='rover_custom_publisher',
            output='screen'
        ),
        Node(
            package='kratos_naren_msgs',          
            executable='rover_custom_subscriber.py',
            name='rover_custom_subscriber',
            output='screen'
        ),
    ])