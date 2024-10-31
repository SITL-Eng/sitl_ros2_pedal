import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'sitl_ros2_pedal'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.xml')),
    ],
    install_requires=[
        'setuptools',
        'sitl_ros2_interfaces',
    ],
    zip_safe=True,
    maintainer='sitl-dvrk-sub',
    maintainer_email='sktlgt93@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
        ],
    },
)
