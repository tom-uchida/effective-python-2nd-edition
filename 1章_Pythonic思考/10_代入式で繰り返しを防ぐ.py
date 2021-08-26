# 項目10: 代入式で繰り返しを防ぐ

# 代入式は「a := b」と書かれ、「aウォラスb」と発音する。
# 代入式は、if文の条件式のような、これまで代入文が許されなかった箇所で変数に代入できるので便利。
# 代入式の値は、walrus演算子の左側の識別子に代入される値。
fresh_fruit = {
    'apple': 10,
    'banana': 8,
    'lemon': 5,
}

def make_lemonade(count):
    print("make_lemonade")

def out_of_stock():
    print("out_of_stock")

if count := fresh_fruit.get('lemon', 0):
    make_lemonade(count)
    print(count) # 5
else:
    out_of_stock()