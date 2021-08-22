# 項目6: インデックスではなく複数代入アンパックを使う

# 重要なアンパックの用途が、forループや同様の内包表記とジェネレータ式におけるターゲットリスト。
# 比較対象のため、アンパックを使わずにスナック食品リストのイテレーション例を次に示す：
names = ['pretzels', 'carrots', 'bacon']
snacks = [('bacon', 350), ('donut', 240), ('muffin', 190)]
for i in range(len(snacks)):
    item = snacks[i]
    name = item[0]
    calories = item[1]
    print(f'#{i+1}: {name} has {calories} calories')
    #1: bacon has 350 calories
    #2: donut has 240 calories
    #3: muffin has 190 calories


# これは動きますが、とても読みづらいコード。
# snacksの構造の深さごとにインデックスを使うため文字が余計に必要。
# アンパックを組み込み関数enumerateとともに使うことで、同じ出力が次のコードで得られる：
for rank, (name, calories) in enumerate(snacks, 1):
    print(f'#{rank}: {name} has {calories} calories')
    #1: bacon has 350 calories
    #2: donut has 240 calories
    #3: muffin has 190 calories

# これは、この種のループを書く短くて理解しやすいPythonicなやり方。インデックスを使う必要がない。