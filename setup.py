import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'sitl_ros2_pedal'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.xml')),
    ],
    install_requires=[
        'setuptools',
    ],
    zip_safe=True,
    maintainer='sitl-dvrk-sub',
    maintainer_email='sktlgt93@gmail.com',
    description='SITL ROS2 Package for Electrosurgical Unit Control',
    license='MIT',
    entry_points={
        'console_scripts': [
            'pub_pedal_mp_r      = sitl_ros2_pedal.pub_pedal_mp_r:main',
            'sub_pedal_mp_w      = sitl_ros2_pedal.sub_pedal_mp_w:main',
            'pub_pedal_mp_w_test = sitl_ros2_pedal.pub_pedal_mp_w_test:main',
        ],
    },
)
