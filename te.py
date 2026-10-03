''''
nums = 0

for number in range(100):
    if number < 10:
        continue

    print(number)
    steps = 0

    while number > 1:
        steps += 1

        if number / 2 - number // 2 == 0:
            number = number // 2

        else:
            number -= 1

    if steps == 7:
        print("быстрое")
        nums += 1
    else:
        print("не быстрое:", steps)

    print(" ")

print("быстрых чисел:", nums)

count = 0

for n in range(10, 31):

    if n % 4 == 0 or n // 10 == n % 10:

        count += 1

print(count)
text = input()

cur_length = 0
max_length = 0

for symbol in text:
    if symbol.isdigit():
        cur_length = cur_length + 1

    else:
        cur_length = 0

    if cur_length > max_length:
        max_length += 1

print(max_length)

number = int(input())
count = 1

while number > 0:
    d = number // 10

    print(count, d)

    if d > 5:
        print("больше")
        count += d

    number = number % 10

print(count)
'''

nums = 0
smaller = 10000

for number in range(10000):
    if number < 1000:
        continue

    have_zero = False
    for x in str(number):
        if x == "0":
            have_zero = True

    print(number)

    if not have_zero:
        print("нет нуля\n")
        continue

    str_num = str(number)

    start_num = str_num[0]
    end_num = str_num[-1]

    middle_num = int(str_num[len(str_num)//2])
    middle_plus = middle_num+middle_num

    if int(start_num)+int(end_num) != middle_plus:
        print("сумма первой и последней цифр\nне равна сумме двух средних цифр")
        continue

    if middle_plus//6 - middle_plus/6 == 0:
        print("сбалансированное")
        nums += 1

        if number < smaller:
            smaller = number

    else:
        print("не сбалансированное")

print(" ")

print("сбалансированных чисел:", nums)
print("наименьшее:", smaller)