# butterknife 
> A Network-Slicing System for Software-Defined Mobile Networks


## File structure (only source code shown)
- butter
    - butter
        - client.py
        - server.py
        - manifest.py
        - plot.py
    
- handle
    - handler
        - multiplex_zmq.py
        - rl_interface.py
        
    - srsRAN (submodule)
    
        - config 
    
            *(This is the configuration files used for testing)*
    
        - ```
          lib/srsenb/src/stack/mac/schedulers/sched_ext_prio.cc 
          ```
    
            *(Modification made in srsRAN for our project)*
    
- slicer
    - slicer
        - network_slicing_application_simulation.py
        - network_slicing_application.py
        - client_simulation.py
        - DQN.py
        - Environment.py
    
- toast
    - toast
        - __init__.py
        - client.py
        - main.py
        - server.py

## Run Procedures
To run the server:

```
python3 ./butter/butter/server.py
```
To run the unbuffer client:
```
python3 ./butter/butter/client.py --ip <ip address> --ft <frame time> --rt <recovery time> --bs <buffer size> --unbuffer --id <id>
```
To run the buffer client:
```
python3 ./butter/butter/client.py --ip <ip address> --ft <frame time> --rt <recovery time> --bs <buffer size> --buffer --id <id>
```

Default value of parameter for client:

--ip: "local host"

--ft: "0.016"

--rt: "0.016"

--bs: "500"

--buffer/--unbuffer

--id: "70"

UE configurations:
|   |Buffer|Unbuffer|
|---|---|---|
|High throughput| Buffer size: 500, frame time = 0.008 | Buffer size: 1, frame time = 0.008 |
|Low throughput| Buffer size: 500, frame time = 0.032 | Buffer size: 1, frame time = 0.032 |

To run the network slicing application (reinforcement learning model):
```
python3 ./slicer/slicer/network_slicing_application.py
```

To run the network slicing model simulation (reinforcement learning model):
```
python3 ./slicer/slicer/network_slicing_application_sim.py
```

To run the scheduler interface:
```
python3 ./handle/handle/rl_interface.py
```
