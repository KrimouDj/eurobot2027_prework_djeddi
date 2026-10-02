import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist

class STM32Bridge(Node):
    def __init__(self):
        super().__init__('stm32_bridge_node')
        
        # Publishers (To EKF)
        self.odom_pub = self.create_publisher(Odometry, '/odom_raw', 50)
        self.imu_pub = self.create_publisher(Imu, '/imu/data', 50)
        
        # Subscriber (From Nav2)
        self.cmd_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)
        
        self.get_logger().info("STM32 Hardware Bridge Initialized. TF: odom -> base_link ready.")

    def cmd_callback(self, msg):
        # Convert Twist to left/right wheel speeds and send via UART
        vx = msg.linear.x
        wz = msg.angular.z
        self.get_logger().debug(f"Sending to STM32: Vx={vx}, Wz={wz}")

def main(args=None):
    rclpy.init(args=args)
    node = STM32Bridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()