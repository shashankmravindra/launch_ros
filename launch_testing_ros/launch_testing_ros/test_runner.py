# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module for a ROS aware LaunchTestRunner."""

import launch
import launch_testing.test_runner


class LaunchTestRunner(launch_testing.test_runner.LaunchTestRunner):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import rclpy  # Import on first use to avoid races at module level
        self._rclpy_context = rclpy.context.Context()
        rclpy.init(args=self._launch_file_arguments, context=self._rclpy_context)

    def generate_preamble(self):
        import launch_ros  # Import on first use to avoid races at module level
        return [launch.actions.IncludeLaunchDescription(
            launch_description_source=launch.LaunchDescriptionSource(
                launch_description=launch_ros.get_default_launch_description(
                    rclpy_context=self._rclpy_context,
                )
            )
        )]
