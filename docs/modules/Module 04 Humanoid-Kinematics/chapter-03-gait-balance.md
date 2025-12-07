---
title: Gait, Balance, and Locomotion
sidebar_label: Gait and Balance
description: Understanding humanoid gait patterns, balance control, and locomotion strategies
---

# Gait, Balance, and Locomotion

## Introduction to Humanoid Locomotion

Humanoid locomotion is one of the most challenging problems in robotics. Unlike wheeled robots that can maintain stability through continuous contact with the ground, bipedal robots must constantly balance on two legs, mimicking the complex biomechanics of human walking. This chapter explores the principles of humanoid gait, balance control, and locomotion strategies.

## The Challenge of Bipedal Locomotion

Walking on two legs is inherently unstable. A biped robot must:

- Maintain its center of mass (CoM) within the support polygon defined by its feet
- Manage the dynamic forces during walking
- Adapt to terrain variations and disturbances
- Coordinate multiple joints in a coordinated pattern

### Key Concepts in Humanoid Locomotion

1. **Zero Moment Point (ZMP)**: The point on the ground where the net moment of the ground reaction force is zero
2. **Center of Pressure (CoP)**: The point where the ground reaction force acts
3. **Capture Point**: The point where a robot must step to come to a complete stop
4. **Support Polygon**: The convex hull of all ground contact points

## Gait Patterns and Walking Phases

### Double Support Phase
During double support, both feet are in contact with the ground. This is the most stable phase of walking.

### Single Support Phase
During single support, only one foot is in contact with the ground. This is the most dynamically challenging phase.

### Walking Pattern Generation

The most common approach to humanoid walking is the **ZMP-based walking pattern generation**:

```python
import numpy as np
from scipy import signal

class ZMPWalker:
    def __init__(self, robot_height, step_length, step_width, step_time):
        self.omega = np.sqrt(9.81 / robot_height)  # Natural frequency
        self.step_length = step_length
        self.step_width = step_width
        self.step_time = step_time

    def generate_footsteps(self, num_steps, start_pos=(0, 0), start_yaw=0):
        """
        Generate a sequence of footsteps for walking
        """
        footsteps = []
        x, y, yaw = start_pos[0], start_pos[1], start_yaw

        for i in range(num_steps):
            # Alternate feet
            if i % 2 == 0:  # Right foot
                foot_x = x + self.step_length / 2
                foot_y = y - self.step_width / 2
            else:  # Left foot
                foot_x = x + self.step_length / 2
                foot_y = y + self.step_width / 2

            # Update position for next step
            x += self.step_length * np.cos(yaw)
            y += self.step_length * np.sin(yaw)

            footsteps.append((foot_x, foot_y, yaw))

        return footsteps

    def generate_zmp_trajectory(self, footsteps):
        """
        Generate ZMP trajectory based on footsteps
        """
        # Simplified ZMP reference trajectory
        zmp_x = []
        zmp_y = []

        for i, (fx, fy, fyaw) in enumerate(footsteps):
            # Generate ZMP trajectory for each step
            t = np.linspace(0, self.step_time, int(self.step_time * 100))  # 100 Hz

            # Simple ZMP reference - stays under the supporting foot
            for j in range(len(t)):
                zmp_x.append(fx - 0.5 * self.step_length * (1 - np.cos(np.pi * j / len(t))))
                zmp_y.append(fy)

        return np.array(zmp_x), np.array(zmp_y)
```

## Balance Control Strategies

### Center of Mass (CoM) Control

The most fundamental approach to balance control is to maintain the CoM within the support polygon:

