function rho_res = update_rho(rho, alpha, DAMPING)
[N_USER, N_BW] = size(rho);
rho_old = rho;
INF = 10^6;
            
for i = 1:N_USER
    for a = 1:N_BW
        temp = alpha(i, :);
        temp(a) = -INF;
        rho(i, a) = -max(temp);
    end
end

rho_res = rho*(1- DAMPING) + rho_old*DAMPING;
end