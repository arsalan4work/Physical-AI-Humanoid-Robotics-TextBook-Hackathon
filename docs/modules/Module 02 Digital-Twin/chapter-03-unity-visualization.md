---
sidebar_position: 3
title: Unity Visualization (Intermediate/Expert)
description: Guide to visualizing robot simulations in Unity.
---

# Unity Visualization: Real-time Rendering for Digital Twins (Intermediate/Expert)

While Gazebo excels in physics-accurate simulation, **Unity** offers unparalleled capabilities for high-fidelity visualization, user interfaces, and complex interactive environments. Integrating Unity with your robot simulations allows for realistic rendering, immersive experiences, and advanced data visualization, making it an excellent companion for digital twins.

## Prerequisites

*   Unity Hub and Unity Editor installed (latest LTS version recommended).
*   Basic understanding of Unity development (C# scripting, scene management).
*   A running ROS 2 / Gazebo simulation (from previous sections).
*   Familiarity with ROS-Unity integrations (e.g., `ROS-TCP-Connector`, `ROS#.Unity`).

## 1. ROS-Unity Integration Overview

Connecting Unity to your ROS 2 ecosystem typically involves a bridge that translates ROS messages into Unity-understandable data, and vice-versa. Popular methods include:

*   **ROS-TCP-Connector**: A Unity package that facilitates communication with ROS 2 over TCP. This is often preferred for direct, real-time data streaming.
*   **ROS#.Unity (ROS#)**: A more mature framework for Unity to interact with ROS, offering comprehensive message serialization and deserialization.

For this textbook, we will focus on the conceptual integration and a basic C# example that would typically receive data from a ROS 2 topic.

## 2. Setting Up a Unity Project for Robot Visualization

1.  **Create a New Unity Project**: Open Unity Hub and create a new 3D (URP or HDRP for modern rendering) project.
2.  **Import Robot Model**: Import your robot's visual assets (e.g., `.fbx`, `.dae`, `.stl` files) into your Unity project. Assemble them in the scene to match your URDF/SDF structure.
3.  **Install ROS-Unity Bridge**: Install the chosen ROS-Unity communication package (e.g., ROS-TCP-Connector via Unity Package Manager).
4.  **Create a ROS Bridge Node**: In your ROS 2 environment, you'll need a Python node (or similar) that bridges the simulation data from Gazebo (or other ROS 2 topics) to the Unity application via the chosen connector.

## 3. Example: Receiving Robot Pose Data in Unity (C#)

This C# script for Unity demonstrates how a `MonoBehaviour` might subscribe to a ROS 2 topic (via a ROS-Unity bridge) and update a robot's pose within the Unity scene. This assumes a ROS-Unity connector is set up and publishing `geometry_msgs/Pose` data to a `/robot_pose` topic.

**File**: `docs/chapters/digital-twin/unity-visualization.md` (embedded)

```csharp
using UnityEngine;
using RosMessageTypes.Geometry; // Assuming you have ROS#.Unity or similar message types
using Ros; // Assuming Ros-TCP-Connector namespace

public class RobotPoseSubscriber : MonoBehaviour
{
    public string rosTopicName = "/robot_pose"; // The ROS 2 topic to subscribe to
    private ROSConnection ros;

    void Start()
    {
        // Get the ROSConnection instance (assuming it's in the scene)
        ros = ROSConnection.Get           (  );
        if (ros != null)
        {
            // Subscribe to the ROS 2 topic
            ros.Subscribe<PoseMsg>(rosTopicName, ReceivePoseMessage);
            Debug.Log($"Subscribed to ROS topic: {rosTopicName}");
        }
        else
        {
            Debug.LogError("ROSConnection not found in the scene. Please add it.");
        }
    }

    void ReceivePoseMessage(PoseMsg poseMessage)
    {
        // ROS coordinates (Z-up, X-forward) usually need conversion to Unity (Y-up, Z-forward)
        Vector3 position = new Vector3(
            (float)poseMessage.position.x,
            (float)poseMessage.position.z, // Z from ROS becomes Y in Unity
            (float)poseMessage.position.y * -1 // Y from ROS becomes -Z in Unity (or similar)
        );

        Quaternion rotation = new Quaternion(
            (float)poseMessage.orientation.x,
            (float)poseMessage.orientation.z, // Z from ROS becomes Y in Unity
            (float)poseMessage.orientation.y * -1, // Y from ROS becomes -Z in Unity
            (float)poseMessage.orientation.w
        );

        // Apply the received pose to the GameObject
        transform.localPosition = position;
        transform.localRotation = rotation;

        Debug.Log($"Received pose for robot: Position({position}), Rotation({rotation.eulerAngles})");
    }
}
```

### How to Use This Unity Script

1.  Attach this script to the root GameObject of your robot model in Unity.
2.  Ensure you have the `ROSConnection` component (from ROS-TCP-Connector) in your Unity scene, and it's configured to connect to your ROS 2 environment.
3.  In your ROS 2 environment, a node needs to publish `geometry_msgs/Pose` messages to the `/robot_pose` topic, reflecting your robot's actual or simulated position.

## Common Unity Integration Challenges

*   **Coordinate System Mismatches**: ROS uses a Z-up, X-forward coordinate system, while Unity uses Y-up, Z-forward. This requires careful conversion for positions and rotations.
*   **Message Serialization**: Ensuring that ROS 2 messages are correctly serialized and deserialized between ROS 2 and Unity.
*   **Performance**: High-frequency data streams (e.g., camera images) can impact Unity's performance. Consider data throttling or efficient message types.
*   **Setup Complexity**: Integrating ROS 2 and Unity can involve multiple layers of configuration and code.

## Exercises (Intermediate/Expert)

1.  **Coordinate Conversion**: Research the exact coordinate system transformations required when converting from ROS (REP 103) to Unity, and explain why each axis changes.
2.  **Publisher Implementation**: Design a C# script that would allow Unity to *publish* commands (e.g., `geometry_msgs/Twist`) back to a ROS 2 robot, thereby controlling it from Unity.
3.  **Advanced Visualization**: Explore how you might visualize sensor data (e.g., LiDAR point clouds from a ROS 2 topic) within a Unity scene, perhaps using Unity's VFX Graph or custom rendering.

---
**Next Steps**: Now that User Story 2 (Digital Twin Concepts) is complete, you can proceed to User Story 3: Implement Vision-Language-Action Robotics.
