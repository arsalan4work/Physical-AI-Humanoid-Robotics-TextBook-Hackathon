---
title: Manipulation and Control
sidebar_label: Manipulation
description: Advanced manipulation techniques and control strategies for humanoid robots
---

# Manipulation and Control

## Introduction to Humanoid Manipulation

Humanoid manipulation involves using the robot's arms and hands to interact with objects in the environment. Unlike industrial manipulators that are fixed to a base, humanoid robots must perform manipulation tasks while maintaining balance and coordinating with locomotion. This chapter explores the principles and techniques of humanoid manipulation and control.

## Challenges in Humanoid Manipulation

Humanoid manipulation presents unique challenges compared to fixed-base manipulators:

### Balance Constraints
- Manipulation actions can affect the robot's balance
- Must coordinate arm movements with postural adjustments
- Need to consider CoM displacement during manipulation

### Redundancy Management
- Humanoid robots have many more degrees of freedom than needed for simple tasks
- Must optimize joint configurations for multiple objectives
- Need to consider obstacle avoidance and joint limits

### Dual-Arm Coordination
- Tasks often require both arms working together
- Need to coordinate movements to avoid self-collisions
- Must manage load distribution between arms

### Dynamic Environment
- Robot may be moving while manipulating
- Need to adapt to changing base positions
- Must handle external disturbances during manipulation

## Manipulation Control Strategies

### Operational Space Control

Operational space control allows direct control of end-effector motion while maintaining balance:

```python
import numpy as np
from scipy.spatial.transform import Rotation as R

class OperationalSpaceController:
    def __init__(self, robot_model):
        self.model = robot_model

    def compute_operational_control(self, target_pos, target_vel, target_acc,
                                   current_pos, current_vel, current_joints):
        """
        Compute operational space control for end-effector
        """
        # Calculate Jacobian
        J = self.model.compute_jacobian(current_joints)

        # Calculate task-space error
        pos_error = target_pos - current_pos
        vel_error = target_vel - current_vel

        # Task-space acceleration command
        Kp = np.eye(3) * 10.0  # Position gain
        Kd = np.eye(3) * 6.32  # Velocity gain (critically damped)

        task_acc = target_acc + Kp @ pos_error + Kd @ vel_error

        # Map to joint space
        J_inv = np.linalg.pinv(J)
        joint_acc = J_inv @ task_acc

        return joint_acc

    def compute_nullspace_control(self, joint_acc, desired_nullspace_motion):
        """
        Add nullspace motion to the control
        """
        J = self.model.compute_jacobian()
        J_inv = np.linalg.pinv(J)

        # Nullspace projection matrix
        I = np.eye(len(joint_acc))
        N = I - J_inv @ J

        # Add nullspace motion
        nullspace_acc = N @ desired_nullspace_motion

        return joint_acc + nullspace_acc
```

### Impedance Control

Impedance control allows the robot to behave like a spring-damper system, useful for contact tasks:

```python
class ImpedanceController:
    def __init__(self, stiffness=1000, damping=100, mass=10):
        self.M = np.eye(6) * mass      # Mass matrix
        self.D = np.eye(6) * damping   # Damping matrix
        self.K = np.eye(6) * stiffness # Stiffness matrix

    def compute_impedance_control(self, target_pose, current_pose,
                                 target_vel, current_vel, target_acc):
        """
        Compute impedance control law
        """
        # Calculate pose error (position and orientation)
        pos_error = target_pose[:3] - current_pose[:3]

        # For orientation, use rotation error
        R_current = current_pose[3:].reshape(3, 3)  # Assuming rotation matrix
        R_target = target_pose[3:].reshape(3, 3)
        R_error = R_target.T @ R_current
        # Convert to angle-axis representation for error
        angle_axis_error = self.rotation_matrix_to_angle_axis(R_error)

        pose_error = np.concatenate([pos_error, angle_axis_error])

        # Calculate velocity error
        vel_error = target_vel - current_vel

        # Impedance control law
        acc_command = (np.linalg.inv(self.M) @
                      (self.K @ pose_error +
                       self.D @ vel_error +
                       self.M @ target_acc))

        return acc_command

    def rotation_matrix_to_angle_axis(self, R):
        """
        Convert rotation matrix to angle-axis representation
        """
        angle = np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1))

        if np.abs(angle) < 1e-6:
            return np.zeros(3)

        axis = np.array([R[2, 1] - R[1, 2],
                         R[0, 2] - R[2, 0],
                         R[1, 0] - R[0, 1]]) / (2 * np.sin(angle))

        return angle * axis
```

