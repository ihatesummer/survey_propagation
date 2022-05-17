function [Rate_sum] = sum_rate(Rate_single, Rate_MA, allo)
[~,N_resource] = size(allo);
mode = sum(allo, 1);
Rate_sum = 0;

for i = 1:N_resource
    if mode(i) == 1
        Rate_sum = Rate_sum + sum(Rate_MA(:,i).*allo(:,i));
    end
    if mode(i) == 2
        Rate_sum = Rate_sum + sum(Rate_single(:,i).*allo(:,i));
    end
end

end

