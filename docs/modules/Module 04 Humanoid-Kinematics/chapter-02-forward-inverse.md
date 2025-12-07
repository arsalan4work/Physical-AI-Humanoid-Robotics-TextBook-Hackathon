---
title: Forward and Inverse Kinematics for Humanoid Robots
sidebar_label: Kinematics
description: Understanding forward and inverse kinematics in complex humanoid systems
---

# Forward and Inverse Kinematics for Humanoid Robots

## Introduction to Kinematics

Kinematics is the study of motion without considering the forces that cause it. In robotics, kinematics describes the relationship between joint angles and the position and orientation of the robot's end-effectors (hands, feet, head). For humanoid robots, this becomes particularly complex due to the large number of degrees of freedom and the need to coordinate multiple limbs simultaneously.

## Forward Kinematics

Forward kinematics calculates the position and orientation of an end-effector given the joint angles. For a humanoid robot, this means knowing where each hand, foot, and head is located in space based on all the joint angles in the system.

### Mathematical Foundation

The forward kinematics of a humanoid robot is typically solved using the Denavit-Hartenberg (DH) convention or product-of-exponentials (PoE) formulation. For each kinematic chain (arm, leg), we can represent the transformation from base to end-effector as:

```
T = T1(θ1) * T2(θ2) * ... * Tn(θn)
```

Where T is the transformation matrix and Ti(θi) represents the transformation due to joint i with angle θi.

### Humanoid-Specific Considerations

In humanoid robots, we must consider multiple kinematic chains simultaneously:

- **Left Arm Chain**: Shoulder → Elbow → Wrist → Hand
- **Right Arm Chain**: Shoulder → Elbow → Wrist → Hand
- **Left Leg Chain**: Hip → Knee → Ankle → Foot
- **Right Leg Chain**: Hip → Knee → Ankle → Foot
- **Head Chain**: Neck joints

### Example: Humanoid Arm Forward Kinematics

```python
import numpy as np
from scipy.spatial.transform import Rotation as R

def forward_kinematics_arm(joint_angles):
    """
    Calculate forward kinematics for a humanoid arm
    joint_angles: [shoulder_yaw, shoulder_pitch, shoulder_roll, elbow_pitch, wrist_yaw, wrist_pitch]
    """
    # Define link lengths (in meters) - example for adult-sized humanoid
    l_shoulder = 0.15  # distance from body to shoulder
    l_upper_arm = 0.30  # upper arm length
    l_lower_arm = 0.28  # lower arm length
    l_hand = 0.10       # hand length

    # Extract joint angles
    shoulder_yaw, shoulder_pitch, shoulder_roll, elbow_pitch, wrist_yaw, wrist_pitch = joint_angles

    # Calculate transformations for each joint
    # Base to shoulder
    T01 = np.eye(4)
    T01[:3, :3] = R.from_euler('xyz', [0, 0, shoulder_yaw]).as_matrix()
    T01[:3, 3] = [l_shoulder, 0, 0]

    # Shoulder to elbow
    T12 = np.eye(4)
    T12[:3, :3] = R.from_euler('xyz', [shoulder_pitch, shoulder_roll, 0]).as_matrix()
    T12[:3, 3] = [l_upper_arm, 0, 0]

    # Elbow to wrist
    T23 = np.eye(4)
    T23[:3, :3] = R.from_euler('xyz', [elbow_pitch, 0, 0]).as_matrix()
    T23[:3, 3] = [l_lower_arm, 0, 0]

    # Wrist to hand
    T34 = np.eye(4)
    T34[:3, :3] = R.from_euler('xyz', [wrist_pitch, wrist_yaw, 0]).as_matrix()
    T34[:3, 3] = [l_hand, 0, 0]

    # Combine transformations
    T_total = T01 @ T12 @ T23 @ T34

    return T_total
```

## Inverse Kinematics

Inverse kinematics (IK) is the reverse problem: given a desired position and orientation for an end-effector, calculate the required joint angles. This is significantly more complex than forward kinematics and often has multiple solutions or no solution at all.

### Challenges in Humanoid IK

Humanoid robots face several unique challenges in inverse kinematics:

1. **Redundancy**: More degrees of freedom than required to reach a target
2. **Multiple Constraints**: Need to satisfy balance, joint limits, and collision avoidance
3. **Real-time Requirements**: IK must be solved quickly for responsive behavior
4. **Multiple End-effectors**: Must coordinate arms, legs, and head simultaneously

### Common IK Approaches

#### 1. Analytical IK
For simple chains, closed-form solutions exist. However, humanoid robots are too complex for pure analytical solutions.

#### 2. Numerical IK
Iterative methods that approximate the solution:

