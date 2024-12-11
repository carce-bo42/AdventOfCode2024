
def do_weird_fibonacci(times, numbers):

    if times == 0:
        return numbers
    
    result = []
    for n in numbers:
        if n == '0':
            result.append('1')
        elif len(n)%2 == 0:
            result.append(n[0:len(n)//2])
            result.append(str(int(n[len(n)//2:len(n)])))
        else:
            result.append(str(int(n)*2024))

    return do_weird_fibonacci(times-1, result)

fname = "input.test2.txt"
count = 0
numbers = []
with open(fname) as file:
    for line in file:
        numbers = line.strip().split()

result = do_weird_fibonacci(25, numbers)
print(len(result))
