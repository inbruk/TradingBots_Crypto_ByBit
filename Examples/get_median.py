def get_median(num_values):
    srt_values = sorted(num_values)
    lst_len = len(srt_values)
    pos1 = lst_len // 2
    if lst_len % 2 != 0:
        return int(srt_values[pos1])
    else:
        pos2 = pos1 - 1
        return (srt_values[pos1] + srt_values[pos2]) / 2



print(get_median([3, 3, 7, 9]))
print(get_median([9, 7]))
print(get_median([7]))
