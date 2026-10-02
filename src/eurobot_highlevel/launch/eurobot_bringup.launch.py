import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 1. Localisation Relative (EKF Node)
    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[os.path.join(get_package_share_directory('eurobot_highlevel'), 'config', 'ekf.yaml')]
    )

    # 2. SLAM LiDAR (Slam Toolbox)
    slam_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[{'use_sim_time': False}]
    )

    # 3. Hardware Bridge (Dummy Node for STM32)
    stm32_bridge = Node(
        package='eurobot_highlevel',
        executable='stm32_bridge',
        name='stm32_bridge_node',
        output='screen'
    )

    return LaunchDescription([
        stm32_bridge,
        ekf_node,
        slam_node
    ])