## Dual-Arm Manipulation

### Coordinated Manipulation

When two arms work together, special coordination is needed:

```python
class DualArmController:
    def __init__(self, left_arm_model, right_arm_model):
        self.left_arm = left_arm_model
        self.right_arm = right_arm_model

    def coordinated_object_transport(self, object_pose, object_mass):
        """
        Control both arms to transport an object
        """
        # Calculate required forces at each hand
        gravity_force = np.array([0, 0, -object_mass * 9.81])

        # Distribute load between arms
        left_force = gravity_force / 2
        right_force = gravity_force / 2

        # Calculate required hand poses to maintain object orientation
        left_hand_pose = self.calculate_hand_pose(object_pose, 'left')
        right_hand_pose = self.calculate_hand_pose(object_pose, 'right')

        # Control both arms to achieve desired forces and poses
        left_control = self.compute_arm_control('left', left_hand_pose, left_force)
        right_control = self.compute_arm_control('right', right_hand_pose, right_force)

        return left_control, right_control

    def calculate_hand_pose(self, object_pose, hand_side):
        """
        Calculate hand pose for coordinated manipulation
        """
        # This would involve inverse kinematics with constraints
        # to maintain object orientation and handle forces properly
        pass
```

### Priority-Based Control

Use priorities to manage multiple tasks simultaneously:

```python
class PriorityBasedController:
    def __init__(self, robot_model):
        self.model = robot_model

    def compute_priority_control(self, high_priority_task, low_priority_task):
        """
        Execute high-priority task while trying to achieve low-priority task
        """
        # High priority task
        J1 = high_priority_task['jacobian']
        e1 = high_priority_task['error']
        Kp1, Kd1 = high_priority_task['gains']

        # Compute control for high priority task
        task_acc_1 = Kp1 * e1 + Kd1 * high_priority_task['error_derivative']
        J1_pinv = np.linalg.pinv(J1)
        joint_acc_1 = J1_pinv @ task_acc_1

        # Low priority task in nullspace of high priority task
        J2 = low_priority_task['jacobian']
        e2 = low_priority_task['error']
        Kp2, Kd2 = low_priority_task['gains']

        # Nullspace projection
        I = np.eye(len(joint_acc_1))
        N1 = I - J1_pinv @ J1

        # Compute low priority control in nullspace
        task_acc_2 = Kp2 * e2 + Kd2 * low_priority_task['error_derivative']
        J2_N = J2 @ N1  # J2 projected into nullspace of J1
        J2_N_pinv = np.linalg.pinv(J2_N)

        joint_acc_2 = J2_N_pinv @ task_acc_2

        # Total control
        total_joint_acc = joint_acc_1 + joint_acc_2

        return total_joint_acc
```

## Grasp Planning and Execution

### Grasp Stability Analysis

```python
class GraspAnalyzer:
    def __init__(self):
        pass

    def compute_grasp_matrix(self, contact_points, contact_normals):
        """
        Compute grasp matrix for analyzing grasp stability
        """
        G = np.zeros((6, 3 * len(contact_points)))  # 6 DOF object, 3 DOF per contact

        for i, (point, normal) in enumerate(zip(contact_points, contact_normals)):
            # Position cross product part
            p_skew = np.array([
                [0, -point[2], point[1]],
                [point[2], 0, -point[0]],
                [-point[1], point[0], 0]
            ])

            # Fill grasp matrix
            G[:3, 3*i:3*i+3] = np.eye(3)  # Translation part
            G[3:, 3*i:3*i+3] = p_skew      # Rotation part

        return G

    def check_grasp_stability(self, grasp_matrix, friction_cones):
        """
        Check if grasp can resist external wrenches
        """
        # This would involve checking if the grasp can resist
        # arbitrary external forces and torques
        # Implementation involves convex optimization
        pass
```

### Adaptive Impedance Control

Adjust impedance parameters based on task requirements:

