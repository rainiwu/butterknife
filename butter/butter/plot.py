import matplotlib as plt
import numpy as np

def plot(csvName, start_val = 500):
    data = np.genfromtxt(csvName, delimiter=",")

    x = data[start_val:, 0]
    y1 = data[start_val:, 1]
    y2 = data[start_val:, 2]
    y3 = data[start_val:, 3]
    y4 = data[start_val:, 4]

    plt.figure(1)
    plt.clf()
    plt.hold(True)
    plt.plot(x, y1, 'LineWidth', 2)
    plt.plot(x, y2, 'LineWidth', 2)
    plt.plot(x, y3, 'LineWidth', 2)
    plt.plot(x, y4, 'LineWidth', 2)
    plt.title('Quality of Experience vs Time')
    plt.xlabel('Time')
    plt.ylabel('QoE')
    plt.legend("High Throughput Buffered Video", "Low Throughput Buffered Video",
            "High Throughput Unbuffered Video", "Low Throughput Unbuffered Video",
            loc='southeast')
    plt.grid(True, which='minor')
    plt.hold(False)
    plt.savefig('QoE_Graph.png')

