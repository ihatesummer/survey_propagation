function phi_res = update_phi(phi, rho, Rate_single, Rate_MA, ind, DAMPING)
[N_BW, ~] = size(phi);
phi_old = phi;
INF = 10^6;
            
for a = 1:N_BW
        temp11 = Rate_MA(:,a) - Rate_single(:,a);
        temp11 = temp11 - INF.*(ind~=1);

        temp12 = Rate_single(:,a) + rho(:,a);
        temp12 = temp12 - INF.*(ind~=2);

        phi_1 = max(temp11) - max(temp12);

        temp21 = Rate_MA(:,a) - Rate_single(:,a);
        temp21 = temp21 - INF.*(ind~=2);

        temp22 = Rate_single(:,a) + rho(:,a);
        temp22 = temp22 - INF.*(ind~=1);

        phi_2 = max(temp21) - max(temp22);

        phi(a) = max([phi_1, phi_2]);
end

phi_res = phi*(1- DAMPING) + phi_old*DAMPING;
end