# 項目8: イテレータを並列に処理するにはzipを使う

names = ['Cecilia', 'Lise', 'Marie']
counts = [len(n) for n in names]
longest_name = None
max_count = 0
for i, name in enumerate(names):
    count = counts[i]
    if count > max_count:
        longest_name = name
        max_count = count

print(longest_name)
# Cecilia

# このようなコードをもっと明確にするために、Pythonには組み込み関数zipがある。
# zipジェネレータは、各イテレータからの次の値のタプルをyieldする。
# これらのタプルは、for文の内側で直接アンパックできる。
# 結果として、コードは、複数のリストにインデックスを使うよりもずっと明確になる：
for name, count in zip(names, counts):
    if count > max_count:
        longest_name = name
        max_count = count