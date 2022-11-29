%% Import Data
QoEdata = readmatrix("QoEcsv_2022-11-27_23-01-13.csv");

%% Plot Data

% Start at a later value since first row is
startVal = 500;

figure(1);
clf(1);
hold on;
plot(QoEdata(startVal:end,1),QoEdata(startVal:end,2),'LineWidth',2);
plot(QoEdata(startVal:end,1),QoEdata(startVal:end,3),'LineWidth',2);
plot(QoEdata(startVal:end,1),QoEdata(startVal:end,4),'LineWidth',2);
plot(QoEdata(startVal:end,1),QoEdata(startVal:end,5),'LineWidth',2);
title('Quality of Experience vs Time');
xlabel('Time');
ylabel('QoE');
legend("High Throughput Buffered Video","Low Throughput Buffered Video",...
    "High Throughput Unbuffered Video","Low Throughput Unbuffered Video",...
    'Location','southeast');
grid minor;
hold off;