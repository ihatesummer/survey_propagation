clc
clear
rng(1);

addpath(genpath('functions'));
addpath(genpath('data'));

N_users = 10;
N_resource = 10;
% N_resource = 6;
N_case = 100;
% bandwidth_list = [20; 20; 20; 20; 40; 40; 40; 80; 80; 80; 160; 160; 160; 320; 320; 320];
% bandwidth_list = 40*ones(N_resource,1)+40*[ones(N_resource/2,1); zeros(N_resource/2,1)];
bandwidth_list = 40*ones(N_resource,1);
[N_BW, ~] = size(bandwidth_list);
MA_limit = 7;

% 1,2차원은 rate 정보, 3차원은 index.
for i = 1:N_case
%     snr = 10*rand(1,N_USER);
    [snr_BS1, snr_BS2, user_pos_x, user_pos_y, ind(:,i)]=snr_from_random_position(N_users);
    Rate_BS1 = rate_from_snr(snr_BS1, bandwidth_list);
    Rate_BS1 = Rate_BS1-0.1*rand(N_users,N_BW).*Rate_BS1;
    Rate_BS2 = rate_from_snr(snr_BS2, bandwidth_list);
    Rate_BS2 = Rate_BS2-0.1*rand(N_users,N_BW).*Rate_BS2;
    Rate_single(:,:,i) = 10^(-3)*max(Rate_BS1, Rate_BS2);
    Rate_MA_temp = (Rate_BS1+Rate_BS2);
    Rate_MA_temp = Rate_MA_temp-0.5*rand(N_users,N_BW).*Rate_MA_temp;
    Rate_MA(:,:,i) = 10^(-3)*Rate_MA_temp;    
%     Rate_single(:,:,i) = 10^(-3)*Rate_single;
%     Rate_MA(:,:,i) = 10^(-3)*Rate_MA;
    
%     snr = [10 6 3.16 2.31 1.05 0.8];
%     [Rate_ij_a, Rate_ij_a_bar, Rate_jj] = get_mp_rate_from_snr_old(snr);
%     Rate_jj_all(:,:,i) = Rate_jj;
%     Rate_ij_a_all(:,:,i) = Rate_ij_a;
%     Rate_ij_a_bar_all(:,:,i) = Rate_ij_a_bar;
%     R = Rate_ij_a+ Rate_ij_a_bar+diag(Rate_jj);
%     
%     [Rate_ij_a, Rate_ij_a_bar, Rate_jj] = get_mp_rate_from_snr_beamforming(snr, theta_B_NOMA, theta_B_OMA, theta_U, phi);
%     Rate_jj_beam_all(:,:,i) = Rate_jj;
%     Rate_ij_a_beam_all(:,:,i) = Rate_ij_a;
%     Rate_ij_a_bar_beam_all(:,:,i) = Rate_ij_a_bar;
% %     Rate_ij_a_beam_all(:,:,i) = Rate_ij_a.*get_beamforming_matrix(theta);
% %     Rate_ij_a_bar_beam_all(:,:,i) = Rate_ij_a_bar.*get_beamforming_matrix(theta);
%     RB = Rate_ij_a+ Rate_ij_a_bar+diag(Rate_jj); 
end

% save(['N_Users_' num2str(N_users) '.mat']);
save(['data\test.mat']);
