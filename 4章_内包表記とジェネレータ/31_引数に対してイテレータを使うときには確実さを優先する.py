# 項目31: 引数に対してイテレータを使うときには確実さを優先する

# 関数のパラメータがオブジェクトのリストのとき、そのリストに対して何度も繰り返す処理が必要な場合がよくある。
# 例えば、米国テキサス州の旅行者の人数について分析するとする。
# 各都市への訪問数(年ごとに百万人単位)のデータセットがあるとする。
# 旅行者全体の何パーセントを各都市で受け入れているか計算する：
def normalize(numbers: list):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0
# [11.538461538461538, 26.923076923076923, 61.53846153846154]

# このコードをスケールアップするには、テキサス州のすべての都市を含んだファイルからデータを読み込む。
# これを行うには、後で全世界の旅行者数のようなずっと大きなメモリが必要なデータセットにも
# 同じ関数を再利用したいので、ジェネレータを定義する：
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)

# 驚くべきことに、ジェネレータread_visitsの戻り値にnormalizeを呼び出しても何も結果が得られない：
it = read_visits('my_numbers.txt')
percentages = normalize(it)
print(percentages)
# []

# この振る舞いの原因は、イテレータが結果を一度だけしか生成しないこと。
# StopIteration例外を既に起こしたイテレータやジェネレータに反復処理をしても何の結果も得られない：
it = read_visits('my_numbers.txt')
print(list(it))
print(list(it)) # 既に反復処理は完了した
# [15, 35, 80]
# []

# 困るのは、既に完了したイテレータに対して反復処理をしても、何のエラーも生じないこと。
# この問題を解決するために、入力イテレータを明示的に終わるまで動かし、内容全体の複製をリストに保持する。
# そうすれば、必要なだけ何度でもリストのデータに対して反復処理ができる：
def normalize_copy(numbers):
    numbers = list(numbers) # イテレータを複製
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# この関数は、ジェネレータread_visitsの戻り値を正しく処理する：
it = read_visits('my_numbers.txt')
percentages = normalize_copy(it)
print(percentages)
assert sum(percentages) == 100.0
# [11.538461538461538, 26.923076923076923, 61.53846153846154]

# しかし、この方式には、入力イテレータの複製の内容が巨大になりうるという問題がある。
# イテレータの複製によって、プログラムがメモリを食いつぶし、クラッシュしかねない。
# スケーラビリティに関するこの危険性こそ、最初にread_visitsをジェネレータとして書いた理由。
# これを回避する1つの方法は、呼ばれるたびに新たなイテレータを返す関数を受け入れること：
def normalize_func(get_iter):
    total = sum(get_iter) # 新たなイテレータ
    result = []
    for value in get_iter(): # 新たなイテレータ
        percent = 100 * value / total
        result.append(percent)
    return result

# normalize_funcを使うと、ジェネレータを呼び出して新たなイテレータをそのたびに生成するlamda式を渡すことができる：
path = 'my_numbers.txt'
percentages = normalize_func(lambda: read_visits(path))
print(percentages)
assert sum(percentages) == 100.00
# [11.538461538461538, 26.923076923076923, 61.53846153846154]

# これは動くが、このようにラムダ関数を渡さなければならないことは面倒。
# 同じ結果が得られるより良い方法は、イテレータプロトコルを実装した新たなコンテナクラスを提供すること。
# イテレータプロトコルとは、Pythonのforループや関連する式が、コンテナ型の内容をどのように横断するか示すもの。

# Pythonがfor x in fooのような文を受け取ると、実際には、iter(foo)を呼び出す。
# この組み込み関数iterは、特殊メソッドfoo.__iter__を次に呼び出す。
# __iter__メソッドは、(特殊メソッド__next__を実装した)イテレータオブジェクトを返さなければならない。
# そうして、forループはイテレータオブジェクトに対して組み込み関数nextを、
# それが完了する(StopIteration例外が発生する)まで繰り返し呼び出す。

# これは、複雑なように思えるが、実際には、
# 自分のクラスに対するこれらの振る舞いのすべてをジェネレータとした__iter__メソッドを実装して実現できる。
# 旅行者データを含むファイルを読み込むイテラブルなコンテナクラスを次のように定義する：
class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path
    
    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

# この新たなコンテナ型は、何の修正も加えていない元の関数に渡されても正しく働く：
visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0
# [11.538461538461538, 26.923076923076923, 61.53846153846154]

# これが動くのは、normalizeのsumメソッドが新たなイテレータオブジェクトを生成するためにReadVisits.__iter__を呼び出すから。
# 数を正規化するforループも、第2のイテレータオブジェクトを生成するために__iter__を呼び出す。
# これらのイテレータは、それぞれ独立に終わるまで進められ、どの反復処理でも入力データ値がすべて処理されることを保証する。
# しかし、この方式には唯一、入力データを複数回読み込んでしまうという欠点がある。

# イテレータプロトコルでは、組み込み関数iterにイテレータが渡されると、iterがイテレータそのものを返すことになっている。
# 対照的に、コンテナ型がiterに渡されると、そのたびに、新たなイテレータオブジェクトが返される。
# そうして、この振る舞いの入力値をテストして、条件を満たさないと、TypeErrorを起こして反復処理できない引数を拒絶する。
# その他に、組み込みモジュールcollections.abcでIteratorクラスを定義し、
# 起こりかねない問題がないかどうかisinstanceテストを行うことができる：
from collections.abc import Iterator

def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# この関数は、listやReadVisitsのような入力に対しても、
# それらがイテレータプロトコルに従うイテラブルなコンテナなので期待通りに働く：
visits = [15, 35, 80]
normalize_defensive(visits)
assert sum(percentages) == 100.0

visits = ReadVisits
normalize_defensive(visits)
assert sum(percentages) == 100.0

# この関数は、入力がコンテナではなく、イテレータの場合に例外が発生する：
visits = [15, 35, 80]
it = iter(visits)
normalize_defensive(it)
# Traceback ...
# TypeError: Must supply a container