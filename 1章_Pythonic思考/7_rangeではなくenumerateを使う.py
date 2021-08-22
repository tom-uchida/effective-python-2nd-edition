# 項目7: rangeではなくenumerateを使う

# リストの処理で、リスト中の要素のインデックスが必要なこともよくあります。
# 例えば、好きなフレーバーのアイスクリームのランキングを出力したいとする。
# まず考えられるのは、rangeを使う方法：
flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print(f'{i + 1}: {flavor}')
    # 1: vanilla
    # 2: chocolate
    # 3: pecan
    # 4: strawberry

# これは、リストの長さが必要で、配列のようにインデックスを使う必要があり、ステップが多くて読むのが面倒です。
# Pythonには、このような状況に対する組み込み関数enumerateがあります。
# enumerateは、ループのインデックスとイテレータの次の値の対をyieldします。
# enumerateでyieldされる各対は、for文でうまくアンパックできる：
for i, flavor in enumerate(flavor_list):
    print(f'{i + 1}: {flavor}')
    # 1: vanilla
    # 2: chocolate
    # 3: pecan
    # 4: strawberry