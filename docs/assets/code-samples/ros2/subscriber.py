#!/usr/bin/env python3

"""
ROS 2 Subscriber Example for Robot Control

This script demonstrates a basic subscriber that receives robot sensor data
and status messages. It's designed to work with the ROS 2 ecosystem.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class RobotSensorSubscriber(Node):
    """
    A ROS 2 subscriber node that receives robot sensor data and status messages.
    """

    def __init__(self):
        super().__init__('robot_sensor_subscriber')

        # Create subscription for robot status messages
        self.status_subscription = self.create_subscription(
            String,
            '/robot_status',
            self.status_callback,
            10
        )

        # Create subscription for laser scan data
        self.laser_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_callback,
            10
        )

        # Create subscription for velocity commands
        self.cmd_vel_subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        self.get_logger().info('Robot Sensor Subscriber initialized')

    def status_callback(self, msg):
        """Callback function for robot status messages."""
        self.get_logger().info(f'Received status: {msg.data}')

    def laser_callback(self, msg):
        """Callback function for laser scan data."""
        # Get the minimum distance from the laser scan
        if msg.ranges:
            min_distance = min(msg.ranges)
            if min_distance < 1.0:  # Less than 1 meter
                self.get_logger().warn(f'Obstacle detected! Distance: {min_distance:.2f}m')

    def cmd_vel_callback(self, msg):
        """Callback function for velocity commands."""
        self.get_logger().info(
            f'Received velocity command - Linear: {msg.linear.x:.2f}, '
            f'Angular: {msg.angular.z:.2f}'
        )


def main(args=None):
    """
    Main function to initialize and run the ROS 2 subscriber node.
    """
    rclpy.init(args=args)

    robot_subscriber = RobotSensorSubscriber()

    try:
        rclpy.spin(robot_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        robot_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()