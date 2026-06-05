# sitl_ros2_pedal

**da Vinci console pedal & Electrosurgical Unit (ESU) control in ROS 2**, developed by the
[Surgical Innovation and Training Lab (SITL)](https://sitl.us/) at the University of Illinois Chicago.

This package bridges the da Vinci surgeon-console **monopolar foot pedal** and the **electrosurgical
unit (ESU)** to ROS 2 through a small Arduino interface. It works in two directions:

- **Read** the surgeon's monopolar pedal presses and publish them as timestamped ROS 2 messages
  (used, for example, to record pedal signals in the [CRCD dataset](https://github.com/SITL-Eng/CRCD)).
- **Write** / actuate the ESU monopolar energy **programmatically** from a ROS 2 topic, so that an
  autonomous controller can deliver cautery energy during robotic dissection.

> Part of the SITL dVRK ROS 2 platform behind *Towards Autonomous Robot-Assisted Surgery*.
> See the project overview: **https://koh43.github.io/robotic-cholecystectomy/**

---

## How it works

An Arduino is wired to the monopolar pedal / ESU trigger circuit (a MOSFET-driven switch in parallel
with the physical foot pedal). The ROS 2 nodes talk to the Arduino over a USB serial connection
(default `/dev/ttyACM1` at `57600` baud) using a tiny single-character protocol:

| Direction | Byte | Meaning |
|-----------|:----:|---------|
| Host → Arduino | `R` | Request the current monopolar pedal state |
| Arduino → Host | `1` / `0` | Pedal pressed / released |
| Host → Arduino | `H` | Activate monopolar energy (ESU **ON**) |
| Host → Arduino | `L` | Deactivate monopolar energy (ESU **OFF**) |

The matching Arduino firmware (not included here) simply implements this `R` / `H` / `L` protocol and
drives the switching circuit.

## Nodes and topics

| Executable | Role | Topic | Type | I/O |
|------------|------|-------|------|-----|
| `pub_pedal_mp_r` | Polls the Arduino at a fixed rate (default 100 Hz) and publishes the pedal state | `/pedal/monopolar/read` | `sitl_ros2_interfaces/BoolStamped` | publishes |
| `sub_pedal_mp_w` | Subscribes to energy commands and switches the ESU on/off via the Arduino | `/pedal/monopolar/write` | `sitl_ros2_interfaces/BoolStamped` | subscribes |
| `pub_pedal_mp_w_test` | Test publisher that toggles the write command on/off (bench testing) | `/pedal/monopolar/write` | `sitl_ros2_interfaces/BoolStamped` | publishes |

`mp` stands for **monopolar**. All messages are timestamped so pedal activity can be synchronized with
endoscopic video and robot kinematics.

---

## Dependencies

- [ROS 2 Humble](https://docs.ros.org/en/humble/Installation.html) (`rclpy`)
- [`sitl_ros2_interfaces`](https://github.com/SITL-Eng/sitl_ros2_interfaces) — provides `BoolStamped`
- Python: [`pyserial`](https://pyserial.readthedocs.io/) — `pip install pyserial`
- An Arduino (or compatible MCU) running firmware that implements the `R` / `H` / `L` serial protocol,
  wired to the monopolar pedal / ESU trigger circuit

## Installation

```bash
cd ~/ros2_ws/src
git clone https://github.com/SITL-Eng/sitl_ros2_interfaces.git   # required messages
git clone https://github.com/SITL-Eng/sitl_ros2_pedal.git
cd ~/ros2_ws
colcon build --packages-select sitl_ros2_interfaces sitl_ros2_pedal
source install/setup.bash
```

Make sure your user can access the serial device (otherwise you may need to grant permissions):

```bash
sudo usermod -aG dialout $USER   # then log out / back in
ls -l /dev/ttyACM*               # confirm the Arduino device path
```

## Configuration

Serial port, baud rate, and polling frequency are set in the entry-point scripts under
`sitl_ros2_pedal/` (`pub_pedal_mp_r.py`, `sub_pedal_mp_w.py`, `pub_pedal_mp_w_test.py`):

```python
params = {
    "node_name"  : "pub_pedal_mp_read",
    "queue_size" : 5,
    "port"       : "/dev/ttyACM1",   # <-- set to your Arduino device
    "baud"       : 57600,
    "hz"         : 100,
}
```

## Usage

Launch the read and write nodes together:

```bash
ros2 launch sitl_ros2_pedal pedal_mp_base.xml
```

Or run nodes individually:

```bash
# Read the surgeon's monopolar pedal and publish it
ros2 run sitl_ros2_pedal pub_pedal_mp_r
ros2 topic echo /pedal/monopolar/read

# Command the ESU on/off from ROS 2 (autonomous energy delivery)
ros2 run sitl_ros2_pedal sub_pedal_mp_w
ros2 topic pub --once /pedal/monopolar/write sitl_ros2_interfaces/msg/BoolStamped "{data: true}"

# Bench test the write path without a controller
ros2 run sitl_ros2_pedal pub_pedal_mp_w_test
```

## Repository structure

```
sitl_ros2_pedal/
├── launch/
│   └── pedal_mp_base.xml          # launches pub_pedal_mp_r + sub_pedal_mp_w
├── nodes/                         # node implementations (rclpy Node classes)
│   ├── pub_pedal_mp_r.py          # read pedal state -> /pedal/monopolar/read
│   ├── sub_pedal_mp_w.py          # /pedal/monopolar/write -> Arduino (ESU on/off)
│   └── pub_pedal_mp_w_test.py     # test toggler for the write path
├── sitl_ros2_pedal/               # console_scripts entry points (params + main)
├── utils/
│   └── ros2_utils.py              # QoS profile, timestamp, logging helpers
├── package.xml
└── setup.py
```

---

## ⚠️ Safety

This package **switches a real electrosurgical unit**, which delivers high-frequency electrical energy
capable of cutting and coagulating tissue and of causing burns or fire.

- **Research use only.** Not a medical device; not for use on humans.
- Always test on the bench (e.g., with an LED/relay in place of the ESU) before connecting to an ESU.
- Keep a hardware interlock and an accessible physical kill switch in the loop at all times.
- Validate the wiring and Arduino firmware independently before enabling energy delivery.

## Related repositories

- [`sitl_ros2_interfaces`](https://github.com/SITL-Eng/sitl_ros2_interfaces) — shared custom messages (required)
- [`sitl_ros2_cv`](https://github.com/SITL-Eng/sitl_ros2_cv) — real-time surgical computer vision
- [`sitl_ros2_dvrk`](https://github.com/SITL-Eng/sitl_ros2_dvrk) — da Vinci Research Kit control
- [`CRCD`](https://github.com/SITL-Eng/CRCD) — the Comprehensive Robotic Cholecystectomy Dataset (records pedal signals)

## License

Released under the [MIT License](LICENSE).

## Citation

If you use this package, please cite the works it supports:

```bibtex
@INPROCEEDINGS{oh2025autonomous,
  author={Oh, Ki-Hwan and Borgioli, Leonardo and Žefran, Miloš and Valle, Valentina and Giulianotti, Pier Cristoforo},
  booktitle={2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  title={Autonomous Dissection in Robotic Cholecystectomy},
  year={2025},
  pages={11240-11246},
  doi={10.1109/IROS60139.2025.11246364}
}

@INPROCEEDINGS{oh2024crcd,
  author={Oh, Ki-Hwan and Borgioli, Leonardo and Mangano, Alberto and Valle, Valentina and Di Pangrazio, Marco and Toti, Francesco and Pozza, Gioia and Ambrosini, Luciano and Ducas, Alvaro and Žefran, Miloš and Chen, Liaohai and Giulianotti, Pier Cristoforo},
  booktitle={2024 International Symposium on Medical Robotics (ISMR)},
  title={Comprehensive Robotic Cholecystectomy Dataset (CRCD): Integrating Kinematics, Pedal Signals, and Endoscopic Videos},
  year={2024},
  pages={1-7},
  doi={10.1109/ISMR63436.2024.10585836}
}
```

## Disclaimer

This software is for research purposes only and is not intended for clinical use without proper
validation and regulatory approval.
