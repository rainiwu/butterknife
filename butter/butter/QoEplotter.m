%% Import Data
QoEdata = readmatrix("QoEcsv_2022-11-27_23-01-13.csv");

%% Plot Data

startVal = 500;

figure(1);
clf(1);
hold on;
plot(QoEdata(startVal:end,1),QoEdata(startVal:end,2),'LineWidth',2);
plot(QoEdata(startVal:end,1),QoEdata(startVal:end,3),'LineWidth',2);
plot(QoEdata(startVal:end,1),QoEdata(startVal:end,4),'LineWidth',2);
plot(QoEdata(startVal:end,1),QoEdata(startVal:end,5),'LineWidth',2);
title('QoE Metrics');
xlabel('Time');
ylabel('QoE');
legend("70","71","72","73");
grid minor;
hold off;