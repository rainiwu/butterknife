%% Import Data
QoEdata_RR1 = readmatrix("data/test1.csv");
QoEdata_RR2 = readmatrix("data/test2.csv");
QoEdata_RR3 = readmatrix("data/test3.csv");
QoEdata_RR4 = readmatrix("data/test4.csv");
QoEdata_RR5 = readmatrix("data/test5.csv");
QoEdata_RL1 = readmatrix("data/test6.csv");
QoEdata_RL2 = readmatrix("data/test7.csv");
QoEdata_RL3 = readmatrix("data/test8.csv");
QoEdata_RL4 = readmatrix("data/test9.csv");
QoEdata_RL5 = readmatrix("data/test10.csv");

%% Plot Data

% Start at a later value since first row is
startVal = 500;

figure(1);
clf(1);
hold on;
%for legend
% Low Throughput Buffered - RR
plot(QoEdata_RR1(startVal:end,1),QoEdata_RR1(startVal:end,3),'LineWidth',1,'Color','#EF476F');
% High Throughput Unbuffered - RR
plot(QoEdata_RR1(startVal:end,1),QoEdata_RR1(startVal:end,2),'LineWidth',1,'Color','#FFD166');
% Low Throughput Buffered Video - RL
plot(QoEdata_RL1(startVal:end,1),QoEdata_RL1(startVal:end,3),'LineWidth',1,'Color','#073B4C');
% High Throughput Unbuffered Video - RL
plot(QoEdata_RL1(startVal:end,1),QoEdata_RL1(startVal:end,2),'LineWidth',1,'Color','#118AB2');

plot(QoEdata_RR2(startVal:end,1),QoEdata_RR2(startVal:end,2),'LineWidth',1,'Color','#FFD166');
plot(QoEdata_RR2(startVal:end,1),QoEdata_RR2(startVal:end,3),'LineWidth',1,'Color','#EF476F');
plot(QoEdata_RR3(startVal:end,1),QoEdata_RR3(startVal:end,2),'LineWidth',1,'Color','#FFD166');
plot(QoEdata_RR3(startVal:end,1),QoEdata_RR3(startVal:end,3),'LineWidth',1,'Color','#EF476F');
plot(QoEdata_RR4(startVal:end,1),QoEdata_RR4(startVal:end,2),'LineWidth',1,'Color','#FFD166');
plot(QoEdata_RR4(startVal:end,1),QoEdata_RR4(startVal:end,3),'LineWidth',1,'Color','#EF476F');
plot(QoEdata_RR5(startVal:end,1),QoEdata_RR5(startVal:end,2),'LineWidth',1,'Color','#FFD166');
plot(QoEdata_RR5(startVal:end,1),QoEdata_RR5(startVal:end,3),'LineWidth',1,'Color','#EF476F');
plot(QoEdata_RL2(startVal:end,1),QoEdata_RL2(startVal:end,2),'LineWidth',1,'Color','#118AB2');
plot(QoEdata_RL2(startVal:end,1),QoEdata_RL2(startVal:end,3),'LineWidth',1,'Color','#073B4C');
plot(QoEdata_RL3(startVal:end,1),QoEdata_RL3(startVal:end,2),'LineWidth',1,'Color','#118AB2');
plot(QoEdata_RL3(startVal:end,1),QoEdata_RL3(startVal:end,3),'LineWidth',1,'Color','#073B4C');
plot(QoEdata_RL4(startVal:end,1),QoEdata_RL4(startVal:end,2),'LineWidth',1,'Color','#118AB2');
plot(QoEdata_RL4(startVal:end,1),QoEdata_RL4(startVal:end,3),'LineWidth',1,'Color','#073B4C');
plot(QoEdata_RL5(startVal:end,1),QoEdata_RL5(startVal:end,2),'LineWidth',1,'Color','#118AB2');
plot(QoEdata_RL5(startVal:end,1),QoEdata_RL5(startVal:end,3),'LineWidth',1,'Color','#073B4C');
% plot(QoEdata(startVal:end,1),QoEdata(startVal:end,4),'LineWidth',2);
% plot(QoEdata(startVal:end,1),QoEdata(startVal:end,5),'LineWidth',2);
ylim([35, 100]);
title('Quality of Experience vs. Time');
xlabel('Time');
ylabel('QoE');
legend("Low Throughput Buffered Video-Round-Robin","High Throughput Unbuffered Video-Round-Robin",...
        "Low Throughput Buffered Video-RL Model","High Throughput Unbuffered Video-RL Model",...
    'Location','southeast');


grid minor;
hold off;


%% Find the % Improvement for each
% Start at a later value since first row is
startVal = 500;

% Find average of each invidual run, then find average across all runs
% Low Throughput Buffered Video - Round Robin
avg_LTBV_RR = mean([mean(QoEdata_RR1(startVal:end,3)),...
    mean(QoEdata_RR2(startVal:end,3)),...
    mean(QoEdata_RR3(startVal:end,3)),...
    mean(QoEdata_RR4(startVal:end,3)),...
    mean(QoEdata_RR5(startVal:end,3))]);

% High Throughput Unbuffered Video - Round Robin
avg_HTUV_RR = mean([mean(QoEdata_RR1(startVal:end,2)),...
    mean(QoEdata_RR2(startVal:end,2)),...
    mean(QoEdata_RR3(startVal:end,2)),...
    mean(QoEdata_RR4(startVal:end,2)),...
    mean(QoEdata_RR5(startVal:end,2))]);

% Low Throughput Buffered Video - RL Model
avg_LTBV_RL = mean([mean(QoEdata_RL1(startVal:end,3)),...
    mean(QoEdata_RL2(startVal:end,3)),...
    mean(QoEdata_RL3(startVal:end,3)),...
    mean(QoEdata_RL4(startVal:end,3)),...
    mean(QoEdata_RL5(startVal:end,3))]);

% High Throughput Unbuffered Video - RL Model
avg_HTUV_RL = mean([mean(QoEdata_RL1(startVal:end,2)),...
    mean(QoEdata_RL2(startVal:end,2)),...
    mean(QoEdata_RL3(startVal:end,2)),...
    mean(QoEdata_RL4(startVal:end,2)),...
    mean(QoEdata_RL5(startVal:end,2))]);


% Find Perecent Improvement to be 100*(RL - RR)/ RR
improvement_LTBV = 100*(avg_LTBV_RL - avg_LTBV_RR)/avg_LTBV_RR;
improvement_HTUV = 100*(avg_HTUV_RL - avg_HTUV_RR)/avg_HTUV_RR;

writetable(table(avg_LTBV_RR,avg_LTBV_RL,avg_HTUV_RR,avg_HTUV_RL,...
    improvement_LTBV, improvement_HTUV),'AverageDataResults.csv');










