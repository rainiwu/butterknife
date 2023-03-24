# butterknife

> A network-slicing system for software-defined mobile networks

`butterknife` is a proof-of-concept system that can prioritize particular user
connections over software-defined mobile networks.
Using a modified scheduler integrated into a fork of `srsRAN`, we simulate
a full end-to-end LTE connection, including both a software-defined base-station,
and software-defined user equipment.

This project was developed as the final project for ECE 257A at University of California, San Diego.

## File structure

- `butter/` - A network usage simulator, simulating various dynamic video streaming applications. Also provides a notion of
  quality of experience of the various applications through a Python interface.
- `handle/` - Provides a fork of srsRAN, including a modified scheduler that can take external priorities for individual users, and Python interfaces
  for modifying scheduler behavior.
- `slicer/` - A reinforcement-learning based application for intelligent prioritization of users based on application
  information.
- `toast/` - A virtual tunnel interface, used for simulating srsRAN behaviors. Currently not in use.

## Usage

The following section details how to run `butterknife`.
First, `butterknife` uses `poetry` for dependency management.
Please utilize an up-to-date version of `poetry`.

Each individual folder within this repository is set up as a separate `poetry` project.
Additionally, the srsRAN and srsUE fork in `handle` needs to be built and started.
Please refer to the srsRAN documentation for details on that process.
To run the full `butterknife` system, each project needs to be run separately.
The order in which to run the projects are:

1. Start the srsRAN fork and the srsUE.

2. Start `butter` server

3. Start `butter` client with the appropriate settings.

4. Start `slicer`.

5. Start the python interface in `handle`.

### Application notes

The following section provides an overview on how to accomplish the tasks listed above.
Note that only a single `butter` client needs to be started.
Additionally, the `slicer` simulator need only be run when desired.

To run the server:

```
poetry run python ./butter/butter/server.py
```

To run the unbuffer client:

```
poetry run python ./butter/butter/client.py --ip <ip address> --ft <frame time> --rt <recovery time> --bs <buffer size> --unbuffer --id <id>
```

To run the buffer client:

```
poetry run python ./butter/butter/client.py --ip <ip address> --ft <frame time> --rt <recovery time> --bs <buffer size> --buffer --id <id>
```

Default value of parameter for client:

--ip: "local host"

--ft: "0.016"

--rt: "0.016"

--bs: "500"

--buffer/--unbuffer

--id: "70"

UE configurations:
| |Buffer|Unbuffer|
|---|---|---|
|High throughput| Buffer size: 500, frame time = 0.008 | Buffer size: 1, frame time = 0.008 |
|Low throughput| Buffer size: 500, frame time = 0.032 | Buffer size: 1, frame time = 0.032 |

To run the network slicing application (reinforcement learning model):

```
poetry run python ./slicer/slicer/network_slicing_application.py
```

To run the network slicing model simulation (reinforcement learning model):

```
poetry run python ./slicer/slicer/network_slicing_application_sim.py
```

To run the scheduler interface:

```
poetry run python ./handle/handle/rl_interface.py
```

## Contact us!

If you have any questions or concerns about this project, feel free to contact us!
