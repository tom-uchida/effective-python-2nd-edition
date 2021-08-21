# 項目4: Cスタイルフォーマット文字列とstr.formatは使わずf文字列で埋め込む

key = 'my_var'
value = 1.234

f_string = f'{key:<10} = {value:.2f}'

c_tuple  = '%-10s = %.2f' % (key, value)

str_args = '{:<10} = {:.2f}'.format(key, value)

str_kw   = '{key:<10} = {value:.2f}'.format(key=key, value=value)

c_dict   = '%(key)-10s = %(value).2f' % {'key': key, 'value': value}

assert c_tuple == c_dict == f_string
assert str_args == str_kw == f_string

print(f_string)
print(c_tuple)
print(str_args)
print(str_kw)
print(c_dict)
# my_var     = 1.23
# my_var     = 1.23
# my_var     = 1.23
# my_var     = 1.23
# my_var     = 1.23