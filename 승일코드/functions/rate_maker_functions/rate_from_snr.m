function [Rate_BS] = rate_from_snr(snr, bandwidth_list)
Rate_BS=log2(1 + snr)*bandwidth_list';
end