def count_letters(sentence, average=False):
    lst = sentence.split()
    if average==True:
        lst_cnt = list(map(lambda x:len(x), lst))
        return sum(lst_cnt) / len(lst_cnt)
    else:
        wo_spaces = ''.join(lst);
        return len(wo_spaces)

result = count_letters('I will build my own theme park')
print(result)

result = count_letters('I will build my own theme park', average=True)
print(result)