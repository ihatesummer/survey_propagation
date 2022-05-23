clc
clear
% rng(2);
tic

addpath('functions');
N_ITER =  1000;
DAMPING = 0;

% load("N_Users_20.mat");
load("data\test.mat");

for i = [1:10]
    
    %message passing
    [alpha, rho, phi, zeta, alpha_1_res, alpha_4_res] = mp_sol(Rate_single(:,:,i), Rate_MA(:,:,i), ind(:,i), MA_limit, N_ITER, DAMPING);
    
    sumalrho(:,:,i)=alpha+rho;
    sumzephi(:,i)=zeta+phi;
    
    alpha_reg(:,:,i) = alpha;
    rho_reg(:,:,i) = rho;
    phi_reg(:,i) = phi;
    zeta_reg(:,i) = zeta;
%     [res_bi, not_sloved]= find_feasible_from_message(alpha+rho);
%     sum_rate_proposed(i)=get_sum_rate(Rate_ij_a, Rate_ij_a_bar, Rate_jj, res_bi);
    allo(:,:,i) = sumalrho(:,:,i)>0;
    R_sum_proposed(i) = sum_rate(Rate_single(:,:,i), Rate_MA(:,:,i), allo(:,:,i));
end
%%

sum(allo>0,1)
% savefig(['data_Users_' num2str(N_USER) '_Density_' num2str(Density) '.fig'])
save(['data\data_all_Users_' num2str(N_users) '.mat'])
% xlim([600 inf]);
toc