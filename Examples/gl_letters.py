name = 'Севастиан'
gl_char_lst = [ 'а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я' ]
gl_char = '- гласная буква'
so_char = '- согласная буква'
for curr_char in name:
    lo_curr_char = curr_char.lower()
    if lo_curr_char in gl_char_lst:
        print(curr_char, gl_char)
    else:
        print(curr_char, so_char)