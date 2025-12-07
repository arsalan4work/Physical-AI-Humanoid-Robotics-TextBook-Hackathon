---
sidebar_position: 2
title: Gazebo Simulation (Intermediate/Expert)
description: In-depth guide to robot simulation using Gazebo.
---

# Gazebo Simulation: Bringing Robots to Life in a Virtual World (Intermediate/Expert)

Building on our understanding of digital twins, this section dives deep into **Gazebo**, a powerful 3D robot simulator. Gazebo allows you to accurately simulate robot dynamics, sensor data, and environmental interactions, providing a crucial testbed for your robotics software.

## Prerequisites

*   A working ROS 2 environment (e.g., Humble or Iron on Ubuntu 22.04).
*   Gazebo installed (usually comes with ROS 2 desktop installation, or can be installed separately).
*   Understanding of URDF/SDF (covered below).

## 1. Robot Models: URDF and SDF

To simulate a robot in Gazebo, you need a detailed description of its physical properties. **URDF (Unified Robot Description Format)** and **SDF (Simulation Description Format)** are XML-based file formats used for this purpose.

*   **URDF**: Primarily describes the kinematic and dynamic properties of a single robot. It's often used in ROS for defining robot structure.
*   **SDF**: A more general format used by Gazebo to describe not only robots but also environments, sensors, and other objects in the simulation. SDF can describe multiple robots and environmental elements in a single file.

For most ROS 2 applications, you'll start with a URDF model and often convert it or embed it within an SDF world file for Gazebo.

### Example: Simple Robot URDF Fragment

This URDF defines a very simple robot with a base link and a single wheel.

**File**: `docs/chapters/digital-twin/gazebo-simulation.md` (embedded)

```xml
<?xml version="1.0"?>
<robot name="simple_robot">

  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.2 0.2 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.2 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.005" ixy="0" ixz="0" iyy="0.005" iyz="0" izz="0.005"/>
    </inertial>
  </link>

  <!-- Wheel Link -->
  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.02"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.02"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
  </link>

  <!-- Joint between Base and Wheel -->
  <joint name="base_to_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <origin xyz="-0.1 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>

</robot>
```

### Key Elements of URDF/SDF:

*   **`<link>`**: Defines a rigid body of the robot (e.g., base, wheel, arm segment). It includes:
    *   **`<visual>`**: How the link looks (geometry, color).
    *   **`<collision>`**: How the link interacts physically (shape for collision detection).
    *   **`<inertial>`**: Mass and inertia properties for realistic physics.
*   **`<joint>`**: Defines the connection and motion constraints between two links. Key attributes:
    *   `name`: Unique name for the joint.
    *   `type`: (e.g., `revolute`, `continuous`, `prismatic`, `fixed`).
    *   `parent` and `child`: The links connected by the joint.
    *   `origin`: Position and orientation of the joint relative to the parent link.
    *   `axis`: For revolute/prismatic joints, the axis of rotation/translation.

## 2. Launching Gazebo with ROS 2

To get your robot into Gazebo and interact with it via ROS 2, you'll typically use a ROS 2 launch file.

### Example: Basic Gazebo Launch File (Python)

This launch file starts Gazebo (empty world) and then spawns our `simple_robot` into it.

**File**: `docs/chapters/digital-twin/gazebo-simulation.md` (embedded)

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare arguments
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true',
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            'robot_description',
            default_value=os.path.join(
                get_package_share_directory('my_robot_description'),
                'urdf',
                'simple_robot.urdf' # Assuming this path in your package
            ),
            description='Path to the robot URDF file',
        )
    )

    # Get robot description from URDF file
    robot_description_content = LaunchConfiguration('robot_description')
    with open(LaunchConfiguration('robot_description').perform(context=None), 'r') as file:
        robot_description_content = file.read()

    # Nodes
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'simple_robot'],
        output='screen'
    )

    return LaunchDescription(declared_arguments + [
        # Start Gazebo
        Node(
            package='gazebo_ros',
            executable='gazebo_client', # Use gazebo_client for GUI, gazebo_server for headless
            output='screen',
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        ),
        # Publish robot description
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description_content,
                'use_sim_time': LaunchConfiguration('use_sim_time')
            }],
        ),
        spawn_entity,
    ])
```

### How to Run Gazebo Simulation

1.  **Create a ROS 2 package**: If you don't have one, create a package (e.g., `my_robot_description`) and put your URDF file inside its `urdf/` directory, and your launch file in `launch/`.
2.  **Install dependencies**: Ensure `gazebo_ros` and `robot_state_publisher` are installed (`sudo apt install ros-<ros2-distro>-gazebo-ros-pkgs ros-<ros2-distro>-robot-state-publisher`).
3.  **Build your package**: `colcon build --packages-select my_robot_description`
4.  **Source your workspace**: `source install/setup.bash`
5.  **Launch**: `ros2 launch my_robot_description my_robot.launch.py`

This will open Gazebo with your robot spawned. You can then interact with it using ROS 2 commands (e.g., `ros2 topic echo /tf`).

## Common Simulation Challenges & Debugging

*   **URDF/SDF Errors**: Syntax errors in your robot description files are common. Gazebo and `check_urdf` (if you install `urdf_parser_py`) can help pinpoint issues.
*   **Missing Meshes**: If your model has visual meshes (e.g., `.stl`, `.dae` files), ensure their paths are correct and accessible to Gazebo.
*   **Physics Instability**: Incorrect inertial properties or joint limits can lead to unstable simulations where the robot "explodes" or behaves unnaturally.
*   **ROS 2 Bridge**: Ensure the `gazebo_ros_pkgs` are correctly configured to bridge ROS 2 topics/services with Gazebo.

## Exercises (Intermediate/Expert)

1.  **Modify URDF**: Extend the `simple_robot.urdf` to include a second wheel or a simple sensor (e.g., a `box` link representing a camera) attached to the `base_link` with a fixed joint.
2.  **Custom World**: Create a simple Gazebo world (e.g., a flat plane with a cube obstacle) in an `.sdf` file and launch your robot into this world using a modified launch file.
3.  **Control Integration**: Research `ros2_control` and propose how you would integrate it with your Gazebo robot to control its joints (e.g., make the wheel spin).

---
**Next Steps**: Now that you have a grasp of Gazebo simulation, we will explore how to visualize these simulations using Unity.
