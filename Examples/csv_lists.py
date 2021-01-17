f = open('StudentsPerformance.csv')
count = 0
sum = 0
max = 0
for line in f:
    if '"gender"' in line:
        continue
    else:
        info = line.split(',')
        # ws_str = info[7].replace('"', '').replace('/n', '')
        # ws = int(ws_str)
        # if ws > 90:
        #     over_ws += 1
        #     ln = info[3][1:-1]
        #     if ln == 'standard':
        #         ln_count += 1
        gen_str   = info[0].replace('"', '').replace('/n', '')
        test_str  = info[2].replace('"', '').replace('/n', '')
        lunch_str = info[3].replace('"', '').replace('/n', '')
        math_str  = info[5].replace('"', '').replace('/n', '')
        read_str  = info[6].replace('"', '').replace('/n', '')
        write_str = info[7].replace('"', '').replace('/n', '')
        if lunch_str == "free/reduced":
            count += 1
            write = int(write_str)
            sum += write

        # math = int(math_str)
        # write = int(math_str)
        # if math==100:
            # count += 1
            # read = int(read_str)
            # sum += int(read)

            # if test_str == "master's degree":
            #     math = int(math_str)
            #     if math > 90:
            #         count += 1

f.close()

# print(max) 100
result = round(float(sum)/count, 2)
print(result)
