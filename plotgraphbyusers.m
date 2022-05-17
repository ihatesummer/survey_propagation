clc
clear
close all;

label=1;
for iter = [20:20:100]
    load(['data_all_Users_' num2str(iter) '_Density_' num2str(1.25) '.mat']);
    proposal_25(label)=sum_rate_proposed_average;
    Hungarian_25(label)=sum_rate_Hungarian_average;
    Kmedoids_25(label)=sum_rate_Kmedoids_average;
    label=label+1;
end

 
label=1;
for iter = 20:20:100
    load(['data_all_Users_' num2str(iter) '_Density_' num2str(1.75) '.mat']);
    proposal_75(label)=sum_rate_proposed_average;
    Hungarian_75(label)=sum_rate_Hungarian_average;
    Kmedoids_75(label)=sum_rate_Kmedoids_average;
    label=label+1;
end

%%

x = [20:20:100];
y=[proposal_25; Hungarian_25; Kmedoids_25; proposal_75; Hungarian_75; Kmedoids_75];
p=plot(x,y,"LineWidth",1);
xlim([20 100]);
xlabel("Number of users");
ylabel("Sum rate[bps/Hz]");
p(1).Color = 'red';
p(2).Color = 'green';
p(3).Color = 'blue';
p(4).Color = 'red';
p(5).Color = 'green';
p(6).Color = 'blue';
p(1).LineStyle = '-';
p(2).LineStyle = '-';
p(3).LineStyle = '-';
p(4).LineStyle = '--';
p(5).LineStyle = '--';
p(6).LineStyle = '--';
p(1).Marker = 'o';
p(2).Marker = 'o';
p(3).Marker = 'o';
p(4).Marker = '*';
p(5).Marker = '*';
p(6).Marker = '*';
set(gcf,'Position',[0 100 700 500]);
grid on
box on
legend("Proposed (1.25)", "Hungarian (1.25)", "NLUPA (1.25)", "Proposed (1.75)", "Hungarian (1.75)", "NLUPA (1.75)", 'Location','northwest')
savefig(['plotgraphbyusers.fig'])