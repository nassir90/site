#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2
import time
import json
import os

class PointCloudRecorder(Node):
    def __init__(self):
        super().__init__('pointcloud_recorder')
        self.subscription = self.create_subscription(
            PointCloud2,
            '/yrl_cloud',  # change topic as needed
            self.listener_callback,
            10
        )
        self.points = []
        self.start_time = time.time()
        self.duration = 20.0  # seconds
        self.output_file = os.path.expanduser("pointcloud_capture.json")

    def listener_callback(self, msg):
        if time.time() - self.start_time > self.duration:
            # Stop listening and dump data
            self.subscription.destroy()
            self.dump_to_file()
            self.get_logger().info(f"Point cloud data saved to {self.output_file}")
            rclpy.shutdown()
            return

        # Convert PointCloud2 to a list of tuples (x, y, z)
        for point in pc2.read_points(msg, field_names=('x', 'y', 'z'), skip_nans=True):
            self.points.append(point)

    def dump_to_file(self):
        # Convert to JSON for simple loading in JSA
        data = [{"x": p[0].item(), "y": p[1].item(), "z": p[2].item()} for p in self.points]
        with open(self.output_file, 'w') as f:
            json.dump(data, f)


def main(args=None):
    rclpy.init(args=args)
    node = PointCloudRecorder()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
