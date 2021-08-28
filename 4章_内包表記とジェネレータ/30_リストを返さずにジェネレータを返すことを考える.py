# 項目30: リストを返さずにジェネレータを返すことを考える

# 結果をシーケンスで返す関数の実装の最も単純な選択は、要素のリストを返すこと：
def index_words(text: str):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result

address = 'Four score and seven years ago...'
result = index_words(text=address)
print(result[:10])
# このindex_words関数には、2つの問題がある。

# まず、コードが複雑で読みにくいという問題がある。新たな結果が得られるたびに、appendメソッドを呼び出している。
# メソッド呼び出しの部分(result.append)がリストに追加される値(index + 1)より目立っている。
# ジェネレータ(yield式を使う関数)を使うとこの関数はもっとうまく書ける。
# 次のように、前と同じ結果を生成するジェネレータ関数を定義する：
def index_words_iter(text: str):
    print("called.")
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1

# ジェネレータ関数は、呼び出されると実際に作業をせずに、直ちにイテレータを返す。
# 組み込み関数nextが呼び出されるごとに、イテレータはジェネレータを次のyield式に1つ進める。
# ジェネレータによりyieldに渡される値は、それぞれイテレータによって呼び出し元に返される：
it = index_words_iter(address)
print(next(it))
print(next(it))

# index_words_iter関数は、結果リストに関する処理のすべてが省かれているので、はるかに読みやすくなっている。
# 結果はyield式に渡される。ジェネレータ呼び出しで返されるイテレータは、組み込み関数listに渡して簡単にリストに変換できる：
result = list(index_words_iter(address))
print(result[:10])

# index_wordsの第2の問題は、返す前に、すべての結果をリストに格納する必要があること。
# 入力が大量にあるときには、プログラマがメモリを食いつぶしクラッシュを引き起こしかねない。
# 一方で、この関数のジェネレータバージョンは一定のメモリしか必要としないので、どんな長さの入力にも容易に対応できる。
# 例えば、次のように、ファイルから一時に一行ずつ入力して、1単語ずつyieldで出力するストリーム型のジェネレータを定義する：
def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset

# この関数に必要な作業メモリは、入力中の行の最大長あれば大丈夫。
# このジェネレータを実行すると同じ結果が得られる：
with open('address.txt', 'r') as f:
    it = index_file(f)
    results = islice(it, 0, 10)
    print(results)
# [0, 5, 11, 15, 21, 27, 31, 35, 43, 51]

# このようなジェネレータを定義するときは、返されるイテレータがステートフルで再利用できないことを、
# 呼び出し元が認識すべきということを理解しておく。