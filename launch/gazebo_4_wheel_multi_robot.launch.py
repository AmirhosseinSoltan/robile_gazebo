#!/usr/bin/env python3
# Authors: Deebul Nair

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription, LaunchContext
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.descriptions import ParameterValue

def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    
    world = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'worlds',
        'turtlebot3_house.world'
    )

    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    robile = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('robile_gazebo'), 'launch'),
         '/gazebo_4_wheel_multi.launch.py'])
      )
    
    robile_namespaced = GroupAction(
        actions=[
            PushRosNamespace('robile0'),
            robile,
    ])

    rviz_cmd = Node(package='rviz2',
                    # namespace='',
                    executable='rviz2',
                    name='rviz2',
                    output='screen',
                    )

    return LaunchDescription([
        rviz_cmd,
        gzclient_cmd,
        gzserver_cmd,
        robile_namespaced
    ])