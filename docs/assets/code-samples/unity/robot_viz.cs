using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Robotics.Simulation
{
    /// <summary>
    /// Robot Visualization Controller for Unity
    /// Handles the visualization and animation of a robot in Unity 3D
    /// </summary>
    public class RobotViz : MonoBehaviour
    {
        [Header("Robot Configuration")]
        public float moveSpeed = 5.0f;
        public float rotationSpeed = 100.0f;

        [Header("Joint References")]
        public Transform leftWheel;
        public Transform rightWheel;
        public Transform head;

        [Header("Sensor Visualization")]
        public GameObject laserScanner;
        public LineRenderer laserBeam;

        private Rigidbody rb;
        private Vector3 targetPosition;
        private Quaternion targetRotation;

        // Robot state variables
        private float wheelRadius = 0.1f;
        private float wheelSeparation = 0.3f;
        private float leftWheelVelocity = 0f;
        private float rightWheelVelocity = 0f;

        void Start()
        {
            rb = GetComponent<Rigidbody>();
            targetPosition = transform.position;
            targetRotation = transform.rotation;

            // Initialize laser visualization if available
            if (laserScanner != null && laserBeam == null)
            {
                laserBeam = laserScanner.GetComponent<LineRenderer>();
                if (laserBeam == null)
                {
                    laserBeam = laserScanner.gameObject.AddComponent<LineRenderer>();
                    laserBeam.material = new Material(Shader.Find("Sprites/Default"));
                    laserBeam.startWidth = 0.05f;
                    laserBeam.endWidth = 0.01f;
                    laserBeam.startColor = Color.red;
                    laserBeam.endColor = Color.clear;
                }
            }
        }

        void Update()
        {
            // Update wheel rotations based on velocities
            UpdateWheelRotations();

            // Update head rotation for sensor scanning
            UpdateHeadRotation();

            // Visualize laser scanner
            UpdateLaserVisualization();
        }

        /// <summary>
        /// Updates the rotation of wheels based on their velocities
        /// </summary>
        private void UpdateWheelRotations()
        {
            if (leftWheel != null)
            {
                float rotationAngle = (leftWheelVelocity * Time.deltaTime) / wheelRadius * Mathf.Rad2Deg;
                leftWheel.Rotate(Vector3.right, rotationAngle);
            }

            if (rightWheel != null)
            {
                float rotationAngle = (rightWheelVelocity * Time.deltaTime) / wheelRadius * Mathf.Rad2Deg;
                rightWheel.Rotate(Vector3.right, rotationAngle);
            }
        }

        /// <summary>
        /// Updates head rotation for scanning behavior
        /// </summary>
        private void UpdateHeadRotation()
        {
            if (head != null)
            {
                // Simple scanning motion
                float headRotation = Mathf.Sin(Time.time * 2f) * 30f; // ±30 degrees
                head.localRotation = Quaternion.Euler(0, headRotation, 0);
            }
        }

        /// <summary>
        /// Visualizes the laser scanner beam
        /// </summary>
        private void UpdateLaserVisualization()
        {
            if (laserScanner != null && laserBeam != null)
            {
                Vector3 startPos = laserScanner.transform.position;
                Vector3 direction = laserScanner.transform.forward;

                // Raycast to detect obstacles
                if (Physics.Raycast(startPos, direction, out RaycastHit hit, 10f))
                {
                    laserBeam.SetPosition(0, startPos);
                    laserBeam.SetPosition(1, hit.point);
                    laserBeam.enabled = true;
                }
                else
                {
                    laserBeam.SetPosition(0, startPos);
                    laserBeam.SetPosition(1, startPos + direction * 10f);
                    laserBeam.enabled = true;
                }
            }
        }

        /// <summary>
        /// Sets robot wheel velocities (simulating ROS cmd_vel)
        /// </summary>
        /// <param name="linearVelocity">Forward/backward velocity</param>
        /// <param name="angularVelocity">Rotational velocity</param>
        public void SetRobotVelocity(float linearVelocity, float angularVelocity)
        {
            // Convert differential drive velocities
            float leftVel = linearVelocity - (angularVelocity * wheelSeparation / 2.0f);
            float rightVel = linearVelocity + (angularVelocity * wheelSeparation / 2.0f);

            leftWheelVelocity = leftVel;
            rightWheelVelocity = rightVel;

            // Apply movement to the robot body
            transform.Translate(Vector3.forward * linearVelocity * Time.deltaTime);
            transform.Rotate(Vector3.up, angularVelocity * Time.deltaTime * Mathf.Rad2Deg);
        }

        /// <summary>
        /// Simulates a ROS topic subscriber for velocity commands
        /// </summary>
        public void VelocityCommandCallback(float linearX, float angularZ)
        {
            SetRobotVelocity(linearX, angularZ);
        }

        /// <summary>
        /// Gets simulated sensor data
        /// </summary>
        /// <returns>Dictionary containing sensor readings</returns>
        public Dictionary<string, float> GetSensorData()
        {
            Dictionary<string, float> sensorData = new Dictionary<string, float>();

            // Simulate various sensor readings
            sensorData["battery_level"] = Random.Range(80f, 100f);
            sensorData["temperature"] = Random.Range(25f, 35f);

            // Simulate distance to obstacle using raycast
            if (laserScanner != null)
            {
                if (Physics.Raycast(laserScanner.transform.position, laserScanner.transform.forward, out RaycastHit hit, 10f))
                {
                    sensorData["distance_to_obstacle"] = hit.distance;
                }
                else
                {
                    sensorData["distance_to_obstacle"] = 10f; // Max range
                }
            }

            return sensorData;
        }

        /// <summary>
        /// Resets the robot to initial position and state
        /// </summary>
        public void ResetRobot()
        {
            transform.position = Vector3.zero;
            transform.rotation = Quaternion.identity;
            leftWheelVelocity = 0f;
            rightWheelVelocity = 0f;
        }

        // Example usage in Unity's OnValidate for editor feedback
        private void OnValidate()
        {
            if (moveSpeed < 0) moveSpeed = 0;
            if (rotationSpeed < 0) rotationSpeed = 0;
        }
    }

    /// <summary>
    /// Robot Controller for demonstration purposes
    /// Shows how to use the RobotViz component
    /// </summary>
    public class RobotController : MonoBehaviour
    {
        public RobotViz robotViz;

        void Start()
        {
            if (robotViz == null)
            {
                robotViz = GetComponent<RobotViz>();
            }
        }

        void Update()
        {
            // Example: Send velocity commands based on input
            float linear = Input.GetAxis("Vertical"); // W/S or Up/Down arrows
            float angular = Input.GetAxis("Horizontal"); // A/D or Left/Right arrows

            if (robotViz != null)
            {
                robotViz.VelocityCommandCallback(linear * 2.0f, angular * 1.5f);
            }
        }
    }
}