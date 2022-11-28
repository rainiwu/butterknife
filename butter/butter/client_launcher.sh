# 
#    Client Launcher 
# 

# Bash script to launch clients as desired. 

# High Throughput Buffered Video (High Throughput, High Latency)
# Large buffer size, multiple frames per chunk, high framerate (60FPS).
python3 client_buf.py --ip localhost --ft 0.008 --rt 0.008 --bs 500 --ub False --id 70 &

sleep 1

# Low Throughput Buffered Video (Low Throughput, High Latency)
# Large buffer size, multiple frames per chunk, low framerate (30FPS).
python3 client_buf.py --ip localhost --ft 0.016 --rt 0.016 --bs 500 --ub False --id 71 &

sleep 1

# High Throughput Unbuffered Video (High Throughput, Low Latency)
# 1 frame buffer, 1 frame per chunk, high framerate (60FPS).
python3 client_buf.py --ip localhost --ft 0.008 --rt 0.008 --bs 1 --ub False --id 72 &

sleep 1

# Low Throughput Unbuffered Video (Low Throughput, Low Latency)
# 1 frame buffer, 1 frame per chunk, low framerate (30FPS). 
python3 client_buf.py --ip localhost --ft 0.016 --rt 0.016 --bs 1 --ub False --id 73

sleep 1

trap '' EXIT