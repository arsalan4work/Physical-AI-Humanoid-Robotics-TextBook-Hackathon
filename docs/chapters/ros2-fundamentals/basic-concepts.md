---
sidebar_position: 2
title: ROS 2 Core Concepts (Intermediate)
description: Intermediate-level breakdown of ROS 2 nodes, topics, services, and actions.
---

# ROS 2 Core Concepts: Diving Deeper (Intermediate)

Building on the beginner introduction, let's delve into the architectural and practical aspects of ROS 2's core concepts. Understanding these in more detail is crucial for developing robust and scalable robot applications.

## 1. Nodes: The Modular Building Blocks

**Intermediate Breakdown:**
Nodes are executable processes. In ROS 2, the philosophy is to have many small, single-purpose nodes rather than one monolithic program. This modularity offers several advantages:

*   **Fault Isolation**: If one node crashes (e.g., a camera driver), the rest of the robot system (e.g., motor control) can continue to function, preventing system-wide failure.
*   **Reusability**: A well-designed node (e.g., a PID controller) can be reused across different robot platforms or projects without modification.
*   **Concurrency**: Nodes can run independently, potentially on different processors or even different machines, leveraging distributed computing for performance.
*   **Development Speed**: Teams can work on different nodes concurrently, speeding up development.

**Lifecycle Management:**
ROS 2 introduces **Managed Nodes** with explicit lifecycle states (unconfigured, inactive, active, finalized). This allows for graceful startup, shutdown, and error recovery, which is critical for real-world robotics.
*   `unconfigured`: Initial state.
*   `inactive`: Node is configured but not processing data.
*   `active`: Node is fully operational and processing data.
*   `finalized`: Node is shutting down.

**Naming Conventions:**
Nodes typically have unique names within a ROS graph (e.g., `/my_robot/camer-node`, `/controller_node`). Namespaces help organize complex systems (e.g., all nodes for a specific arm can be under `/robot_arm/`).

## 2. Topics: Asynchronous Data Streams

**Intermediate Breakdown:**
Topics facilitate **asynchronous, many-to-many communication**. This means a publisher doesn't wait for a subscriber, and multiple subscribers can receive data from a single publisher.

*   **Message Types**: Every topic has a defined message type (e.g., `sensor_msgs/msg/Image`, `geometry_msgs/msg/Twist`). These types enforce data structure, ensuring nodes understand each other. ROS 2 uses IDL (Interface Definition Language) files (`.msg`, `.srv`, `.action`) to define these types.
*   **Quality of Service (QoS)**: A critical feature in ROS 2. QoS settings define how messages are exchanged. Key policies include:
    *   **Reliability**: `Reliable` (guaranteed delivery) vs. `Best Effort` (data loss is acceptable for speed).
    *   **Durability**: `Transient Local` (new subscribers get last message) vs. `Volatile` (subscribers only get messages while active).
    *   **History**: `Keep Last` (only store N latest messages) vs. `Keep All` (store all messages up to a limit).
    *   **Depth**: How many messages to keep if `Keep Last` is chosen.

    **Example**: For camera images, `Best Effort` reliability and `Volatile` durability might be chosen to prioritize fresh data over guaranteed delivery, as older frames are often irrelevant. For robot commands, `Reliable` and `Transient Local` might be preferred to ensure commands are not missed.

## 3. Services: Synchronous Request/Response

**Intermediate Breakdown:**
Services provide **synchronous, one-to-one communication** where a client sends a request and waits for a single response. This is ideal for tasks like:

*   Querying a sensor for a specific reading.
*   Triggering a one-time action (e.g., "open gripper").
*   Requesting complex computations (e.g., path planning for a single destination).

**Service Definition**: Defined by `.srv` files, which specify a request message and a response message.

```
# Request
int64 a
int64 b
---
# Response
int64 sum

```

## 4. Actions: Asynchronous Goal-Based Tasks with Feedback

**Intermediate Breakdown:**
Actions extend services by adding a **feedback mechanism** for long-running goals. They are built on topics and services, providing:

*   **Goal**: The request to perform a long-running task.
*   **Feedback**: Continuous updates on the progress of the goal.
*   **Result**: The final outcome of the goal (success, failure, partial completion).

**Action Definition**: Defined by `.action` files, which include a goal, result, and feedback message.

```
# Goal
int64 order
---
# Result
int64[] sequence
---
# Feedback
int64[] partial_sequence

```

**Example**: A robot navigation action might have a goal of "navigate to (x,y)", provide feedback on the robot's current pose along the path, and return a result indicating if the destination was reached successfully.

## Parameters: Configuration at Runtime

**Intermediate Breakdown:**
Parameters allow nodes to be configured dynamically at runtime without recompiling. They are key-value pairs (`name: value`) and can be of various types (integers, floats, booleans, strings, lists).

*   **Dynamic Reconfigure**: ROS 2 provides tools to change parameters on-the-fly, which is useful for tuning robot behavior (e.g., PID gains, detection thresholds).
*   **YAML Configuration**: Parameters can be loaded from YAML files, simplifying deployment and configuration management for complex robot systems.

## Exercises (Intermediate)

1.  **QoS Application**: For a robot reporting its current battery level:
    *   Would you use `Reliable` or `Best Effort` reliability for the topic publishing battery data? Justify your choice.
    *   Would `Transient Local` or `Volatile` durability be more appropriate? Why?
2.  **Modular Design**: You are designing a robot system with a "movement control" node and a "safety monitoring" node. The safety node needs to stop the robot immediately if an obstacle is detected.
    *   Which communication pattern would be most suitable for the safety node to command the movement control node to stop? Explain why.
3.  **Action vs. Service**: When would you prefer to use a ROS 2 Action over a ROS 2 Service for commanding a robot arm to pick up an object?
4.  **Parameter Utility**: Describe a scenario where dynamically changing a parameter at runtime would be beneficial for debugging or tuning a robot's behavior.

---
**Next Steps**: Proceed to the next section for expert-level insights and functional code examples of these ROS 2 concepts.
