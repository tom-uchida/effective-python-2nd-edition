def generator():
    for i in range(5):
        yield i

for g in generator():
    print(g)
# 0
# 1
# 2
# 3
# 4