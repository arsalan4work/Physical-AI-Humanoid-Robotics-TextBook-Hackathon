---
sidebar_position: 3
title: "ROS 2 Expert: Code Samples & Advanced Topics"
description: "Expert-level ROS 2 with functional Python code examples."
---

# ROS 2 Expert: Functional Code Samples and Advanced Topics

This section provides expert-level insights into ROS 2 concepts, focusing on practical implementation with functional Python code samples (using `rclpy`). We'll cover how to create publishers and subscribers, and briefly touch on advanced topics like custom message definitions and launch files.

## Prerequisites

Before running these examples, ensure you have a ROS 2 environment set up (e.g., ROS 2 Humble or Iron on Ubuntu 22.04). You'll need `rclpy` installed, which typically comes with a standard ROS 2 installation.

## 1. Minimal Publisher Node (Python)

This example demonstrates how to create a simple ROS 2 publisher node in Python that continuously publishes "Hello ROS 2" messages to a topic.

**File**: `docs/chapters/ros2-fundamentals/code-examples.md` (embedded)

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    """
    A minimal ROS 2 publisher node that publishes String messages to a topic.
    """
    def __init__(self):
        # Initialize the Node with the name 'minimal_publisher'
        super().__init__('minimal_publisher')
        # Create a publisher for String messages on the 'topic' topic with a queue size of 10
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds: publish every 0.5 seconds
        # Create a timer that calls the timer_callback method periodically
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0  # Counter for messages published

    def timer_callback(self):
        """
        Callback function executed by the timer. Publishes a new message.
        """
        msg = String()
        msg.data = f'Hello ROS 2: {self.i}' # f-string for cleaner formatting
        self.publisher_.publish(msg)
        # Log the published message (only prints if logger level is INFO or higher)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    """
    Main function to initialize and spin the ROS 2 node.
    """
    rclpy.init(args=args)  # Initialize the ROS 2 client library

    minimal_publisher = MinimalPublisher() # Create an instance of the publisher node

    rclpy.spin(minimal_publisher) # Keep the node alive and process callbacks

    # Destroy the node explicitly to release resources
    minimal_publisher.destroy_node()
    rclpy.shutdown() # Shut down the ROS 2 client library

if __name__ == '__main__':
    main()
```

### How to Run the Publisher

1.  Save the code above into a Python file (e.g., `publisher_node.py`) within your ROS 2 package.
2.  Make sure the file is executable: `chmod +x publisher_node.py`
3.  Source your ROS 2 environment.
4.  Run the node: `ros2 run <your_package_name> publisher_node`

## 2. Minimal Subscriber Node (Python)

This example demonstrates how to create a simple ROS 2 subscriber node in Python that listens for "Hello ROS 2" messages on the same topic.

**File**: `docs/chapters/ros2-fundamentals/code-examples.md` (embedded)

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    """
    A minimal ROS 2 subscriber node that subscribes to String messages from a topic.
    """
    def __init__(self):
        # Initialize the Node with the name 'minimal_subscriber'
        super().__init__('minimal_subscriber')
        # Create a subscriber for String messages on the 'topic' topic
        # It will call the listener_callback method when a message is received
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription # prevent unused variable warning

    def listener_callback(self, msg):
        """
        Callback function executed when a new message is received on the topic.
        """
        self.get_logger().info(f'I heard: "{msg.data}"') # Log the received message

def main(args=None):
    """
    Main function to initialize and spin the ROS 2 node.
    """
    rclpy.init(args=args)  # Initialize the ROS 2 client library

    minimal_subscriber = MinimalSubscriber() # Create an instance of the subscriber node

    rclpy.spin(minimal_subscriber) # Keep the node alive and process callbacks

    # Destroy the node explicitly to release resources
    minimal_subscriber.destroy_node()
    rclpy.shutdown() # Shut down the ROS 2 client library

if __name__ == '__main__':
    main()
```

### How to Run the Subscriber

1.  Save the code above into a Python file (e.g., `subscriber_node.py`) within your ROS 2 package.
2.  Make sure the file is executable: `chmod +x subscriber_node.py`
3.  Source your ROS 2 environment.
4.  Run the node: `ros2 run <your_package_name> subscriber_node`

    *   **Tip**: Run the publisher and subscriber nodes in separate terminal windows to see them communicate!

## 3. Advanced Topics: Custom Messages and Launch Files

### Custom Message Definitions

For more complex data, you'll define custom message types using `.msg` files.

**Example: `custom_interfaces/msg/RobotStatus.msg`**
```
std_msgs/Header header
string robot_name
float32 battery_voltage
bool emergency_stop_active
```

After defining, you compile your package to generate the necessary language-specific bindings.

### ROS 2 Launch Files

Launch files (often written in Python or XML) are used to start multiple ROS 2 nodes and configure their parameters simultaneously. This is crucial for managing complex robot systems.

**Example: `my_robot_launch/launch/my_robot.launch.py`**
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_package',
            executable='publisher_node',
            name='my_publisher',
            output='screen'
        ),
        Node(
            package='my_package',
            executable='subscriber_node',
            name='my_subscriber',
            output='screen'
        )
    ])
```

This launch file starts both the `publisher_node` and `subscriber_node` defined earlier.

## Exercises (Expert)

1.  **Modify Publisher**: Update the `MinimalPublisher` code to publish a custom `RobotStatus` message instead of `String`. Assume `custom_interfaces` is available.
2.  **Create Launch File**: Create a ROS 2 Python launch file that starts both the `MinimalPublisher` and `MinimalSubscriber` nodes.
3.  **QoS Configuration**: Experiment with different QoS settings (e.g., `Reliable` vs `Best Effort` reliability) for the publisher and subscriber, and observe their impact on message delivery in high-traffic scenarios (you might need to add a delay or faster publishing rate).

---
**Next Steps**: Now that User Story 1 (ROS 2 Fundamentals) is complete, you can proceed to User Story 2: Explore Digital Twin Concepts.
