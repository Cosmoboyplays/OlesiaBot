
def func(a, b):
    print(a/b)

try:
    func(2, 0)
except Exception as e:
    print('Отловили', e)