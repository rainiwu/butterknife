%% Set up the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 3);

% Specify range and delimiter
opts.DataLines = [2, Inf];
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["Time (s)", "Buffered", "Unbuffered"];
opts.VariableTypes = ["double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
QoEtable = readtable("C:\Users\Jim\Documents\GitHub\butterknife\butter\butter\QoEcsv Sun Nov 27 211948 2022.csv", opts);

clear opts

%% Plot Data

figure(1);
clf(1);
hold on;
plot(QoEtable.Time_s_,QoEtable.Buffered,QoEtable.Time_s_,QoEtable.Unbuffered,'LineWidth',2);
title('QoE Metrics');
xlabel('Time');
ylabel('QoE');
grid minor;
hold off;