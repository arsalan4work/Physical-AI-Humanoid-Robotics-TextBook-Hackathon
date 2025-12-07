#!/usr/bin/env python3

"""
ROS 2 Publisher Example for Robot Control

This script demonstrates a basic publisher that sends robot commands.
It's designed to work with the ROS 2 ecosystem for robotics applications.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class RobotCommandPublisher(Node):
    """
    A ROS 2 publisher node that sends robot movement commands.
    """

    def __init__(self):
        super().__init__('robot_command_publisher')

        # Create publisher for robot velocity commands
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # Create publisher for status messages
        self.status_publisher = self.create_publisher(String, '/robot_status', 10)

        # Timer to send messages periodically
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Counter for messages
        self.i = 0

        self.get_logger().info('Robot Command Publisher initialized')

    def timer_callback(self):
        """Callback function that publishes messages periodically."""
        # Create a Twist message for robot movement
        msg = Twist()
        msg.linear.x = 1.0  # Move forward at 1.0 m/s
        msg.angular.z = 0.5  # Rotate at 0.5 rad/s

        # Publish the movement command
        self.cmd_vel_publisher.publish(msg)

        # Create and publish a status message
        status_msg = String()
        status_msg.data = f'Robot command published: {self.i}'
        self.status_publisher.publish(status_msg)

        self.get_logger().info(f'Publishing: linear.x={msg.linear.x}, angular.z={msg.angular.z}')
        self.i += 1


def main(args=None):
    """
    Main function to initialize and run the ROS 2 publisher node.
    """
    rclpy.init(args=args)

    robot_publisher = RobotCommandPublisher()

    try:
        rclpy.spin(robot_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        robot_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()