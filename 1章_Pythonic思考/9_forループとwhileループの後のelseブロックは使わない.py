# 項目9: forループとwhileループの後のelseブロックは使わない

# Pythonでのelse,except,finallyのすべての用法から、初めてのプログラマは、
# for/elseのelse部分は、「ループが完了しなかったらこれをしなさい」という意味だと思い込んでしまう。
# 実際にはこれはまったく反対。ループでbreak文が実行されると、実はelseブロックがスキップされる：
for i in range(3):
    print('Loop', i)
    if i == 1:
        break
else:
    print('Else block!')
# Loop 0
# Loop 1

# この振る舞いの背景にあるのは、ループの後のelseブロックが、ループして何かを探す場合に役立つということ。
# しかし、実際には、そのようなコードは書かない。代わりにヘルパー関数を書く。
# そのヘルパー関数を書くには、次の2通りのスタイルがよく使われる。

# 最初の方式は、探している条件が見つかり次第、早めにループを抜ける。
# ループが終了したら、デフォルトの結果を返す：
def coprime(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True

assert coprime(4, 9)
assert not coprime(3, 6)

# 第2の方式は、ループして探していたものが見つかったかどうかを示す結果変数を使う。
# 何か見つかり次第、breakしてループを抜ける：
def coprime_alternate(a, b):
    is_coprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_coprime = False
            break
    return is_coprime

assert coprime_alternate(4, 9)
assert not coprime_alternate(3, 6)

# どちらのやり方もコードを初めて読む人にも明瞭。状況によってどちらかを選べばよい。
# ループのような単純な構成要素は、Pythonでは自明であるべき。ループの後のelseブロックの使用は避けるべき。