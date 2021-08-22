# 項目5: 複雑な式の代わりにヘルパー関数を書く

from urllib.parse import parse_qs

my_values = parse_qs('red=5&blue=0&green=', keep_blank_values=True)
print(my_values)
# {'red': ['5'], 'blue': ['0'], 'green': ['']}

# Pythonではif/else条件式、すなわち三項式で、コードを短く保ちながら、より明確にすることが可能：
red_str = my_values.get('red', [''])
red = int(red_str[0]) if red_str[0] else 0
print(type(red_str)) # <class 'list'>
print(red_str) # ['5'] 
print(red) # 5


# しかし、この例の場合は、複数行にまたがる完全なif/else文ほどには明確ではない：
green_str = my_values.get('green', [''])
if green_str[0]:
    green = int(green_str[0])
else:
    green = 0
print(green_str) # ['']


# このロジックを何回か使う必要があるなら、ヘルパー関数を書くことが解決法となる：
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])
    else:
        return default

# 呼び出しコードは、orを使った複合式やif/else条件式を使った2行のものよりもずっと明確になる：
green = get_first_int(my_values, 'green')
print(green) # 0

# 読みやすさで得られる利益は常に、簡潔さがもたらす便益を上回る。
# DRY原則(Don't Repeat Yourself)を守る。