```python
class AdaptiveImpedanceController:
    def __init__(self):
        self.base_stiffness = np.eye(6) * 1000
        self.base_damping = np.eye(6) * 100

    def adjust_impedance(self, task_phase, contact_state, object_properties):
        """
        Adjust impedance based on current task requirements
        """
        if task_phase == 'approach':
            # Low stiffness for safe approach
            stiffness = self.base_stiffness * 0.1
            damping = self.base_damping * 0.1
        elif task_phase == 'contact':
            # Variable stiffness based on contact compliance
            if contact_state['soft_contact']:
                stiffness = self.base_stiffness * 0.5
            else:
                stiffness = self.base_stiffness * 2.0
            damping = self.base_damping * 1.5
        elif task_phase == 'manipulation':
            # High stiffness for precise control
            stiffness = self.base_stiffness
            damping = self.base_damping
        elif task_phase == 'release':
            # Low stiffness to avoid sticking
            stiffness = self.base_stiffness * 0.2
            damping = self.base_damping * 0.2

        return stiffness, damping
```

## Whole-Body Control

### Task-Priority Framework

```python
class WholeBodyController:
    def __init__(self, robot_model):
        self.model = robot_model
        self.tasks = []

    def add_task(self, task_name, jacobian, desired_value, priority, weight=1.0):
        """
        Add a control task with specified priority
        """
        task = {
            'name': task_name,
            'jacobian': jacobian,
            'desired': desired_value,
            'priority': priority,
            'weight': weight
        }
        self.tasks.append(task)

    def compute_whole_body_control(self, current_state):
        """
        Compute whole-body control with task priorities
        """
        # Sort tasks by priority
        sorted_tasks = sorted(self.tasks, key=lambda x: x['priority'])

        joint_acc = np.zeros(self.model.num_joints)
        current_jacobian = np.zeros((0, self.model.num_joints))

        for task in sorted_tasks:
            # Compute task error
            error = task['desired'] - self.model.compute_task_value(task['name'], current_state)

            # Compute Jacobian for current configuration
            J_task = task['jacobian'](current_state)

            # Project into nullspace of higher priority tasks
            if current_jacobian.shape[0] > 0:
                P = np.eye(self.model.num_joints) - np.linalg.pinv(current_jacobian) @ current_jacobian
                J_task_null = J_task @ P
            else:
                J_task_null = J_task

            # Compute control
            J_pinv = np.linalg.pinv(J_task_null)
            task_acc = J_pinv @ error

            # Add to total control
            joint_acc += task_acc

            # Update current Jacobian for nullspace projection
            current_jacobian = np.vstack([current_jacobian, J_task]) if current_jacobian.shape[0] > 0 else J_task

        return joint_acc

# Example usage:
# controller = WholeBodyController(robot_model)
# controller.add_task('balance', balance_jacobian, desired_com, priority=1, weight=1.0)
# controller.add_task('left_hand', left_hand_jacobian, desired_left_hand_pose, priority=2, weight=0.8)
# controller.add_task('right_hand', right_hand_jacobian, desired_right_hand_pose, priority=3, weight=0.8)
```

## Control Implementation with ROS 2

### Using MoveIt! for Manipulation

