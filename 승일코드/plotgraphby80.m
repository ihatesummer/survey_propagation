clc
clear
close all;

label=1;

load(['data_all_Users_' num2str(80) '_Density_' num2str(1.25) '.mat']);
sum_rate_proposed_1_25=sum_rate_proposed;
sum_rate_Hungarian_1_25=sum_rate_Hungarian;
sum_rate_Kmedoids_1_25=sum_rate_Kmedoids;

 

load(['data_all_Users_' num2str(80) '_Density_' num2str(1.75) '.mat']);
sum_rate_proposed_1_75=sum_rate_proposed;
sum_rate_Hungarian_1_75=sum_rate_Hungarian;
sum_rate_Kmedoids_1_75=sum_rate_Kmedoids;


%%
hold on
p1=cdfplot(sum_rate_proposed_1_25);
p2=cdfplot(sum_rate_Hungarian_1_25);
p3=cdfplot(sum_rate_Kmedoids_1_25);
p4=cdfplot(sum_rate_proposed_1_75);
p5=cdfplot(sum_rate_Hungarian_1_75);
p6=cdfplot(sum_rate_Kmedoids_1_75);
hold off
title("");

xlabel("Sum rate[bps/Hz]");
ylabel("CDF");
p1.LineWidth = 1;
p2.LineWidth = 1;
p3.LineWidth = 1;
p4.LineWidth = 1;
p5.LineWidth = 1;
p6.LineWidth = 1;
p1.Color = 'red';
p2.Color = 'green';
p3.Color = 'blue';
p4.Color = 'red';
p5.Color = 'green';
p6.Color = 'blue';
p1.LineStyle = '-';
p2.LineStyle = '-';
p3.LineStyle = '-';
p4.LineStyle = '--';
p5.LineStyle = '--';
p6.LineStyle = '--';
xlim([0 600]);
set(gcf,'Position',[0 100 350 500]);
grid on
box on
legend("Proposed (\lambda=1.25)", "Hungarian (\lambda=1.25)", "NLUPA (\lambda=1.25)", "Proposed (\lambda=1.75)", "Hungarian (\lambda=1.75)", "NLUPA (\lambda=1.75)", 'Location','northwest')
savefig(['plotgraphby80.fig'])