```python
class BalanceController:
    def __init__(self, robot_mass, gravity=9.81):
        self.mass = robot_mass
        self.gravity = gravity
        self.g = gravity

    def compute_com_dynamics(self, com_pos, com_vel, external_forces):
        """
        Compute CoM dynamics
        """
        # CoM acceleration = (external forces) / mass
        com_acc = external_forces / self.mass
        return com_acc

    def compute_stability_margin(self, com_pos, support_polygon):
        """
        Compute stability margin based on CoM position relative to support polygon
        """
        # Project CoM to ground plane
        com_2d = np.array([com_pos[0], com_pos[1]])

        # Check if CoM is inside support polygon
        if self.point_in_polygon(com_2d, support_polygon):
            # Calculate distance to closest edge
            min_dist = float('inf')
            for i in range(len(support_polygon)):
                edge_start = support_polygon[i]
                edge_end = support_polygon[(i + 1) % len(support_polygon)]
                dist = self.distance_to_line_segment(com_2d, edge_start, edge_end)
                min_dist = min(min_dist, dist)
            return min_dist
        else:
            # CoM is outside support polygon - unstable
            return -self.distance_to_polygon(com_2d, support_polygon)

    def point_in_polygon(self, point, polygon):
        """
        Check if point is inside polygon using ray casting algorithm
        """
        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside
```

### Linear Inverted Pendulum Model (LIPM)

The Linear Inverted Pendulum Model is a simplified representation of bipedal walking:

```python
class LIPMController:
    def __init__(self, height, gravity=9.81):
        self.height = height
        self.omega = np.sqrt(gravity / height)

    def compute_capture_point(self, com_pos, com_vel):
        """
        Compute the capture point where the robot must step to come to a stop
        """
        capture_point = com_pos + com_vel / self.omega
        return capture_point

    def plan_step_location(self, current_com_pos, current_com_vel, support_foot_pos):
        """
        Plan where to place the next step based on current state
        """
        capture_point = self.compute_capture_point(current_com_pos[:2], current_com_vel[:2])

        # Step toward capture point but within reasonable limits
        step_pos = capture_point

        # Limit step size based on robot capabilities
        max_step_dist = 0.3  # meters
        step_vector = step_pos - support_foot_pos[:2]
        step_dist = np.linalg.norm(step_vector)

        if step_dist > max_step_dist:
            step_pos = support_foot_pos[:2] + (step_vector / step_dist) * max_step_dist

        return step_pos
```

### Feedback Control for Balance

```python
class FeedbackBalanceController:
    def __init__(self, kp_com=10.0, ki_com=1.0, kd_com=5.0):
        self.kp_com = kp_com  # Proportional gain for CoM control
        self.ki_com = ki_com  # Integral gain for CoM control
        self.kd_com = kd_com  # Derivative gain for CoM control
        self.com_error_integral = np.zeros(2)
        self.com_error_prev = np.zeros(2)

    def compute_balance_correction(self, desired_com, actual_com, desired_com_vel, actual_com_vel, dt):
        """
        Compute balance correction based on CoM feedback
        """
        # Calculate errors
        com_pos_error = desired_com - actual_com
        com_vel_error = desired_com_vel - actual_com_vel

        # Update integral term
        self.com_error_integral += com_pos_error * dt

        # Calculate derivative term
        com_error_derivative = (com_pos_error - self.com_error_prev) / dt if dt > 0 else np.zeros(2)
        self.com_error_prev = com_pos_error

        # PID control
        correction = (self.kp_com * com_pos_error +
                     self.ki_com * self.com_error_integral +
                     self.kd_com * com_vel_error)

        return correction
```

## Walking Pattern Generation

### Preview Control Method

The preview control method uses future ZMP reference values to compute stable CoM trajectories:

```python
class PreviewController:
    def __init__(self, robot_height, control_dt, preview_time):
        self.omega = np.sqrt(9.81 / robot_height)
        self.dt = control_dt
        self.preview_steps = int(preview_time / control_dt)

    def compute_com_trajectory(self, zmp_reference):
        """
        Compute CoM trajectory using preview control
        """
        # This is a simplified implementation
        # In practice, this involves solving Riccati equations
        com_trajectory = []
        com_pos = np.array([0.0, 0.0])  # Initial CoM position
        com_vel = np.array([0.0, 0.0])  # Initial CoM velocity

        for i in range(len(zmp_reference)):
            # Simple feedback + preview control
            zmp_current = zmp_reference[i]
            com_acc = self.omega**2 * (com_pos - zmp_current)

            # Integrate to get velocity and position
            com_vel += com_acc * self.dt
            com_pos += com_vel * self.dt

            com_trajectory.append(com_pos.copy())

        return np.array(com_trajectory)
```

