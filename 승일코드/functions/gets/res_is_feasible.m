function [flag] = res_is_feasible(bi_res)
[N_USER, ~] = size(bi_res);
sum_of_res = sum(bi_res);
flag = true;

for i = 1:N_USER
    if sum_of_res(i) > 2
        flag = false;
        break
    end
end

if sum(sum_of_res) ~= N_USER
    flag = false;
end

end

