"""Launch the pirouetting demo

   ros2 launch JIB pirouette.launch.py

   This launch file is intended as an example of how to spin an
   ungrounded robot (humanoid).

   This should start
     1) RVIZ, ready to view the robot
     2) The robot_state_publisher to broadcast the robot model
     3) The GUI to determine the joints.
     4) The pirouette example code

"""

import os

from ament_index_python.packages import get_package_share_directory as pkgdir

from launch                      import LaunchDescription
from launch.actions              import Shutdown
from launch_ros.actions          import Node


#
# Generate the Launch Description
#
def generate_launch_description():

    ######################################################################
    # LOCATE FILES

    # Locate the RVIZ configuration file.
    rvizcfg = os.path.join(pkgdir('JIB'), 'rviz/viewurdf.rviz')

    # Locate the URDF file.
    urdf = os.path.join(pkgdir('JIB'), 'urdf/atlas_v5.urdf')

    # Load the robot's URDF file (XML).
    with open(urdf, 'r') as file:
        robot_description = file.read()


    ######################################################################
    # PREPARE THE LAUNCH ELEMENTS

    # Configure a node for the robot_state_publisher.
    node_robot_state_publisher = Node(
        name       = 'robot_state_publisher', 
        package    = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        output     = 'screen',
        parameters = [{'robot_description': robot_description}])

    # Configure a node for RVIZ.
    node_rviz = Node(
        name       = 'rviz', 
        package    = 'rviz2',
        executable = 'rviz2',
        output     = 'screen',
        arguments  = ['-d', rvizcfg],
        on_exit    = Shutdown())

    # Configure a node for the GUI.
    node_gui = Node(
        name       = 'gui', 
        package    = 'joint_state_publisher_gui',
        executable = 'joint_state_publisher_gui',
        output     = 'screen',
        on_exit    = Shutdown())

    # Configure a node for the pirouette demo.
    node_pirouette = Node(
        name       = 'pirouette',
        package    = 'JIB',
        executable = 'pirouette',
        output     = 'screen')


    ######################################################################
    # RETURN THE ELEMENTS IN ONE LIST

    return LaunchDescription([
        # Start the robot_state_publisher, RVIZ, the GUI, and the demo.
        node_robot_state_publisher,
        node_rviz,
        node_gui,
        node_pirouette,
    ])