```python
import rclpy
from rclpy.node import Node
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, RobotState
from geometry_msgs.msg import PoseStamped
from control_msgs.action import FollowJointTrajectory
import numpy as np

class HumanoidManipulationController(Node):
    def __init__(self):
        super().__init__('humanoid_manipulation_controller')

        # Action clients for MoveIt! and trajectory execution
        self.move_group_client = ActionClient(self, MoveGroup, 'move_group')
        self.trajectory_client = ActionClient(self, FollowJointTrajectory, 'joint_trajectory_controller/follow_joint_trajectory')

        # Publisher for real-time control
        self.joint_cmd_pub = self.create_publisher(JointTrajectory, 'joint_group_position_controller/command', 10)

    def plan_dual_arm_motion(self, left_target_pose, right_target_pose):
        """
        Plan coordinated motion for both arms
        """
        # Create planning request for left arm
        left_goal = MoveGroup.Goal()
        left_goal.request.group_name = 'left_arm'
        left_goal.request.workspace_parameters.header.frame_id = 'base_link'

        # Add target pose constraint
        left_pose_constraint = self.create_pose_constraint('l_wrist', left_target_pose)
        left_goal.request.goal_constraints.append(
            Constraints(position_constraints=[], orientation_constraints=[],
                       visibility_constraints=[], joint_constraints=[],
                       pose_constraints=[left_pose_constraint])
        )

        # Similar for right arm
        right_goal = MoveGroup.Goal()
        right_goal.request.group_name = 'right_arm'
        right_pose_constraint = self.create_pose_constraint('r_wrist', right_target_pose)
        right_goal.request.goal_constraints.append(
            Constraints(pose_constraints=[right_pose_constraint])
        )

        # Execute both plans simultaneously or sequentially based on collision checking
        return self.execute_coordinated_plan(left_goal, right_goal)

    def create_pose_constraint(self, link_name, target_pose):
        """
        Create a pose constraint for MoveIt!
        """
        from moveit_msgs.msg import PositionConstraint, OrientationConstraint
        from shape_msgs.msg import SolidPrimitive
        from geometry_msgs.msg import Point

        # Position constraint
        pos_constraint = PositionConstraint()
        pos_constraint.link_name = link_name
        pos_constraint.target_point_offset = Point(x=0.0, y=0.0, z=0.0)
        pos_constraint.constraint_region.primitives.append(SolidPrimitive(type=SolidPrimitive.SPHERE, dimensions=[0.01]))

        # Orientation constraint
        orientation_constraint = OrientationConstraint()
        orientation_constraint.link_name = link_name
        orientation_constraint.orientation = target_pose.orientation
        orientation_constraint.absolute_x_axis_tolerance = 0.1
        orientation_constraint.absolute_y_axis_tolerance = 0.1
        orientation_constraint.absolute_z_axis_tolerance = 0.1
        orientation_constraint.weight = 1.0

        return orientation_constraint
```

## Advanced Control Techniques

### Model Predictive Control (MPC) for Manipulation

```python
import cvxpy as cp

class MPCManipulationController:
    def __init__(self, horizon=20, dt=0.01):
        self.horizon = horizon
        self.dt = dt

    def solve_mpc_problem(self, current_state, target_trajectory, constraints):
        """
        Solve MPC optimization problem for manipulation
        """
        # Define optimization variables
        X = cp.Variable((7, self.horizon + 1))  # State: [pos, vel, acc]
        U = cp.Variable((6, self.horizon))      # Control: joint torques or accelerations

        # Cost function
        cost = 0
        for k in range(self.horizon):
            # Tracking cost
            cost += cp.sum_squares(X[:3, k+1] - target_trajectory[k])

            # Control effort cost
            cost += 0.01 * cp.sum_squares(U[:, k])

        # Dynamics constraints
        constraints_list = []
        constraints_list.append(X[:, 0] == current_state)  # Initial state

        for k in range(self.horizon):
            # Simple double integrator dynamics (simplified)
            constraints_list.append(X[3:6, k+1] == X[3:6, k] + U[:, k] * self.dt)
            constraints_list.append(X[:3, k+1] == X[:3, k] + X[3:6, k] * self.dt + 0.5 * U[:, k] * self.dt**2)

        # Add system constraints
        constraints_list.extend(constraints)

        # Solve optimization problem
        problem = cp.Problem(cp.Minimize(cost), constraints_list)
        problem.solve()

        if problem.status == cp.OPTIMAL:
            return U[:, 0].value  # Return first control input
        else:
            return None
```

## Exercises

1. Implement a simple operational space controller and test it with different end-effector trajectories
2. Design a dual-arm coordination controller for carrying an object
3. Implement an impedance controller and experiment with different stiffness/damping values
4. Create a grasp stability analyzer for a simple object
5. Design a whole-body controller that balances while reaching with one arm
6. Implement a basic MPC controller for a single joint and compare with PID

## Summary

Humanoid manipulation combines advanced control techniques with the need to maintain balance and coordinate multiple limbs. Key strategies include operational space control, impedance control, priority-based frameworks, and whole-body control approaches. Successful humanoid manipulation requires considering the interaction between manipulation tasks and balance control, as well as coordinating multiple degrees of freedom in real-time. Modern approaches use sophisticated optimization techniques and sensor feedback to achieve robust manipulation performance.