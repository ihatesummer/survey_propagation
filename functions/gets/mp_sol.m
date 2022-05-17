function [alpha, rho, phi, zeta, alpha_1_res, alpha_4_res] = mp_sol(Rate_single, Rate_MA, ind, MA_limit, N_ITER, DAMPING)
% INF = 10^6
[N_USER, N_BW] = size(Rate_single);

alpha = zeros(N_USER, N_BW);
rho = zeros(N_USER, N_BW);
phi = zeros(N_BW, 1);
zeta = zeros(N_BW, 1);
% sim_res_history = zeros(N_USER, N_BW, N_ITER);

for iter = 1:N_ITER
    [alpha, alpha_1_res, alpha_4_res] = update_alpha(alpha, rho, zeta, Rate_single, Rate_MA, ind, DAMPING);
    rho = update_rho(rho, alpha, DAMPING);
    phi = update_phi(phi, rho, Rate_single, Rate_MA, ind, DAMPING);
    zeta = update_zeta(zeta, phi, MA_limit, 0);
    
%     alpha_1_res<alpha_4_res;

%     sim_res_history(:, :, iter) = alpha + rho;
end
% sim_res_final = get_mp_sim_res(alpha, rho);
end

