# a = 0.3
a = float(input())
def get_hash(key, size):
    return (key*a - (key*a//1) *1)*size
x = 0.9
y = 1
result = x - (x//y) * y

# print(a, int(get_hash(8,8)))

key = 3
# a = 0.3
size = 8
result = int((key*a - (key*a//1) *1)*size)
print(result, type(a))