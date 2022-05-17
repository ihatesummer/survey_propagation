function [snr_BS1, snr_BS2, user_pos_x, user_pos_y, ind] = snr_from_random_position(N_users)
%uniform random position in rectangular

BS1_pos = [0, 0];
BS2_pos = [10, 0];
MAX_DISTANCE=10;

user_pos_x = BS1_pos(1)-MAX_DISTANCE+(2*MAX_DISTANCE+BS2_pos(1)-BS1_pos(1))*rand(N_users,1);
user_pos_y = -MAX_DISTANCE+2*MAX_DISTANCE*rand(N_users,1);
% user_pos_x = [4; -3; -5; 13; 15];
% user_pos_y = [0; 2; -3; 1; -4];

[theta_BS1,user_pos_r_BS1] = cart2pol(user_pos_x,user_pos_y);
[theta_BS2,user_pos_r_BS2] = cart2pol(user_pos_x-BS2_pos(1),user_pos_y);

N = 1;
eta = 3;

% BS1

%%rayleigh fading 적용
% Rayleigh_coefficient_H = sqrt(user_dist_from_BS.^-eta)*(randn(1,N) + 1i*randn(1,N))/sqrt(2);

%%rayleigh fading 적용안함
Rayleigh_coefficient_H = sqrt(user_pos_r_BS1.^-eta);

Rayleigh_coefficient_G = (abs(Rayleigh_coefficient_H)).^2;

TX_POWER_DB = -15;  %10 20 40     %dB
TX_POWER_LN = (10^-3)*db2pow(TX_POWER_DB);%Linear
% NOISE_POWER_DB = pow2db(1.38*10^(-23) * 290 * 10^7 / 10^(-3)); %-114 %kTB/1mW dBm
NOISE_POWER_DB = -80; %-90
NOISE_POWER_LN = (10^-3)*db2pow(NOISE_POWER_DB);

snr_BS1 = TX_POWER_LN.*Rayleigh_coefficient_G./NOISE_POWER_LN;
snr_BS1 = snr_BS1+(10^7-snr_BS1).*(snr_BS1>10^7);

% BS2
Rayleigh_coefficient_H = sqrt(user_pos_r_BS2.^-eta);

Rayleigh_coefficient_G = (abs(Rayleigh_coefficient_H)).^2;

TX_POWER_DB = -15;  %10 20 40     %dB
TX_POWER_LN = (10^-3)*db2pow(TX_POWER_DB);%Linear
% NOISE_POWER_DB = pow2db(1.38*10^(-23) * 290 * 10^7 / 10^(-3)); %-114 %kTB/1mW dBm
NOISE_POWER_DB = -80; %-90
NOISE_POWER_LN = (10^-3)*db2pow(NOISE_POWER_DB);

snr_BS2 = TX_POWER_LN.*Rayleigh_coefficient_G./NOISE_POWER_LN;
snr_BS2 = snr_BS2+(10^7-snr_BS2).*(snr_BS2>10^7);

ind = 1*(snr_BS1>snr_BS2)+2*(snr_BS1<snr_BS2);
snr = max(snr_BS1, snr_BS2);

[snr I] = sort(snr,'descend');

user_pos_x = user_pos_x(I);
user_pos_y = user_pos_y(I);
ind = ind(I);
snr_BS1 = snr_BS1(I);
snr_BS2 = snr_BS2(I);


% phi = angdiff(repmat(user_pos_a,N_users,1),repmat(user_pos_a,N_users,1)');
end