## Dynamic Walking Strategies

### Capture Point Based Walking

```python
class CapturePointWalker:
    def __init__(self, robot_height, max_foot_shift=0.2):
        self.omega = np.sqrt(9.81 / robot_height)
        self.max_foot_shift = max_foot_shift

    def compute_next_foot_position(self, current_com_pos, current_com_vel):
        """
        Compute next foot position based on capture point
        """
        # Calculate capture point
        capture_point = current_com_pos + current_com_vel / self.omega

        # Determine which foot will be the next support foot
        # This is a simplified version - in practice, you'd track stance/swing feet
        next_foot_pos = capture_point

        # Limit foot placement to robot capabilities
        next_foot_pos = np.clip(next_foot_pos,
                               current_com_pos - self.max_foot_shift,
                               current_com_pos + self.max_foot_shift)

        return next_foot_pos
```

## Real-World Implementation Considerations

### Sensor Fusion for Balance

Humanoid robots use multiple sensors for balance control:

```python
import numpy as np
from scipy.spatial.transform import Rotation as R

class SensorFusionBalancer:
    def __init__(self):
        self.imu_orientation = np.eye(3)
        self.imu_angular_velocity = np.zeros(3)
        self.foot_pressure_sensors = {'left': [0, 0, 0, 0], 'right': [0, 0, 0, 0]}
        self.accelerometer = np.zeros(3)

    def estimate_robot_state(self):
        """
        Estimate robot state (CoM position, velocity, orientation) from sensor data
        """
        # Fuse IMU, pressure sensors, and other data
        # This is a simplified representation
        estimated_state = {
            'com_position': self.estimate_com_position(),
            'com_velocity': self.estimate_com_velocity(),
            'orientation': self.estimate_orientation(),
            'angular_velocity': self.estimate_angular_velocity()
        }
        return estimated_state

    def estimate_com_position(self):
        """
        Estimate CoM position using sensor fusion
        """
        # Combine encoder data with IMU data
        # In practice, this would use a Kalman filter or similar
        pass

    def estimate_orientation(self):
        """
        Estimate global orientation using IMU and gravity vector
        """
        # Use complementary filter or extended Kalman filter
        pass
```

## Walking Stabilization

### Hip Strategy and Ankle Strategy

Humanoid robots use different strategies to maintain balance:

```python
class WalkingStabilizer:
    def __init__(self, robot):
        self.robot = robot

    def apply_ankle_strategy(self, roll_error, pitch_error):
        """
        Apply ankle strategy for small disturbances
        """
        # Small adjustments by tilting feet
        ankle_roll_correction = np.clip(roll_error * 0.5, -0.1, 0.1)
        ankle_pitch_correction = np.clip(pitch_error * 0.5, -0.1, 0.1)

        return ankle_roll_correction, ankle_pitch_correction

    def apply_hip_strategy(self, lateral_error):
        """
        Apply hip strategy for larger lateral disturbances
        """
        # Move hip to shift CoM
        hip_lateral_correction = np.clip(lateral_error * 0.3, -0.05, 0.05)

        return hip_lateral_correction

    def apply_stepping_strategy(self, capture_point):
        """
        Apply stepping strategy when other methods are insufficient
        """
        # Plan an emergency step to the capture point
        step_location = capture_point
        return step_location
```

## Exercises

1. Implement a simple ZMP-based walking pattern generator and test it with different step parameters
2. Simulate the Linear Inverted Pendulum Model and observe how different CoM heights affect stability
3. Design a capture point controller and test it with various initial conditions
4. Research and implement a simple preview controller for CoM trajectory generation
5. Explore how sensor noise affects balance control performance
6. Design a finite state machine for different walking phases (start, steady, stop)

## Summary

Humanoid locomotion combines complex control theory with biomechanics to achieve stable bipedal walking. The key challenges include maintaining balance during single support phases, generating stable walking patterns, and adapting to disturbances. Modern approaches combine ZMP-based pattern generation with feedback control and sensor fusion to achieve robust walking performance. Understanding these principles is essential for developing effective humanoid locomotion systems.