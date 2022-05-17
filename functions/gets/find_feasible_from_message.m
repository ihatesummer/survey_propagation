function [feasible_sol, not_sloved] = find_feasible_from_message(msg_res)
[N_USER, ~] = size(msg_res);
INF = 10^6;
bi_msg = msg_res > 0;
sum_bi_msg = sum(bi_msg);
feasible_sol = bi_msg;
iter = 0;
not_sloved = 0;

while ~res_is_feasible(feasible_sol)
    head_candidate = zeros(1, N_USER);
    infeasible_node = zeros(1, N_USER);
    sum_col_feasible_sol = sum(feasible_sol);
    for i = 1:N_USER
        if sum_col_feasible_sol(i) == 1
            head_candidate(i) = 1;
        end
        if sum_col_feasible_sol(i) > 2
            infeasible_node(i) = 1;
        end
    end
    
    for i = N_USER:-1:1
        if infeasible_node(i) == 1
            feasible_sol(:,i) = 0;
            msg_col = msg_res(:,i)- INF * sum(feasible_sol, 2);
            
            [~, max_idx_col] = max(msg_col);
            feasible_sol(max_idx_col,i) = 1;
            msg_col(max_idx_col) = -INF;
            
            [~, max_idx_col] = max(msg_col);
            feasible_sol(max_idx_col,i) = 1;
            msg_col(max_idx_col) = -INF;
            
            head_candidate(i) = 0;
            
            for j = 1:N_USER
                if msg_col(j) > - INF
                    msg_row = msg_res(:, j)' - INF * (1 - head_candidate);
                    [~, max_idx_row] = max(msg_row);
                    feasible_sol(j, max_idx_row) = 1;
                end
            end
            
            infeasible_node(i) = 0;
        end
    end
    iter = iter+1;
    if iter>10
        not_sloved=1;
        break;
    end
end

