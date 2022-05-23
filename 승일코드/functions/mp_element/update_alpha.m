function [alpha_res, alpha_1_res, alpha_4_res] = update_alpha(alpha, rho, zeta, Rate_single, Rate_MA, ind, DAMPING)
[N_USER, N_BW] = size(alpha);
alpha_old = alpha;
INF = 10^6;
            
for a = 1:N_BW
    for i = 1:N_USER
        % BS1 connected
        if ind(i) == 1
            temp1 = Rate_single(:,a) + rho(:,a);
            temp1 = temp1.*(ind==1) - INF.*(ind~=1);
            temp1(i) = -INF;
            alpha_1 = Rate_single(i,a)-max(temp1);
            alpha_1_res(i,a) = alpha_1;
  
            temp21 = Rate_MA(:,a) + rho(:,a);
            temp21(i) = -INF;
            temp22 = Rate_single(:,a) + rho(:,a);
            temp22 = temp22 - INF*(ind~=2);
            alpha_2 = Rate_single(i,a)-max(temp21)+max(temp22)-zeta(a);

            alpha_3 = Rate_MA(i,a)-max(temp1)-max(temp22)+zeta(a);

            alpha_4 = Rate_MA(i,a)-max(temp21);
            alpha_4_res(i,a) = alpha_4;
            
%             alpha(i,a) = max([alpha_1, alpha_2, alpha_3, alpha_4]);
            alpha(i,a) = max([alpha_1, alpha_4]);
            alpha(i,a) = alpha_1;
        end

% BS2 connected
        if ind(i) == 2
            temp1 = Rate_single(:,a) + rho(:,a);
            temp1 = temp1.*(ind==2) - INF.*(ind~=2);
            temp1(i) = -INF;
            alpha_1 = Rate_single(i,a)-max(temp1);
            alpha_1_res(i,a) = alpha_1;

            temp21 = Rate_MA(:,a) + rho(:,a);
            temp21(i) = -INF;
            temp22 = Rate_single(:,a) + rho(:,a);
            temp22 = temp22 - INF*(ind~=1);
            alpha_2 = Rate_single(i,a)-max(temp21)+max(temp22)-zeta(a);

            alpha_3 = Rate_MA(i,a)-max(temp1)-max(temp22)+zeta(a);

            alpha_4 = Rate_MA(i,a)-max(temp21);
            alpha_4_res(i,a) = alpha_4;

%             alpha(i,a) = max([alpha_1, alpha_2, alpha_3, alpha_4]);
            alpha(i,a) = max([alpha_1, alpha_4]);
            alpha(i,a) = alpha_1;
        end
    end
end
alpha_res = alpha*(1- DAMPING) + alpha_old*DAMPING;
end