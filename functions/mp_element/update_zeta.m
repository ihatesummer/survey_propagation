function zeta_res = update_zeta(zeta, phi, MA_limit, DAMPING)
[N_BW, ~] = size(zeta);
zeta_old = zeta;
INF = 10^6;
            
if MA_limit == 0
    zeta_res = -INF.*ones(N_BW, 1);
    return;
end

sorted_phi = sort(phi);
pivot_big = sorted_phi(end - MA_limit + 1);
    
if MA_limit >= N_BW
    pivot_small = 0;
else
    pivot_small = sorted_phi(end - MA_limit);
end

% if MA_limit >= N_BW
%     zeta = zeros(1, N_BW);
% end

for j = 1:N_BW
    if phi(j) > pivot_small
        zeta(j) = - pivot_small;
    else
        zeta(j) = - pivot_big;
    end
end

zeta_res = zeta*(1- DAMPING) + zeta_old*DAMPING;
end