```python
import numpy as np
from scipy.spatial.transform import Rotation as R

def jacobian_ik(target_pos, target_rot, current_joints, jacobian_func, max_iter=100, tolerance=1e-4):
    """
    Jacobian-based inverse kinematics solver
    """
    joints = current_joints.copy()

    for i in range(max_iter):
        # Calculate current end-effector pose
        current_pose = forward_kinematics(joints)
        current_pos = current_pose[:3, 3]
        current_rot = current_pose[:3, :3]

        # Calculate error
        pos_error = target_pos - current_pos
        rot_error = rotation_error(target_rot, current_rot)

        # Check convergence
        if np.linalg.norm(pos_error) < tolerance and np.linalg.norm(rot_error) < tolerance:
            break

        # Calculate Jacobian
        J = jacobian_func(joints)

        # Solve for joint updates
        error = np.concatenate([pos_error, rot_error])
        delta_joints = np.linalg.pinv(J) @ error

        # Update joints
        joints += delta_joints

        # Apply joint limits
        joints = np.clip(joints, joint_limits_min, joint_limits_max)

    return joints

def rotation_error(R1, R2):
    """
    Calculate rotation error between two rotation matrices
    """
    R_rel = R1.T @ R2
    angle_axis = rotation_matrix_to_angle_axis(R_rel)
    return angle_axis
```

#### 3. Optimization-Based IK
Formulate IK as an optimization problem with multiple objectives:

```python
import numpy as np
from scipy.optimize import minimize

def optimization_ik(target_pos, target_rot, initial_joints, constraints):
    """
    Optimization-based inverse kinematics
    """
    def objective(joints):
        # Primary objective: reach target
        current_pose = forward_kinematics(joints)
        pos_error = np.linalg.norm(target_pos - current_pose[:3, 3])
        rot_error = rotation_error(target_rot, current_pose[:3, :3])

        # Secondary objectives: minimize joint motion, maintain balance, etc.
        joint_motion = np.sum((joints - initial_joints)**2)

        return pos_error + rot_error + 0.1 * joint_motion

    result = minimize(objective, initial_joints, method='SLSQP', constraints=constraints)
    return result.x
```

## Humanoid-Specific Kinematic Considerations

### Balance and Center of Mass

For humanoid robots, IK solutions must consider the center of mass (CoM) to maintain balance:

```python
def compute_com(robot_state):
    """
    Compute center of mass of the humanoid robot
    """
    total_mass = 0
    weighted_pos = np.zeros(3)

    for link in robot_state.links:
        total_mass += link.mass
        weighted_pos += link.mass * link.com_position

    com_position = weighted_pos / total_mass
    return com_position

def is_balanced(robot_state, support_polygon):
    """
    Check if the robot is balanced based on CoM projection
    """
    com_proj = compute_com(robot_state)[:2]  # Project to 2D ground plane
    return point_in_polygon(com_proj, support_polygon)
```

### Whole-Body IK

Humanoid robots require solving IK for multiple end-effectors simultaneously while maintaining balance:

```python
class WholeBodyIK:
    def __init__(self, robot_model):
        self.robot = robot_model

    def solve(self, tasks):
        """
        Solve whole-body inverse kinematics with multiple tasks
        tasks: list of (end_effector, target_pose, weight)
        """
        # Formulate as constrained optimization problem
        # Minimize: sum of task errors weighted by importance
        # Subject to: balance constraints, joint limits, collision avoidance

        # This is a simplified representation
        # Real implementation would use sophisticated solvers
        pass
```

## Practical Implementation with ROS 2

Using MoveIt! for humanoid kinematics:

```xml
<!-- In robot's URDF/SRDF -->
<group name="left_arm">
  <chain base_link="torso" tip_link="l_wrist"/>
</group>
<group name="right_arm">
  <chain base_link="torso" tip_link="r_wrist"/>
</group>
<group name="left_leg">
  <chain base_link="torso" tip_link="l_foot"/>
</group>
<group name="right_leg">
  <chain base_link="torso" tip_link="r_foot"/>
</group>
```

```python
import rclpy
from moveit_msgs.srv import GetPositionIK
from moveit_msgs.msg import RobotState, Constraints
from sensor_msgs.msg import JointState

class HumanoidKinematicsNode:
    def __init__(self):
        self.ik_client = self.create_client(GetPositionIK, 'compute_ik')

    def solve_ik(self, group_name, target_pose, current_joints):
        request = GetPositionIK.Request()
        request.ik_request.group_name = group_name
        request.ik_request.pose_stamped.pose = target_pose
        request.ik_request.robot_state.joint_state = current_joints

        future = self.ik_client.call_async(request)
        return future
```

## Exercises

1. Implement forward kinematics for a simplified 3-DOF arm and verify with geometric calculations
2. Research and compare different IK solvers (Jacobian pseudoinverse, Damped Least Squares, CCD)
3. Design a simple whole-body IK problem with balance constraints for a 2D biped
4. Explore MoveIt! configuration for a humanoid robot (e.g., HRP-2 or NAO)
5. Implement a basic Jacobian-based IK solver and test it with different target positions

## Summary

Forward and inverse kinematics form the mathematical foundation for controlling humanoid robots. While forward kinematics is straightforward, inverse kinematics for humanoid robots is complex due to redundancy, multiple constraints, and real-time requirements. Modern approaches combine numerical methods with optimization techniques to solve whole-body kinematics while maintaining balance and avoiding collisions.