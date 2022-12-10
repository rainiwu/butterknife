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
    - srsRAN
- slicer
    - slicer
        - Application_simulation.py
        - Application.py
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

To run the network slicing model:
```
python3 ./slicer/slicer/Application.py
```

To run the scheduler interface:
```
python3 ./handle/handle/rl_interface.py
```
